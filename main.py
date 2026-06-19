import sys
import os
import subprocess
import store
import products
import promotions


def clear_screen():
    """
    Clean the screen before showing the menu. Does not seem to work well though on this terminal
    """
    if os.name == "nt":
        subprocess.run("cls")
    else:
        # fallback if TERM not set
        if "TERM" in os.environ:
            subprocess.run("clear")
        else:
            print("\n" * 100)


def command_quit(the_store):
    """
    quits the application
    :return:
    """
    sys.exit()


def print_all_products(the_store):
    """
    prints all the available products from the store.
    :param the_store:
    :return:
    """
    the_store.print_all_products()


def print_total_quantity(the_store):
    """
    initiates the printing of the total items in the store
    :param the_store:
    :return:
    """
    the_store.print_total_quantity()


def order_from_store(the_store):
    """
    Get all the relevant input from the user to generate an order list
    and to create the order to the store.
    Prints the price to pay for the order
    :param the_store:
    :return:
    """
    all_products = the_store.get_all_products()
    choice = 0
    for product in all_products:
        choice += 1
        print(f"{choice}. ", end="")
        print(product.show())
    order_list = []
    while True:
        print("When you want to finish order, enter empty text.")
        order_product = input("Which product # do you want? ")
        if len(order_product) == 0:  # break when empty text is provided
            break
        try:
            order_product = int(order_product)
            if not 1 <= order_product <= choice:
                raise ValueError
            order_product = all_products[(order_product - 1)]
            order_quantity = input("What amount do you want? ")
            if len(order_quantity) == 0:  # break when empty text is provided
                break
            order_quantity = int(order_quantity)
            order_list.append((order_product, order_quantity))
        except (TypeError, ValueError):
            print("Please enter a valid choice!")
    try:
        print(f"Order made! Total payment: {the_store.order(order_list)}")
    except store.NotInStore as e:
        print("Could not create order: ",e)
    # input("\nPress enter to continue")


def start():
    """Responsible for displaying the menu and ensure correct input
    for menu choices from the user"""

    #
    # Function Dispatch Dictionary:
    #
    functions = {
        1: (print_all_products, "List all products in store"),
        2: (print_total_quantity, "Show total amount in store"),
        3: (order_from_store, "Make an order"),
        4: (command_quit, "Exit"),
    }
    while True:
        clear_screen()  # clears the screen
        # print(f"Welcome to {the_store.get_name()}!")
        print("** ** ** ** ** Store Menu ** ** ** ** ** \n\n")
        for number, function in functions.items():
            print(f"{number} - {function[1]}")
        try:
            user_choice = int(input("Enter choice(0 - 4): "))
            if user_choice in functions:
                return functions[user_choice][0]
        except (TypeError, ValueError):
            print("Please enter a valid choice!")


def main():
    """
    Responsible for construction the store with a predefined product list and for initiating the menu.
    :return: -
    """
    # setup initial stock of inventory
    product_list = [products.Product("MacBook Air M2", price=1450, quantity=100),
                    products.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
                    products.Product("Google Pixel 7", price=500, quantity=250),
                    products.NonStockedProduct("Windows License", price=125),
                    products.LimitedProduct("Shipping", price=10, quantity=250, maximum=1)
                    ]

    # Create promotion catalog
    second_half_price = promotions.SecondHalfPrice("Second Half price!")
    third_one_free = promotions.ThirdOneFree("Third One Free!")
    thirty_percent = promotions.PercentDiscount("30% off!", percent=30)

    # Add promotions to products
    product_list[0].set_promotion(second_half_price)
    product_list[1].set_promotion(third_one_free)
    product_list[3].set_promotion(thirty_percent)

    best_buy = store.Store(product_list, "BEST BUY!!!")
    while True:
        menu_selection = start()
        menu_selection(best_buy)
        input("\nPress enter to continue")


if __name__ == "__main__":
    main()
