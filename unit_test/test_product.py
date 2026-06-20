"""
Product testables:
1.      Creating a new Product
1.1     Creating a new Product with a name, price and quantity successfully
        -   the correct show is provided
        -   product is activated
        -   total of available products correctly increased
1.2     Create a new Product with an empty name
        -   check correct assertion
        -   check that the number of total products did not increase
1.3     Create a new Product with a string for price
        -   check ValueError is raised
        -   check that no new product is created
1.4     Create a new Product with a float for quantity
        -   test ValueError is raised
1.5     Create a new Product with a negative price
        -   test ValueError is raised
1.6     Create a new Product with a negative quantity
        -   test ValueError is raised

1.7     Create a new NonStockedProduct with name, price
        -   the correct show is provided
        -   product is activated
        -   total of available products correctly increased

2.      Deactivating a Product
2.1     Deactivate a product by deactivate the Product
        -   check product is deactivated
        -   check that the product still exist with the correct price and quantity
2.2     Deactivate a product by removing reducing the quantities to 0
        -   check that the product is deactivated
        -   check that the product has now quantity 0
        -   check that the price remained the same
2.3     Deactivate illegally.
        Deactivate the product by directly assessing the Product variable
        -   Check that the product is still activated
        -   the correct show is provided
        -   product is activated
        -   total of available products correctly increased

3.      Buying products
3.1     Buy an active product with an available quantity
        -   check the right price
        -   check available quantity is reduced correctly
        -   check that the product remains active

3.2     Buy an active product where the quantity is too high
        -   check the right assertion
        -   check that the available quantity is not reduced
        -   check that the product remains active

3.3     Buy one active NonStockedProduct successfully
        -   check that the quantity remains 0
        -   check that the is_active remains True
        -   check that the right price is calculated


3.4     Buy 5 NonStockedProducts successfully
        -   check that the quantity remains 0
        -   check that the is_active remains True
        -   check that the right price is calculated


3.5     Buy an active LimitedProduct successfully, with maximum quantity
        -   check that the quantity remains 0
        -   check that the is_active remains True
        -   check that the right price is calculated

3.6     Buy too many LimitedPRoducts. I.e. more than the maximum quantity
        -   check the right assertion
        -   check that the available quantity is not reduced
        -   check that the product remains active


4       Promotions
4.1     setting and activating of a promotion for a normal product
        -   Check that the promotion is indeed set in the printout of the product
        -   Check that the promotion is active
        -   buy a product, check that the promotion is calculated for the price

4.2     setting and activating of a promotion for a non-stocked product
        -   Check that the promotion is indeed set in the printout of the product
        -   Check that the promotion is active
        -   buy a product, check that the promotion is calculated for the price

4.3     setting and activating of a promotion for a limited product
        -   Check that the promotion is indeed set in the printout of the product
        -   Check that the promotion is active
        -   buy a product, check that the promotion is calculated for the price

4.4     Removing a promotion

4.4     Changing a promotion

4.4     Deactivating a promotion

5       Buy normal product with promotion
5.1     Buy normal product with promotion, for buy 3, pay 2 promotion.
        remove promotion and buy it again
        - check correct prices
        - check activation and removal
        -

5.2     Buy normal product, for 2nd half price promotion
        deactivate promotion and buy it again.
        - check correct prices
        - check activation and deactivation

5.3     Buy normal product, for x percent off promotion
        deactivate promotion and buy it again.
        - check correct prices

        Repeat 5.1, 5.2 and 5.3 for the 2 other product types

6.      Testing magic methods
6.1     Check Product A > Product B
6.2     Check Product A < Product B

"""
import pytest
from products import Product, ProductUnavailable, LimitedProduct, NonStockedProduct
import promotions
# 1.1


def test_create_new_product():
    prod = Product("test product", 100.00, 50)
    assert prod.is_active()
    assert prod.show() == "test product, Price: 100.00, Quantity: 50"
    assert prod.get_quantity() == 50

# 1.2


def test_create_new_product_empty_name():
    with pytest.raises(ValueError, match="Product name can not be empty"):
        prod = Product("", 100, 50)

# 1.3


