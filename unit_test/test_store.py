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
ORIGINAL_PRODUCT_LIST = [
    products.Product(
        "MacBook Air M2", price=1450, quantity=100), products.Product(
            "Bose QuietComfort Earbuds", price=250, quantity=500), products.Product(
                "Google Pixel 7", price=500, quantity=250), products.NonStockedProduct(
                    "Windows License", price=125), products.LimitedProduct(
                        "Shipping", price=10, quantity=250, maximum=1)]


@pytest.fixture
def default_ajax_store():
    default_product_list = [
        products.Product(
            "MacBook Air M2", price=1450, quantity=100), products.Product(
            "Bose QuietComfort Earbuds", price=250, quantity=500), products.Product(
                "Google Pixel 7", price=500, quantity=250), products.NonStockedProduct(
                    "Windows License", price=125), products.LimitedProduct(
                        "Shipping", price=10, quantity=250, maximum=1)]
    ajax_store = store.Store(default_product_list, "AJAX Forever")
    return ajax_store


@pytest.fixture
def discount_ajax_store():
    default_product_list = [
        products.Product(
            "MacBook Air M2", price=1450, quantity=100), products.Product(
            "Bose QuietComfort Earbuds", price=250, quantity=500), products.Product(
                "Google Pixel 7", price=500, quantity=250), products.NonStockedProduct(
                    "Windows License", price=125), products.LimitedProduct(
                        "Shipping", price=10, quantity=250, maximum=1)]
    thirty_percent = promotions.PercentDiscount("30% off!", percent=30)
    second_half_price = promotions.SecondHalfPrice(
        "50% discount on every 2nd product!")
    third_one_free = promotions.ThirdOneFree("Buy 3, pay2!")
    default_product_list[0].set_promotion(thirty_percent)
    default_product_list[1].set_promotion(second_half_price)
    default_product_list[2].set_promotion(third_one_free)
    default_product_list[3].set_promotion(thirty_percent)
    default_product_list[4].set_promotion(thirty_percent)
    ajax_store = store.Store(default_product_list, "AJAX Forever")
    return ajax_store


thirty_percent = promotions.PercentDiscount("30% off!", percent=30)
second_half_price = promotions.SecondHalfPrice(
    "50% discount on every 2nd product!")
third_one_free = promotions.ThirdOneFree("Buy 3, pay2!")
# 1.1


def test_11_store_creation(default_ajax_store):
    default_ajax_store.get_all_products()[3].set_promotion(thirty_percent)
    # best_buy = store.Store(default_product_list, "AJAX Forever")
    assert default_ajax_store.get_store_name() == "AJAX Forever"
    assert default_ajax_store.get_all_products() == ORIGINAL_PRODUCT_LIST
    assert default_ajax_store.get_all_products(
    )[3].get_promotion() == thirty_percent
    assert default_ajax_store.get_total_quantity() == 1100
# 1.2


def test_12_store_creation_with_no_products():
    best_buy = store.Store([], "AJAX Forever")
    assert best_buy.get_store_name() == "AJAX Forever"
    assert best_buy.get_all_products() == []

# 1.3


def test_13_store_creation_with_empty_name():
    with pytest.raises(TypeError, match="Wrong construction of the store! Shop name must be valid."):
        best_buy = store.Store([], "")

# 1.4


def test_14_store_creation_with_invalid_type_for_product_list():
    with pytest.raises(TypeError, match="Wrong construction of the store!"):
        best_buy = store.Store(1, "AJAX Forever")

# 1.5


def test_15_store_creation_with_invalid_type_for_name():
    with pytest.raises(TypeError, match="Wrong construction of the store!"):
        best_buy = store.Store([], 1)

# 2.1


def test_21_buy_product_from_store(default_ajax_store):
    default_ajax_store.get_all_products()[3].set_promotion(thirty_percent)
    price = default_ajax_store.get_all_products()[3].buy(4)
    assert default_ajax_store.get_total_quantity() == 1100
    assert price == (4 * 125) * 0.7
# 2.2


