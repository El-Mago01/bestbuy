import products


class NotInStore(Exception):
    """
    Exception definition for when product or not enough product quantity is available
    """

    pass


class Store:
    """
    Definition for the Store class
    """

    def __init__(self, product_list, name):
        self.name = name
        self.product_list = product_list

    def get_store_name(self):
        """returns the name of the store"""
        return self.name

    def add_product(self, product):
        """add a product to the product list"""
        self.product_list.append(product)

    def remove_product(self, product):
        """Removes a product from store."""
        self.product_list.remove(product)

    def get_total_quantity(self) -> int:
        """Returns how many items are in the store in total."""
        total_items = 0
        for product in self.product_list:
            total_items += product.get_quantity()
        return total_items

    def print_total_quantity(self) -> int:
        """Returns how many items are in the store in total."""
        print(
            f"There are currently {
                self.get_total_quantity()} items in the store")

    def get_all_products(self) -> list:
        """Returns all products in the store that are active."""
        active_products = []
        for product in self.product_list:
            if product.is_active():
                active_products.append(product)
        return active_products

    def print_all_products(self):
        """
        print all the available products in the store according to requirements
        :return:
        """
        active_prods = self.get_all_products()
        for product in active_prods:
            print(product.show())

    def order(self, shopping_list) -> float:
        """Gets a list of tuples, where each tuple has 2 items:
        Product (Product class) and quantity (int).
        Buys the products and returns the total price of the order."""
        sales = 0
        for product_list_item, quantity in shopping_list:
            try:
                sales += product_list_item.buy(quantity)
            except products.ProductUnavailable as e:
                raise NotInStore("Product not available. ") from e
        return sales


def main():
    """
    Some initial testing of the store
    :return:
    """
    product_list = [products.Product("MacBook Air M2", price=1450, quantity=100),
                    products.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
                    products.Product("Google Pixel 7", price=500, quantity=250),
                    products.NonStockedProduct("Windows License", price=125),
                    products.LimitedProduct("Shipping", price=10, quantity=250, maximum=1)
                    ]

    best_buy = Store(product_list, "BEST BUY")
    all_products = best_buy.get_all_products()
    for product in all_products:
        product.show()
    print(best_buy.get_total_quantity())
    print(best_buy.order([(all_products[0], 1), (all_products[1], 2)]))
    all_products = best_buy.get_all_products()
    for product in all_products:
        product.show()


if __name__ == "__main__":
    main()
