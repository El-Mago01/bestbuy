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


"""
import pytest
from products import Product, ProductUnavailable, LimitedProduct, NonStockedProduct

# 1.1
def test_create_new_product():
    prod = Product("test product", 100.00, 50)
    assert prod.is_active() == True
    assert prod.show() == "test product, Price: 100.00, Quantity: 50"
    assert prod.get_quantity() == 50

#1.2
def test_create_new_product_empty_name():
    with pytest.raises(ValueError, match="Product name can not be empty"):
        prod = Product("", 100, 50)

#1.3
def test_create_with_price_as_string():
    with pytest.raises(ValueError, match="Please ensure price is valid"):
        prod = Product("test product","100", 50)

#1.4
def test_create_with_quantity_as_float():
    with pytest.raises(ValueError, match="Please ensure quantity is a valid number"):
        prod = Product("test product",100, 50.0)

# 1.5
def test_create_product_with_negative_price():
    with pytest.raises(ValueError, match="Please ensure price is valid"):
        prod = Product("test product",-100, 50)

#1.6
def test_create_product_with_negative_quantity():
    with pytest.raises(ValueError, match="Please ensure quantity is a valid number"):
        prod = Product("test product",100, -50)

# 1.7
def test_create_new_nonstockedproduct():
    prod = NonStockedProduct("test product", 100.00)
    assert prod.is_active() == True
    assert prod.show() == "test product, Price: 100.00, Quantity: unlimited"
    assert prod.get_quantity() == 0

# 1.8
def test_create_new_limitedproduct():
    prod = LimitedProduct("test product", 100.00, 50, 1)
    assert prod.is_active() == True
    assert prod.show() == "test product, Price: 100.00, Quantity: 50, Max. order size = 1"
    assert prod.get_quantity() == 50

#2.1
def test_deactivate_by_deactivating():
    prod = Product("Test Product", 100, 50)
    assert prod.is_active() == True
    prod.deactivate()
    assert prod.is_active() == False
    assert prod.get_price() == 100
    assert prod.get_quantity() == 50

#2.2
def test_deactivate_by_0_quantity():
    prod = Product("Test Product",100,50)
    assert prod.is_active() == True
    assert prod.get_quantity() == 50
    price = prod.buy(50)
    assert price == 50*100
    assert prod.is_active() == False
    assert prod.get_price() == 100
    assert prod.get_quantity() == 0

#2.3
def test_illegal_deactivation():
    prod = Product("test product", 100, 50)
    prod.__activate = False
    assert prod.is_active() == True

def test_buy_product():
    prod = Product("test product", 100, 50)
    price = prod.buy(10)
    assert price == 10*100
    assert prod.get_quantity() == 40
    assert prod.is_active() == True

def test_buy_product_quantity_too_high():
    prod = Product("test product", price=100.00, quantity=50)
    with pytest.raises(ProductUnavailable, match="Not enough quantity available"):
        price = prod.buy(51)
    assert prod.is_active() == True

def test_buy_nonsstockedproduct():
    prod = NonStockedProduct("test product", 100)
    price = prod.buy(1)
    assert price == 1*100
    assert prod.get_quantity() == 0
    assert prod.is_active() == True

def test_buy_nonsstockedproduct_5_elements():
        prod = NonStockedProduct("test product", 100)
        price = prod.buy(5)
        assert price == 5 * 100
        assert prod.get_quantity() == 0
        assert prod.is_active() == True

def test_buy_limitedproduct_at_maximum():
    prod = LimitedProduct("test product", 100, quantity=2, maximum=2)
    price = prod.buy(2)
    assert price == 2 * 100
    assert prod.get_quantity() == 0
    assert prod.is_active() == False

def test_buy_limitedproduct_over_maximum():
    prod = LimitedProduct("test product", 100, quantity=3, maximum=2)
    with pytest.raises(ValueError, match="^Only 2 articles per order are allowed for this Product"):
        price = prod.buy(3)
    assert prod.is_active() == True



