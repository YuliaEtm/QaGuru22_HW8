"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from models import Product, Cart


@pytest.fixture
def product() -> Product:
    return Product("book", 100, "This is a book", 1000)


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity_poz(self, product):
        # TODO напишите проверки на метод quantity
        print(product.check_quantity(product.quantity))
        assert product.check_quantity(product.quantity)

    def test_product_check_quantity_neg(self, product):
        # TODO напишите проверки на метод quantity
        print(product.check_quantity(product.quantity+1))
        assert not product.check_quantity(product.quantity+1)

    def test_product_buy(self, product):
        user_buy_quantity = 100
        quantity_before = product.quantity
        product.buy(user_buy_quantity)
        assert product.quantity == quantity_before - user_buy_quantity
        # TODO напишите проверки на метод buy

    def test_product_buy_more_than_available(self, product):
        # TODO напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии
        with pytest.raises(ValueError):
            product.buy(product.quantity+1)


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

    def test_add_product(self, cart, product):
        cart.add_product(product, 100)

        pass