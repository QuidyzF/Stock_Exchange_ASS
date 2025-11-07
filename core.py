from dataclasses import dataclass, field
import itertools

# простой вариант счетчика
_id_counter = itertools.count(1)

@dataclass
class InputContainer:
    """
    Контейнер входных данных
    """
    user_action: str
    quote: str
    order_type: str
    price: float
    count: int

@dataclass
class Container:
    """
    Контейнер с информация по акциям
    """
    market_type: str # BUY | SELL
    order_type: str # LMT | MKT
    quantity: int
    quote: str

    price: float | None

    status: str = "PENDING"
    ordered_quantity: int = 0

    id: int = field(init=False, default_factory=lambda: next(_id_counter))

    def status_validation(self):
        """
        Проверяем и меняем статус заявки
        """
        if self.ordered_quantity == 0:
            self.status = 'PENDING'
        elif self.ordered_quantity < self.quantity:
            self.status = 'PARTIAL'
        else:
            self.status = 'FILLED'

    def fill(self, quantity: int, price: float):
        """
        Заполняем контейнер с акциями
        """
        self.ordered_quantity += quantity
        self.status_validation()


    @property
    def remaining_order_quantity(self):
        """
        Возвращаем оставшееся свободное количество
        """
        return self.quantity - self.ordered_quantity

    @property
    def is_filled(self):
        """
        Приравниваем свободное место к нулю, если будет вызов
        """
        return self.ordered_quantity == 0

class BirzhaCore:
    def __init__(self):
        self.trade_actions = {
            ('BUY', 'LMT'): self.add_orded_BUY_LMT,
            ('BUY', 'MKT'): None,
            ('SELL', 'LMT'): None,
            ('SELL', 'MKT'): None
        }

    def command_maker(self,  command: InputContainer):
        """
        Вызываем тип действия на основе полученных данных
        """
        action = (command.user_action, command.order_type)

        if action in self.trade_actions:
            self.trade_actions[action](command.quote, command.price, command.count)
        else:
            print('Error')

    def add_orded_BUY_LMT(self, quote, price, count):
        Container.market_type = 'BUY'
        Container.order_type = 'LMT'
        Container.quote = quote
        Container.price = price
        Container.quantity = count
        return Container