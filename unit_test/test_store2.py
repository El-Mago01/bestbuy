import pytest
import store
import products
import promotions

"""
1.  Test creation of the store
1.1 Test creation of the store with correct name and default product list
1.2 Test creation of the store with correct name and empty product list
1.3 Test creation of the store with empty str as name and default product list
1.4 Test creation of store with default values and setting of a promotion

2.  Test buying of a product in the store
2.1 Buy a product in the store
2.2 Buy a product in the store with a promotion
2.3 Buy the last product available in the store


3.  Check Product availability
3.1 Check if Product A is in the store
3.2 Check if Product B is in the store with a promotion

4.  Remove a product from the store
"""

default_product_list = [products.Product("MacBook Air M2", price=1450, quantity=100),
                    products.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
                    products.Product("Google Pixel 7", price=500, quantity=250),
                    products.NonStockedProduct("Windows License", price=125),
                    products.LimitedProduct("Shipping", price=10, quantity=250, maximum=1)
                    ]

thirty_percent = promotions.PercentDiscount("30% off!", percent=30)
second_half_price = promotions.SecondHalfPrice("50% discount on every 2nd product!")
third_one_free = promotions.ThirdOneFree("Buy 3, pay2!")
# #2.2
# def test_22_buy_product_from_store_that_has_promotion():
#     default_product_list[3].set_promotion(thirty_percent)
#     best_buy = store.Store(default_product_list, "AJAX Forever")
#     price = best_buy.get_all_products()[3].buy(4)
#     assert best_buy.get_total_quantity() == 1100
#     assert price == (4 * 125) * 0.7
# # 2.3
"""
Products in the store:
products.Product("MacBook Air M2", price=1450, quantity=100),
products.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
products.Product("Google Pixel 7", price=500, quantity=250),
products.NonStockedProduct("Windows License", price=125),
products.LimitedProduct("Shipping", price=10, quantity=250, maximum=1)
"""

def test_22_buy_product_from_store_via_shopping_list_no_promotion():
    default_product_list = [products.Product("MacBook Air M2", price=1450, quantity=100),
                            products.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
                            products.Product("Google Pixel 7", price=500, quantity=250),
                            products.NonStockedProduct("Windows License", price=125),
                            products.LimitedProduct("Shipping", price=10, quantity=250, maximum=1)
                            ]
    best_buy = store.Store(default_product_list, "AJAX Forever")
    shopping_list = [(best_buy.get_all_products()[0], 10),
                     (best_buy.get_all_products()[1], 10),
                     (best_buy.get_all_products()[2], 10),
                     (best_buy.get_all_products()[3], 10),
                     (best_buy.get_all_products()[4], 1)
                     ]
    price = best_buy.order(shopping_list)
    assert best_buy.get_total_quantity() == 1100 - 31
    assert price == ((10*1450) + (10*250) + (10*500) + (10*125) + 10)


def test_23_buy_product_from_store_via_shopping_list_no_promotion():
    default_product_list = [products.Product("MacBook Air M2", price=1450, quantity=100),
                            products.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
                            products.Product("Google Pixel 7", price=500, quantity=250),
                            products.NonStockedProduct("Windows License", price=125),
                            products.LimitedProduct("Shipping", price=10, quantity=250, maximum=1)
                            ]
    best_buy = store.Store(default_product_list, "AJAX Forever")
    shopping_list = [(best_buy.get_all_products()[0], 10),
                     (best_buy.get_all_products()[1], 10),
                     (best_buy.get_all_products()[2], 10),
                     (best_buy.get_all_products()[3], 10),
                     (best_buy.get_all_products()[4], 1)
                     ]
    price = best_buy.order(shopping_list)
    assert best_buy.get_total_quantity() == 1100 - 31
    assert price == ((10*1450) + (10*250) + (10*500) + (10*125) + 10)
#2.4
"""
Promotions:
thirty_percent 
second_half_price 
third_one_free 
"""

# 2.5
