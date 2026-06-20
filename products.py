from promotions import Promotion, ThirdOneFree


class ProductUnavailable(Exception):
    """
    Exception definition for when product or not enough product quantity is available
    """

    # pass


class Product:
    """
    Definition for the product class
    """

    @staticmethod
    def calc_price(price: float, quantity: int) -> float:
        """
        Just fooling around with static methods
        """
        return price * quantity

    def __init__(self, name: str, price: float, quantity: int) -> None:
        if len(name) == 0:
            raise ValueError("Product name can not be empty")
        self._name = name
        if not isinstance(price, (float, int)):
            raise ValueError("Please ensure price is valid")
        if price < 0:
            raise ValueError("Please ensure price is valid")
        self._price = price
        if not isinstance(quantity, int):
            raise ValueError("Please ensure quantity is a valid number")
        if quantity < 0:
            raise ValueError("Please ensure quantity is a valid number")
        self._quantity: int = quantity
        self._promotion = None
        self._active = True

    def __gt__(self, other) -> bool:
        return self.get_price() > other.get_price()

    def __lt__(self, other) -> bool:
        return self.get_price() < other.get_price()

    def __eq__(self, other: Product) -> bool:
        return self.get_price() == other.get_price()

    def get_quantity(self) -> int:
        """Getter function for quantity.
        Returns the quantity (int)."""
        return self._quantity

    def set_quantity(self, quantity: int) -> None:
        """Setter function for quantity. If quantity reaches 0, deactivates the product."""
        self._quantity = quantity
        if quantity == 0:
            self._active = True

    def get_name(self) -> str:
        """Return the product name."""
        return self._name

    def set_name(self, new_name: str):
        """Setter function for product name."""
        if len(new_name) == 0:
            raise ValueError("Please ensure the new name is valid")
        self._name = new_name

    def get_price(self) -> float:
        """Getter function for price."""
        return self._price

    def set_promotion(self, promotion: Promotion) -> bool:
        """Setter function for promotion."""
        if not promotion.is_active():
            self._promotion = None
            return False
        if self._quantity > promotion.get_minimum_quantity():
            self._promotion = promotion
            return True
        return False

    def remove_promotion(self):
        """Removes a promotion"""
        self._promotion = None

    def get_promotion(self):
        """Getter function for promotion."""
        if self._promotion is None:
            return None
        if not self._promotion.is_active():
            self.remove_promotion()
        return self._promotion

    def set_price(self, new_price: float):
        """Setter function for price."""
        try:
            self._price: float = new_price
        except ValueError as e:
            raise ValueError("Please ensure price is a valid price") from e

    def is_active(self) -> bool:
        """Getter function for active.
        Returns True if the product is active, otherwise False."""
        return self._active

    def activate(self):
        """Activates the product."""
        self._active = True

    def deactivate(self):
        """Deactivates the product."""
        self._active = False

    def show(self):
        """returns a string that represents the product, for example:
        "MacBook Air M2, Price: 1450, Quantity: 100" """
        if self._promotion:
            if self._promotion.is_active():
                return f"{
                    self._name}, Price: {
                    self._price:.2f}, Quantity: {
                    self._quantity}, Promotion: {
                    self._promotion}"
        return f"{
            self._name}, Price: {
            self._price:.2f}, Quantity: {
            self._quantity}"

    def __str__(self) -> str:
        return self.show()

    def buy(self, buy_quantity) -> float:
        """Buys a given quantity of the product.
        Returns the total price (float) of the purchase.
        Updates the quantity of the product.
        In case of a problem it raises an Exception."""
        receive_quantity = buy_quantity
        if isinstance(self._promotion, ThirdOneFree):
            # stock needs extra products in case of the promotion, buy 2, get 3
            receive_quantity += buy_quantity // 2
        if self._quantity < receive_quantity:
            raise ProductUnavailable(
                "Not enough quantity available for "
                f"product {self._name}. Only {self._quantity} items available"
            )
        if not self._active:
            raise ProductUnavailable(
                "Sorry, product can not be purchased. Product is not active"
            )
        # Everything ready for buying the product
        self._quantity -= receive_quantity
        if self._quantity == 0:
            self._active = False
        if self.get_promotion():
            price = self._promotion.calc_price(self._price, buy_quantity)
            if self._quantity <= self._promotion.get_minimum_quantity():
                self.remove_promotion()
        else:
            # print("no promo", self._price, buy_quantity)
            price = self.calc_price(self._price, buy_quantity)

        return price


class NonStockedProduct(Product):
    """Non-Stocked Product. Extension of Product"""

    def __init__(self, name: str, price: float) -> None:
        super().__init__(name, price, 0)

    def set_quantity(self, quantity):
        self._quantity = 0

    def buy(self, buy_quantity) -> float:
        if not self.is_active():
            raise ProductUnavailable("Product not available. Product is not active")
        # make sure there is enough in the non-existing stack.
        self._quantity = buy_quantity * 2
        price = super().buy(buy_quantity)
        self._quantity = 0
        return price

    def set_promotion(self, promotion: Promotion) -> bool:
        self._promotion = promotion
        return True

    def show(self):
        promotion = self.get_promotion()
        if promotion:
            if promotion.is_active():
                return f"{
                    self._name}, Price: {
                    self._price:.2f}, Quantity: unlimited, Promotion: {promotion}"
        return f"{self._name}, Price: {self._price:.2f}, Quantity: unlimited"

    def __str__(self):
        return self.show()


class LimitedProduct(Product):
    """Limited Product. Extension of Product"""

    def __init__(self, name: str, price: float, quantity, maximum):
        self.__max_order_size = maximum
        super().__init__(name, price, quantity)

    def buy(self, buy_quantity: int) -> float:
        if buy_quantity > self.__max_order_size:
            raise ValueError(
                f"Only {
                    self.__max_order_size} articles per order are allowed for this Product"
            )
        price = super().buy(buy_quantity)
        return price

    def set_promotion(self, promotion: Promotion) -> bool:
        if promotion.get_minimum_quantity() > self.__max_order_size:
            return False
        super().set_promotion(promotion)
        return True

    def show(self):
        promotion = self.get_promotion()
        if promotion:
            if promotion.is_active():
                return f"{
                    self._name}, Price: {
                    self._price:.2f}, Quantity: {
                    self._quantity}, Max. order size = {
                    self.__max_order_size}, Promotion: {promotion}"
        return f"{
            self._name}, Price: {
            self._price:.2f}, Quantity: {
            self._quantity}, Max. order size = {
                self.__max_order_size}"

    def __str__(self):
        return self.show()


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
