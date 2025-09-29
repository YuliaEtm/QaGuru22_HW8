class Product:
    """
    Класс продукта
    """
    name: str
    price: float
    description: str
    quantity: int

    def __init__(self, name, price, description, quantity):
        self.name = name
        self.price = price
        self.description = description
        self.quantity = quantity

    def check_quantity(self, user_quantity) -> bool:
        """
         Верните True если количество продукта больше или равно запрашиваемому
         и False в обратном случае
        """
        return self.quantity >= user_quantity

    def buy(self, user_quantity):
        if self.check_quantity(user_quantity):
            self.quantity = self.quantity - user_quantity
            return True
        else:
            raise ValueError(f"Извините, у нас есть только {self.quantity}")

    def __hash__(self):
        return hash(self.name + self.description)


class Cart:
    """
    Класс корзины. В нем хранятся продукты, которые пользователь хочет купить.
    """

    # Словарь продуктов и их количество в корзине
    products: dict[Product, int]

    def __init__(self):
        # По-умолчанию корзина пустая
        self.products = {}

    def add_product(self, product: Product, buy_count=1):
        """
        Метод добавления продукта в корзину.
        Если продукт уже есть в корзине, то увеличиваем количество
        """
        if buy_count > 0:
            if product not in self.products:
                if product.check_quantity(buy_count):
                    self.products[product] = buy_count
                else:
                    raise ValueError(f"Извините, у нас недостаточно этого продукта")
            else:
                if product.check_quantity(self.products[product] + buy_count):
                    self.products[product] += buy_count
                else:
                    raise ValueError(f"Извините, у нас недостаточно этого продукта")
        else:
            raise ValueError(f" неверное количество 0")

    def remove_product(self, product: Product, remove_count=None):
        """
        Метод удаления продукта из корзины.
        Если remove_count не передан, то удаляется вся позиция
        Если remove_count больше, чем количество продуктов в позиции, то удаляется вся позиция
        """
        if self.products.get(product):
            if not remove_count:
                self.products.pop(product)
            elif remove_count > self.products[product]:
                self.products.pop(product)
            else:
                self.products[product] -= remove_count
        else:
            raise ValueError("продукта нет в корзине")

    def clear(self):
        """
        Метод покупки.
        Очищает корзину
        """
        self.products = {}

    def get_total_price(self):
        """
        Метод покупки.
        Подсчитывает общую стоимость корзины
        """
        total_price = 0
        for key in self.products.keys():
            total_price += key.price * self.products.get(key)
        return total_price

    def buy(self):
        """
        Метод покупки.
        Учтите, что товаров может не хватать на складе.
        В этом случае нужно выбросить исключение ValueError
        """

        for product in self.products.keys():
            product.buy(self.products.get(product))

        self.clear()
