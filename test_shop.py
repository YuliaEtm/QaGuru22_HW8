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
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity_poz(self, product_book):
        # TODO напишите проверки на метод quantity
        print(product_book.check_quantity(product_book.quantity))
        assert product_book.check_quantity(product_book.quantity)

    def test_product_check_quantity_neg(self, product_book):
        # TODO напишите проверки на метод quantity
        print(product_book.check_quantity(product_book.quantity+1))
        assert not product_book.check_quantity(product_book.quantity+1)

    def test_product_buy(self, product_book):
        user_buy_quantity = 100
        quantity_before = product_book.quantity
        product_book.buy(user_buy_quantity)
        assert product_book.quantity == quantity_before - user_buy_quantity
        # TODO напишите проверки на метод buy

    def test_product_buy_more_than_available(self, product_book):
        # TODO напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии
        with pytest.raises(ValueError):
            product_book.buy(product_book.quantity+1)


@pytest.fixture(scope='function')
def cart() -> Cart:
    return Cart()


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """

    def test_add_product(self, cart, product_book):
        cart.add_product(product_book, 100)
        assert cart.products[product_book] == 100

    def test_add_product_twice(self, cart, product_book):
        cart.add_product(product_book, 100)
        cart.add_product(product_book, 300)
        assert cart.products[product_book] == 400

    def test_add_product_twice_not_correct(self, cart, product_book):
        with pytest.raises(ValueError):
            cart.add_product(product_book, 100)
            cart.add_product(product_book, 901)

    def test_add_product_is_0(self, cart, product_book):
        with pytest.raises(ValueError):
            cart.add_product(product_book, 0)

    def test_add_two_products(self, cart, product_book, product_pen):
        cart.add_product(product_book, 10)
        cart.add_product(product_pen, 30)
        assert cart.products[product_book] == 10
        assert cart.products[product_pen] == 30

    def test_remove_product_by_count_is_none(self, cart: Cart, product_book: Product):
        cart.add_product(product_book, 100)
        cart.remove_product(product_book)
        assert cart.products == {}

    def test_remove_over_product(self, cart, product_book):
        cart.add_product(product_book, 100)
        cart.remove_product(product_book, cart.products[product_book]+1)
        assert cart.products == {}

    def test_remove_product(self, cart, product_book):
        cart.add_product(product_book, 100)
        cart.remove_product(product_book, cart.products[product_book]-1)
        assert cart.products[product_book] == 1

    def test_remove_product_multi(self, cart, product_book,product_pen):
        cart.add_product(product_book, 100)
        cart.add_product(product_pen, 10)
        cart.remove_product(product_book, cart.products[product_book]-1)
        assert cart.products[product_book] == 1
        assert cart.products[product_pen] == 10

    def test_remove_product_multi2(self, cart, product_book,product_pen):
        with pytest.raises(ValueError):
            cart.add_product(product_book, 100)

            cart.remove_product(product_pen, 2)