def test_22_buy_product_from_store_that_has_promotion(default_ajax_store):
    default_ajax_store.get_all_products()[3].set_promotion(thirty_percent)
    price = default_ajax_store.get_all_products()[3].buy(4)
    assert default_ajax_store.get_total_quantity() == 1100
    assert price == (4 * 125) * 0.7


# 2.3
"""
Products in the store:
products.Product("MacBook Air M2", price=1450, quantity=100),
products.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
products.Product("Google Pixel 7", price=500, quantity=250),
products.NonStockedProduct("Windows License", price=125),
products.LimitedProduct("Shipping", price=10, quantity=250, maximum=1)
"""


def test_23_buy_product_from_store_via_shopping_list_no_promotion(
        default_ajax_store):
    shopping_list = [(default_ajax_store.get_all_products()[0], 10),
                     (default_ajax_store.get_all_products()[1], 10),
                     (default_ajax_store.get_all_products()[2], 10),
                     (default_ajax_store.get_all_products()[3], 10),
                     (default_ajax_store.get_all_products()[4], 1)
                     ]
    price = default_ajax_store.order(shopping_list)
    assert default_ajax_store.get_total_quantity() == 1100 - 31
    assert price == ((10 * 1450) + (10 * 250) + (10 * 500) + (10 * 125) + 10)


# 2.4
"""
Promotions:
thirty_percent
second_half_price
third_one_free
"""


def test_24_buy_product_with_various_product_promotions(discount_ajax_store):

    shopping_list = [(discount_ajax_store.get_all_products()[0], 10),
                     (discount_ajax_store.get_all_products()[1], 10),
                     (discount_ajax_store.get_all_products()[2], 10),
                     (discount_ajax_store.get_all_products()[3], 10),
                     (discount_ajax_store.get_all_products()[4], 1)
                     ]
    price = discount_ajax_store.order(shopping_list)
    assert discount_ajax_store.get_total_quantity() == 1100 - 31 - 5
    assert price == (10 * 1450 * 0.7) + (5 * 250 + 5 * 125) + \
        (7 * 500) + (10 * 125 * 0.7) + 10 * .7
# 2.5


def test_25_buy_product_from_store_via_empty_shopping_list1(
        default_ajax_store):
    shopping_list = []
    with pytest.raises(TypeError, match=r"Shopping list must be a list of '\(product, quantity\)' pairs"):
        price = default_ajax_store.order(shopping_list)
# 2.6


def test_26_buy_product_from_store_via_empty_shopping_list2(
        default_ajax_store):
    shopping_list = [()]
    with pytest.raises(TypeError, match=r"Shopping list must be a list of '\(product, quantity\)' pairs"):
        price = default_ajax_store.order(shopping_list)
# 2.7


def test_27_buy_product_from_store_via_error_shopping_list3(
        default_ajax_store):
    shopping_list = 4
    with pytest.raises(TypeError, match=r"Shopping list must be a list of '\(product, quantity\)' pairs"):
        price = default_ajax_store.order(shopping_list)
# 2.8


def test_28_buy_product_from_store_via_error_shopping_list3(
        default_ajax_store):
    shopping_list = [("hello", 4)]
    with pytest.raises(TypeError, match=r"Shopping list must be a list of '\(product, quantity\)' pairs"):
        price = default_ajax_store.order(shopping_list)

# 2.9


def test_29_buy_product_from_store_via_error_shopping_list4(
        default_ajax_store):
    shopping_list = [(default_ajax_store.get_all_products()[0], "hello")]
    with pytest.raises(TypeError, match=r"Shopping list must be a list of '\(product, quantity\)' pairs"):
        price = default_ajax_store.order(shopping_list)

# 2.10


def test_210_buy_product_from_store_via_error_shopping_list5(
        default_ajax_store):
    shopping_list = [
        (default_ajax_store.get_all_products()[0], 10), ("hello", 10)]
    with pytest.raises(TypeError, match=r"Shopping list must be a list of '\(product, quantity\)' pairs"):
        price = default_ajax_store.order(shopping_list)
# 3.1


def test_31_product_in_store(default_ajax_store):
    assert ("Mac" in default_ajax_store)
    assert ("Earbuds" in default_ajax_store)
    assert ("xxxyyy" in default_ajax_store) == False
