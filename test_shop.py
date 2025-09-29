"""
Протестируйте классы из модуля homework/models.py
"""
import pytest
from models import Product, Cart


@pytest.fixture
def product_book() -> Product:
    return Product("book", 100, "This is a book", 1000)


@pytest.fixture
def product_pen() -> Product:
    return Product("pen", 1, "This is a pen", 2000)


class TestProducts:

    def test_product_check_quantity_equal(self, product_book):
        assert product_book.check_quantity(product_book.quantity)

    def test_product_check_quantity_more(self, product_book):
        assert not product_book.check_quantity(product_book.quantity + 1)

    def test_product_check_quantity_less(self, product_book):
        assert product_book.check_quantity(product_book.quantity - 1)

    def test_product_buy(self, product_book):
        # проверка корректной покупки
        user_buy_quantity = 100
        quantity_before = product_book.quantity

        product_book.buy(user_buy_quantity)

        assert product_book.quantity == quantity_before - user_buy_quantity

    def test_product_buy_more_than_available(self, product_book):
        #  попытка купить больше, чем есть в наличии
        with pytest.raises(ValueError):
            product_book.buy(product_book.quantity + 1)


@pytest.fixture(scope='function')
def cart() -> Cart:
    return Cart()


class TestCart:

    def test_add_product(self, cart, product_book):
        # добавление в корзину одного продукта
        cart.add_product(product_book, 100)

        assert cart.products[product_book] == 100

    def test_add_product_twice(self, cart, product_book):
        # добавление в корзину два раза одного продукта
        cart.add_product(product_book, 100)
        cart.add_product(product_book, 300)

        assert cart.products[product_book] == 400

    def test_add_product_twice_not_correct(self, cart, product_book):
        # добавление в корзину два раза одного продукта с превышением количества
        with pytest.raises(ValueError):
            cart.add_product(product_book, 100)
            cart.add_product(product_book, 901)

    def test_add_product_is_0(self, cart, product_book):
        # Продукт с количеством 0 в корзину не добавляется
        with pytest.raises(ValueError):
            cart.add_product(product_book, 0)

    def test_add_two_products(self, cart, product_book, product_pen):
        # добавление в корзину двух разных продуктов
        cart.add_product(product_book, 10)
        cart.add_product(product_pen, 30)
        assert cart.products[product_book] == 10
        assert cart.products[product_pen] == 30

    def test_remove_product_by_count_is_none(self, cart: Cart, product_book: Product):
        #  удаление из корзины продукта без указания количества
        cart.add_product(product_book, 100)

        cart.remove_product(product_book)

        assert cart.products == {}

    def test_remove_product(self, cart, product_book):
        # удаление из корзины продукта с указанием корректного количества
        cart.add_product(product_book, 100)

        cart.remove_product(product_book, cart.products[product_book] - 1)

        assert cart.products[product_book] == 1

    def test_remove_over_product(self, cart, product_book):
        # удаление из корзины продукта с указанием большего количества
        cart.add_product(product_book, 100)

        cart.remove_product(product_book, cart.products[product_book] + 1)

        assert cart.products == {}

    def test_remove_product_multi(self, cart, product_book, product_pen):
        # удаление из корзины с несколькими продуктами части одного продукта
        cart.add_product(product_book, 100)
        cart.add_product(product_pen, 10)

        cart.remove_product(product_book, cart.products[product_book] - 1)

        assert cart.products[product_book] == 1
        assert cart.products[product_pen] == 10

    def test_remove_product_multi2(self, cart, product_book, product_pen):
        # удаление из корзины невнесенного продукта
        with pytest.raises(ValueError):
            cart.add_product(product_book, 100)

            cart.remove_product(product_pen, 2)

    def test_clear_cart(self, cart, product_book, product_pen):
        # очистка корзины с несколькими продуктами
        cart.add_product(product_book, 100)
        cart.add_product(product_pen, 10)

        cart.clear()

        assert cart.products == {}

    def test_clear_empty_cart(self, cart):
        # очистка пустой корзины
        cart.clear()
        assert cart.products == {}

    def test_total_prise(self, cart, product_book, product_pen):
        # проверка стоимости корзины
        buy_count_book = 100
        cart.add_product(product_book, buy_count_book)
        buy_count_pen = 10
        cart.add_product(product_pen, buy_count_pen)

        total_price = cart.get_total_price()

        assert total_price == product_book.price * buy_count_book + product_pen.price * buy_count_pen

    #  на один продукт написать

    def test_total_prise_empty_cart(self, cart):
        # проверка стоимости пустой корзины
        total_price = cart.get_total_price()
        assert total_price == 0

    def test_buy_product(self, cart, product_book):
        # проверка покупки 1 товара корзиной корректная
        count_book = product_book.quantity
        buy_count_book = 100
        cart.add_product(product_book, buy_count_book)

        cart.buy()

        assert product_book.quantity == count_book - buy_count_book
        assert cart.products == {}

    def test_buy_two_product(self, cart, product_book, product_pen):
        # проверка покупки 2 товара корзиной корректная
        count_book = product_book.quantity
        buy_count_book = 10
        count_pen = product_pen.quantity
        buy_count_pen = 5
        cart.add_product(product_book, buy_count_book)
        cart.add_product(product_pen, buy_count_pen)

        cart.buy()

        assert product_book.quantity == count_book - buy_count_book
        assert product_pen.quantity == count_pen - buy_count_pen
        assert cart.products == {}
