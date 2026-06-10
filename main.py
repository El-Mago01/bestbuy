import store
import products
import sys
import os
import subprocess

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


def command_quit():
    """
    quits the application
    :return:
    """
    sys.exit()


def print_all_products(the_store):
    the_store.print_all_products()

def print_total_quantity(the_store):
    the_store.print_total_quantity()

def order_from_store(the_store):
    all_products = the_store.get_all_products()
    choice = 0
    for product in all_products:
        choice += 1
        print(f"{choice}. {product.name}, Price: {product.price}, Quantity: {product.quantity}")
    order_list = []
    while True:
        print("When you want to finish order, enter empty text.")
        order_product = input("Which product # do you want? ")
        if len(order_product) == 0: # break when empty text is provided
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
    print(f"Order made! Total payment: {the_store.order(order_list)}")
    # input("\nPress enter to continue")

def start(the_store):
    """
    Function Dispatch Dictionary
    """
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
    # setup initial stock of inventory
    product_list = [products.Product("MacBook Air M2", price=1450, quantity=100),
                    products.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
                    products.Product("Google Pixel 7", price=500, quantity=250)
                    ]
    best_buy = store.Store(product_list, "BEST BUY!!!")
    while True:
        menu_selection = start(best_buy)
        menu_selection(best_buy)
        input("\nPress enter to continue")


if __name__ == "__main__":
    main()