def test_create_with_price_as_string():
    with pytest.raises(ValueError, match="Please ensure price is valid"):
        prod = Product("test product", "100", 50)

# 1.4


def test_create_with_quantity_as_float():
    with pytest.raises(ValueError, match="Please ensure quantity is a valid number"):
        prod = Product("test product", 100, 50.0)

# 1.5


def test_create_product_with_negative_price():
    with pytest.raises(ValueError, match="Please ensure price is valid"):
        prod = Product("test product", -100, 50)

# 1.6


def test_create_product_with_negative_quantity():
    with pytest.raises(ValueError, match="Please ensure quantity is a valid number"):
        prod = Product("test product", 100, -50)

# 1.7


def test_create_new_nonstockedproduct():
    prod = NonStockedProduct("test product", 100.00)
    assert prod.is_active()
    assert prod.show() == "test product, Price: 100.00, Quantity: unlimited"
    assert prod.get_quantity() == 0

# 1.8


def test_create_new_limitedproduct():
    prod = LimitedProduct("test product", 100.00, 50, 1)
    assert prod.is_active()
    assert prod.show() == "test product, Price: 100.00, Quantity: 50, Max. order size = 1"
    assert prod.get_quantity() == 50

# 2.1


def test_deactivate_by_deactivating():
    prod = Product("Test Product", 100, 50)
    assert prod.is_active()
    prod.deactivate()
    assert prod.is_active() == False
    assert prod.get_price() == 100
    assert prod.get_quantity() == 50

# 2.2


def test_deactivate_by_0_quantity():
    prod = Product("Test Product", 100, 50)
    assert prod.is_active()
    assert prod.get_quantity() == 50
    price = prod.buy(50)
    assert price == 50 * 100
    assert prod.is_active() == False
    assert prod.get_price() == 100
    assert prod.get_quantity() == 0

# 2.3


def test_illegal_deactivation():
    prod = Product("test product", 100, 50)
    prod.__activate = False
    assert prod.is_active()

# 3.1


def test_buy_product():
    prod = Product("test product", 100, 50)
    price = prod.buy(10)
    assert price == 10 * 100
    assert prod.get_quantity() == 40
    assert prod.is_active()

# 3.2


def test_buy_product_quantity_too_high():
    prod = Product("test product", price=100.00, quantity=50)
    with pytest.raises(ProductUnavailable, match="Not enough quantity available"):
        price = prod.buy(51)
    assert prod.is_active()
    assert prod.get_quantity() == 50

# 3.3


def test_buy_nonsstockedproduct():
    prod = NonStockedProduct("test product", 100)
    price = prod.buy(1)
    assert price == 1 * 100
    assert prod.get_quantity() == 0
    assert prod.is_active()

# 3.4


def test_buy_nonsstockedproduct_5_elements():
    prod = NonStockedProduct("test product", 100)
    price = prod.buy(5)
    assert price == 5 * 100
    assert prod.get_quantity() == 0
    assert prod.is_active()

# 3.5


def test_buy_limitedproduct_at_maximum():
    prod = LimitedProduct("test product", 100, quantity=2, maximum=2)
    price = prod.buy(2)
    assert price == 2 * 100
    assert prod.get_quantity() == 0
    assert prod.is_active() == False

# 3.6


def test_buy_limitedproduct_over_maximum():
    prod = LimitedProduct("test product", 100, quantity=3, maximum=2)
    with pytest.raises(ValueError, match="^Only 2 articles per order are allowed for this Product"):
        price = prod.buy(3)
    assert prod.is_active()

# 4.1


def test_set_percentage_discount_for_normal_product():
    prod1 = Product("Test Normal Product", price=100.00, quantity=50)
    promo1 = promotions.PercentDiscount("Now 20% off!", percent=20)
    prod1.set_promotion(promo1)
    assert prod1.show() == "Test Normal Product, Price: 100.00, Quantity: 50, Promotion: Now 20% off!"
    assert prod1.get_quantity() == 50
    assert prod1.is_active()
    assert prod1.get_price() == 100
    assert promo1.is_active()
# 4.2


