class ProductUnavailable(Exception):
    """
    Exception definition for when product or not enough product quantity is available
    """

    pass


class Product:
    """
    Definition for the product class
    """

    @staticmethod
    def calc_price(price:float, quantity:int) -> float:
        """
        Just fooling around with static methods
        """
        return price * quantity

    def __init__(self, name:str, price:float, quantity:int) -> None:
        if len(name) == 0:
            raise ValueError("Product name can not be empty")
        self._name = name
        if not (isinstance(price, float) or isinstance(price, int)):
            raise ValueError("Please ensure price is valid")
        if price < 0:
            raise ValueError("Please ensure price is valid")
        self._price = price
        if not isinstance(quantity, int):
            raise ValueError("Please ensure quantity is a valid number")
        if quantity < 0:
            raise ValueError("Please ensure quantity is a valid number")
        self._quantity:int = quantity
        self.__active = True

    def get_quantity(self) -> int:
        """Getter function for quantity.
        Returns the quantity (int)."""
        return self._quantity

    def set_quantity(self, quantity:int) -> None:
        """Setter function for quantity. If quantity reaches 0, deactivates the product."""
        self._quantity = quantity
        if quantity == 0:
            self.__active = True

    def get_name(self) -> str:
        return self._name

    def set_name(self, new_name:str):
        if len(new_name) == 0:
            raise ValueError ("Please ensure the new name is valid")
        self._name = new_name

    def get_price(self) -> float:
        return self._price

    def set_price(self, new_price: float):
        try:
            self._price:float = new_price
        except ValueError as e:
            raise ValueError(
                "Please ensure price is a valid price"
            ) from e

    def is_active(self) -> bool:
        """Getter function for active.
        Returns True if the product is active, otherwise False."""
        return self.__active

    def activate(self):
        """Activates the product."""
        self.__active = True

    def deactivate(self):
        """Deactivates the product."""
        self.__active = False

    def show(self):
        """Prints a string that represents the product, for example:
        "MacBook Air M2, Price: 1450, Quantity: 100" """
        return(f"{self._name}, Price: {self._price:.2f}, Quantity: {self._quantity}")

    def buy(self, quantity) -> float:
        """Buys a given quantity of the product.
        Returns the total price (float) of the purchase.
        Updates the quantity of the product.
        In case of a problem it raises an Exception."""
        if self._quantity < quantity:
            raise ProductUnavailable(
                "Not enough quantity available for "
                f"product {self._name}. Only {self._quantity} items available"
            )
        if self.__active == False:
            raise ProductUnavailable(
                "Sorry, product can not be purchased. Product is not active")
        self._quantity -= quantity
        if self._quantity == 0:
            self.__active = False
        return Product.calc_price(self._price, quantity)

class NonStockedProduct(Product):
    def __init__(self, name:str, price:float) -> None:
        super().__init__(name, price,0)

    def set_quantity(self, quantity):
        self._quantity = 0

    def buy(self, quantity)->float:
        if not self.is_active():
            raise ProductUnavailable("Product not available. Product is not active")
        self._quantity = quantity+1
        price = super().buy(quantity)
        self._quantity = 0
        return price

    def show(self):
        return f"{self._name}, Price: {self._price:.2f}, Quantity: unlimited"

class LimitedProduct(Product):
    def __init__(self, name:str, price:float, quantity, maximum):
        self.__max_order_size = maximum
        super().__init__(name, price, quantity)

    def buy(self, quantity:int) -> float:
        if quantity > self.__max_order_size:
            raise ValueError(f"Only {self.__max_order_size} articles per order are allowed for this Product")
        price = super().buy(quantity)
        return price

    def show(self):
        return f"{self._name}, Price: {self._price:.2f}, Quantity: {self._quantity}, Max. order size = {self.__max_order_size}"


def main():
    """
    test code to test the basic functionality for the Product class
    :return:
    """

    # setup initial stock of inventory

    bose = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    mac = Product("MacBook Air M2", price=1450, quantity=100)

    print(bose.buy(50))
    print(mac.buy(100))
    print(mac.is_active())

    print(bose.show())
    print(mac.show())

    bose.set_quantity(1000)
    print(bose.show())


if __name__ == "__main__":
    main()
