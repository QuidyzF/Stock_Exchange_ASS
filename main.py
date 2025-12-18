from dataclasses import dataclass, field
import itertools

from mypy.dmypy.client import action

# простой вариант счетчика
_id_counter = itertools.count(1)

@dataclass
class Order:
    """Класс Заявок, хранит детали"""
    stock: str # Action name
    order_type: str # BUY | SELL
    order_kind: str # LMT | MKT
    quantity: int # Count of action
    price: float | None = None # Price of action

    filled_quantity: int = 0 # Quantity counter for status
    status: ['PENDING', 'PARTIAL', 'FILLED'] = 'PENDING'

    id: int = next(_id_counter)

    def __post_init__(self):
        """Проверка типа продажи и количества"""
        if self.quantity <= 0:
            raise ValueError("Количество должно быть положительным.")

        if self.order_kind == 'LMT' and (self.price is None or self.price <= 0):
            raise ValueError("Для лимитной заявки цена должна быть указана.")

        if self.order_kind == 'MKT' and self.price is not None:
            raise ValueError("Для рыночной заявки цена не нужна.")

    def  get_quantity(self) -> int:
        return self.quantity - self.filled_quantity

    def filling_update(self, new_quantity):
        """Обновление статуса заявки"""
        if new_quantity <= 0:
            raise ValueError("Количество акций должно быть положительным.")

        new_filled_quantity = self.quantity + new_quantity
        if new_filled_quantity > self.quantity:
            raise ValueError("Количество покупаемых акций не должно превышать количество в заявке.")

        self.filled_quantity = new_filled_quantity

        if self.filled_quantity == self.quantity:
            self.status = 'FILLED'
        elif self.filled_quantity < self.quantity:
            self.status = 'PARTIAL'
        else:
            self.status = 'PENDING'

class OrderBook:
    """Управление заявками на покупку и продажу акций"""
    def __init__(self, stock):
        # Сохраняем название акции
        self.stock = stock
        # Контейнер с заявками на покупку
        self.bids = []
        # Контейнер с заявками на продажу
        self.asks = []
        # Сохраняем цену последней транзакции
        self.last_trade_price = None

    def _sort_books(self):
        # Сортируем завки на покупку ( HIGH to LOW )
        self.bids.sort(key=lambda x: x.price, reverse=True)
        # Сортируем завки на продажу ( LOW to HIGH )
        self.asks.sort(key=lambda x: x.price)

    def get_qoute(self):
        best_bid = self.bids[0].price
        best_ask = self.asks[0].price
        return best_bid, best_ask, self.last_trade_price



class Exchange:
    """Главное управление всей биржей. Команды пользователя и хранит историю сделок/статусы заявок"""
    pass

class Parser:
    """Парсинг входных данных и передача в главный орган"""
    def __init__(self, core: Exchange):
        self.core = core
        self.commands = {
            'BUY': self.trade_command,
            'SELL': self.trade_command,
            'QUOTE': self.quote_command,
            'VIEW': self.view_command,
        }
        print('SEASS started. QUIT for exit')

    # Action: BUY SNAP LMT $30 100
    #         0   1    2   3   4
    def _command_parser(self, user_input: list):
        stock = user_input[1]
        action_type_check = user_input[2]

        if action_type_check == 'LMT':
            if len(user_input) != 5:
                raise ValueError("Для LMT заявки требуются: Продажа/Покупка, LMT, Цена, Кол-во")

            price_check = user_input[3]
            if not price.startswith('$'):
                raise ValueError("Цена должна начинаться с '$'.")

            price = float(price_chek.lstrip('$'))
            quantity = int(user_input[4])
            action_type = 'LMT'

        elif action_type_check == 'MKT':
            if len(user_input) != 4:
                raise ValueError("Для MKT заявки требуются: Продажа/Покупка, MKT, Кол-во")

            price = None
            quantity = int(user_input[3])
            action_type = 'MKT'

        return stock, action_type, price, quantity

    def trade_command(self, quote, price, count):
        pass

    def quote_command(self, quote, price, count):
        pass

    def view_command(self, quote, price, count):
        pass

    def run(self):
        while True:
            user_input = input('Action: ').upper().split()
            if not user_input:
                continue

            action = user_input[0]
            if action in self.commands:
                if action == 'QUIT':
                    return
                self.commands[action](user_input)
            else:
                print(f"Неизвестная команда: {action}.")

if __name__ == "__main__":
    core = Exchange()
    main = Parser(core)
    main.run()