def test_set_third_one_free_discount_for_non_stocked_product():
    prod2 = NonStockedProduct("Test Non Stocked Product", 100)
    promo2 = promotions.ThirdOneFree("Pay 2, bring home 3!")
    prod2.set_promotion(promo2)
    assert prod2.show() == "Test Non Stocked Product, Price: 100.00, Quantity: unlimited, Promotion: Pay 2, bring home 3!"
    assert prod2.get_quantity() == 0
    assert prod2.is_active()
    assert prod2.get_price() == 100
    assert promo2.is_active()
# 4.3


def test_set_percent_discount_for_limited_product():
    prod3 = LimitedProduct("test limited product", 100, quantity=2, maximum=2)
    promo3 = promotions.SecondHalfPrice("2nd for half price! Now!")
    prod3.set_promotion(promo3)
    assert prod3.show() == "test limited product, Price: 100.00, Quantity: 2, Max. order size = 2, Promotion: 2nd for half price! Now!"
    assert prod3.get_quantity() == 2
    assert prod3.is_active()
    assert prod3.get_price() == 100
    assert promo3.is_active()

# 4.4


def test_remove_percent_discount_for_limited_product():
    prod3 = LimitedProduct("test limited product", 100, quantity=2, maximum=2)
    promo3 = promotions.SecondHalfPrice("2nd for half price! Now!")
    prod3.set_promotion(promo3)
    assert prod3.show() == "test limited product, Price: 100.00, Quantity: 2, Max. order size = 2, Promotion: 2nd for half price! Now!"
    assert prod3.get_quantity() == 2
    assert prod3.is_active()
    assert prod3.get_price() == 100
    assert promo3.is_active()
    prod3.remove_promotion()
    assert prod3.is_active()
    assert promo3.is_active()
    assert prod3.show() == "test limited product, Price: 100.00, Quantity: 2, Max. order size = 2"
# 5.1


def test_buy_normal_product_with_promotion1():
    prod = Product("Test Normal Product", price=100, quantity=5)
    promo = promotions.ThirdOneFree("Pay 2, bring home 3!")
    prod.set_promotion(promo)
    price = prod.buy(2)
    assert prod.get_quantity() == 2
    assert prod.is_active()
    assert prod.get_promotion() is promo
    assert price == 2 * 100
    prod.remove_promotion()
    price = prod.buy(2)
    assert prod.get_quantity() == 0
    assert prod.is_active() == False
    assert prod.get_promotion() is None
    assert price == 2 * 100
# 5.2


def test_buy_normal_product_with_promotion2():
    prod = Product("Test Normal Product", price=100, quantity=6)
    promo = promotions.SecondHalfPrice("Second for half price! Now!")
    prod.set_promotion(promo)
    price = prod.buy(4)
    assert prod.get_quantity() == 2
    assert prod.is_active()
    assert prod.get_promotion() is promo
    assert price == 4 * 100 - (2 * .5 * 100)
    prod.remove_promotion()
    price = prod.buy(2)
    assert prod.get_quantity() == 0
    assert prod.is_active() == False
    assert prod.get_promotion() is None
    assert price == 2 * 100
# 5.3


def test_buy_normal_product_with_promotion3():
    prod = Product("Test Normal Product", price=100, quantity=8)
    promo = promotions.PercentDiscount("20% Off!! Buy Now. Limited action", 20)
    prod.set_promotion(promo)
    price = prod.buy(4)
    assert prod.get_quantity() == 4
    assert prod.is_active()
    assert prod.get_promotion() is promo
    assert price == (1 * 100 - 0.2 * 100) * 4
    prod.remove_promotion()
    price = prod.buy(2)
    assert prod.get_quantity() == 2
    assert prod.is_active()
    assert prod.get_promotion() is None
    assert price == 2 * 100
# 5.4


def test_buy_non_stocked_product_with_promotion1():
    prod = NonStockedProduct("Test Normal Product", price=100)
    promo = promotions.ThirdOneFree("Pay 2, bring home 3!")
    prod.set_promotion(promo)
    price = prod.buy(2)
    assert prod.get_quantity() == 0
    assert prod.is_active()
    assert prod.get_promotion() is promo
    assert price == 2 * 100
    promo.deactivate()
    price = prod.buy(2)
    assert prod.get_quantity() == 0
    assert prod.is_active()
    assert prod.get_promotion() is None
    assert price == 2 * 100
