class ProductUnavailable(Exception):
    pass

class Product:
    @staticmethod
    def calc_price(price, quantity)-> float:
        return price * quantity

    def __init__(self, name, price, quantity):
        if len(name) == 0:
            raise ValueError ("Product name can not be empty")
        self.name = name
        try:
            self.price = price
            self.quantity = quantity
        except ValueError as e:
            raise ValueError (f"Please ensure price is a value in $ and quantity is a number")
        self.active = True

    def get_quantity(self) -> int:
        """Getter function for quantity.
        Returns the quantity (int)."""
        return self.quantity

    def set_quantity(self, quantity):
        """Setter function for quantity. If quantity reaches 0, deactivates the product.
        """
        self.quantity = quantity
        if quantity == 0:
            self.active = True

    def is_active(self) -> bool:
        """Getter function for active.
        Returns True if the product is active, otherwise False."""
        return self.active

    def activate(self):
        """Activates the product."""
        self.active = True

    def deactivate(self):
        """Deactivates the product."""
        self.active = False

    def show(self):
        """Prints a string that represents the product, for example:
        "MacBook Air M2, Price: 1450, Quantity: 100" """
        print(f"{self.name}, Price: {self.price}, Quantity: {self.quantity}")

    def buy(self, quantity) -> float:
        """Buys a given quantity of the product.
         Returns the total price (float) of the purchase.
         Updates the quantity of the product.
         In case of a problem it raises an Exception."""
        if self.quantity < quantity:
            raise ProductUnavailable ("Not enough quantity available for "
                f"product {self.product}. Only {self.quantity} items available")
        self.quantity -= quantity
        return Product.calc_price(self.price, quantity)


def main():
    bose = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    mac = Product("MacBook Air M2", price=1450, quantity=100)

    print(bose.buy(50))
    print(mac.buy(100))
    print(mac.is_active())

    bose.show()
    mac.show()

    bose.set_quantity(1000)
    bose.show()

if __name__ == "__main__":
    main()