# 5.5


def test_buy_non_stocked_product_with_promotion2():
    prod = NonStockedProduct("Test Normal Product", price=100)
    promo = promotions.SecondHalfPrice("Second for half price! Now!")
    prod.set_promotion(promo)
    price = prod.buy(4)
    assert prod.get_quantity() == 0
    assert prod.is_active()
    assert prod.get_promotion() is promo
    assert price == 4 * 100 - (2 * .5 * 100)
    promo.deactivate()
    price = prod.buy(2)
    assert prod.get_quantity() == 0
    assert prod.is_active()
    assert prod.get_promotion() is None
    assert price == 2 * 100
# 5.6


def test_buy_non_stocked_product_with_promotion3():
    prod = NonStockedProduct("Test Normal Product", price=100)
    promo = promotions.PercentDiscount("20% Off!! Buy Now. Limited action", 20)
    prod.set_promotion(promo)
    price = prod.buy(4)
    assert prod.get_quantity() == 0
    assert prod.is_active()
    assert prod.get_promotion() is promo
    assert price == (1 * 100 - 0.2 * 100) * 4
    promo.deactivate()
    price = prod.buy(2)
    assert prod.get_quantity() == 0
    assert prod.is_active()
    assert prod.get_promotion() is None
    assert price == 2 * 100
# 5.7


def test_buy_limited_product_with_promotion1():
    prod = LimitedProduct(
        "Test Normal Product",
        price=100,
        quantity=3,
        maximum=2)
    promo = promotions.ThirdOneFree("Pay 2, bring home 3!")
    prod.set_promotion(promo)
    price = prod.buy(2)
    assert prod.get_quantity() == 0
    assert prod.is_active() == False
    assert prod.get_promotion() is None
    assert price == 2 * 100

# 5.8


def test_buy_limited_product_with_promotion2():
    prod = LimitedProduct(
        "Test Normal Product",
        price=100,
        quantity=5,
        maximum=2)
    promo = promotions.SecondHalfPrice("Second for half price! Now!")
    prod.set_promotion(promo)
    price = prod.buy(2)
    assert prod.get_quantity() == 3
    assert prod.is_active()
    assert prod.get_promotion() is promo
    assert price == 2 * 100 - (1 * .5 * 100)
    promo.deactivate()
    price = prod.buy(2)
    assert prod.get_quantity() == 1
    assert prod.is_active()
    assert prod.get_promotion() is None
    assert price == 2 * 100
# 5.9


def test_buy_limited_product_with_promotion3():
    prod = LimitedProduct(
        "Test Normal Product",
        price=100,
        quantity=6,
        maximum=4)
    promo = promotions.PercentDiscount("20% Off!! Buy Now. Limited action", 20)
    prod.set_promotion(promo)
    price = prod.buy(4)
    assert prod.get_quantity() == 2
    assert prod.is_active()
    assert prod.get_promotion() is promo
    assert price == (1 * 100 - 0.2 * 100) * 4
    promo.deactivate()
    price = prod.buy(2)
    assert prod.get_quantity() == 0
    assert prod.is_active() == False
    assert prod.get_promotion() is None
    assert price == 2 * 100

# 6.1 Check if product a > product b is working


def test_product_a_gt_product_b():
    prod_a = Product("Normal Product", price=100.00, quantity=2)
    prod_b = Product("Other Normal Product", price=100.01, quantity=2)
    assert (prod_a > prod_b) == False
    assert (prod_a < prod_b)
    assert (prod_a == prod_b) == False


def test_product_a_lt_product_b():
    prod_a = Product("Normal Product", price=100.01, quantity=2)
    prod_b = Product("Other Normal Product", price=100.00, quantity=2)
    assert (prod_a > prod_b)
    assert (prod_a < prod_b) == False
    assert (prod_a == prod_b) == False


def test_product_a_eq_product_b():
    prod_a = Product("Normal Product", price=100.00, quantity=2)
    prod_b = Product("Other Normal Product", price=100.00, quantity=2)
    assert (prod_a > prod_b) == False
    assert (prod_a < prod_b) == False
    assert (prod_a == prod_b)
