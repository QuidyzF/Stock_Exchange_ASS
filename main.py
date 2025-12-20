import itertools
from dataclasses import dataclass, field

#Декоратор для отладки
def debugger(func):
    def wrapper(*args, **kwargs):
        class_name = args[0].__class__.__name__
        print(f'DEBUG: {class_name}({func.__name__})')
        print(f'    --> args: {args}')
        return func(*args, **kwargs)
    return wrapper

# простой вариант счетчика
_id_counter = itertools.count(1)

@dataclass
class Order:
    """Класс Заявок, хранит детали"""
    stock: str # stock name
    action: str # BUY | SELL
    action_type: str # LMT | MKT
    quantity: int # Count of action
    price: float | None = None # Price of action

    filled_quantity: int = 0 # Quantity counter for status
    status: ['PENDING', 'PARTIAL', 'FILLED'] = 'PENDING'

    id: int = next(_id_counter)

    def __post_init__(self):
        """Проверка типа продажи и количества"""
        if self.quantity <= 0:
            raise ValueError("Количество должно быть положительным.")

        if self.action_type == 'LMT' and (self.price is None or self.price <= 0):
            raise ValueError("Для лимитной заявки цена должна быть указана.")

        if self.action_type == 'MKT' and self.price is not None:
            raise ValueError("Для рыночной заявки цена не нужна.")

    def get_quantity(self) -> int:
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

    def get_quote(self):
        best_bid = self.bids[0].price
        best_ask = self.asks[0].price
        return best_bid, best_ask, self.last_trade_price

    @debugger
    def _match_fill_update(self, new_order, counter_orders, price_check):
        quantity_to_close_order = new_order.get_quantity()

        for i, counter_order in enumerate(counter_orders):
            if quantity_to_close_order <= 0:
                break
        pass

    def process_order(self, new_order):

        if new_order.action_type == 'LMT':
            pass
        else:
            pass
class Exchange:
    """Главное управление всей биржей. Команды пользователя и хранит историю сделок/статусы заявок"""
    def __init__(self):
        self.books = {}
        self.orders_list = {}

    def _get_or_create_order(self, stock):
        if stock not in self.books:
            self.books[stock] = OrderBook(stock)
        return self.books[stock]

    @debugger
    def place_order(self, action, stock, action_type, price, quantity):

        try:
            new_order = Order(
                stock=stock,
                action = action,
                action_type = action_type,
                price = price,
                quantity = quantity
            )
        except ValueError as e:
            print(f'Ошибка в Exchange.place_order() в try: {e}')

        self.orders_list[new_order.id] = new_order
        book = self._get_or_create_order(stock)

        # Здесь вставить обработку операции через class Book
        book.process_order(new_order)
        # --- Возвращение необходимого print ---
        if action_type == 'LMT':
            action_info = 'лимитную заявку'
        action_info = 'рыночную заявку'

        return f"Вы разместили {action_info} на покупку {quantity} акций {stock} по цене ${price} за штуку."

    def view_orders(self):
        output = []

        sorted_order_list = sorted(self.orders_list.values(), key=lambda x: x.id)

        for i, order in enumerate(sorted_order_list, 1):
            line = f'{i}. {order.stock} {order.action_type} {order.action} {order.price} {order.quantity} {order.filled_quantity}/{order.quantity} {order.status}'

            output.append(line)

        return '\n'.join(output)

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
    #         нет   0   1   2   3
    @debugger
    def _command_parser(self, user_input: list) -> tuple:
        stock = user_input[0]
        action_type_check = user_input[1]

        if action_type_check == 'LMT':
            if len(user_input) != 4:
                raise ValueError("Для LMT заявки требуются: Продажа/Покупка, LMT, Цена, Кол-во")

            price_check = user_input[2]
            if not price_check.startswith('$'):
                raise ValueError("Цена должна начинаться с '$'.")

            price = float(price_check.lstrip('$'))
            quantity = int(user_input[3])
            action_type = 'LMT'

        elif action_type_check == 'MKT':
            if len(user_input) != 3:
                raise ValueError("Для MKT заявки требуются: Продажа/Покупка, MKT, Кол-во")

            price = None
            quantity = int(user_input[2])
            action_type = 'MKT'

        else:
            raise ValueError("Указанного вида заявки не существует.")

        return stock, action_type, price, quantity

    @debugger
    def trade_command(self, action, parts):
        try:
            action = action
            stock, action_type, price, quantity = self._command_parser(parts)

            # Здесь мы относимся к классу Exchange и выдаём информацию.
            # Action: BUY FB MKT 20
            # Вы разместили рыночную заявку на покупку 20 акций FB.
            result = self.core.place_order(action, stock, action_type, price, quantity)
            print(result)

        except ValueError as e:
            print(f'Сработка ValueError. Ошибка {e}')
        except TypeError as e:
            print(f'Сработка TypeError. Ошибка {e}')

    @debugger
    def quote_command(self, action, parts):
        stock = parts[0]
        #Дальше относимся к Exchange с обработкой команды.

    @debugger
    def view_command(self, action, parts):
        if len(parts) == 1 and action == 'VIEW' and parts[0] == 'ORDERS':
            print(self.core.view_orders())
            print(self.core.books, self.core.orders_list)
        else:
            raise ValueError("Может вы имели ввиду VIEW ORDERS ?")

    def run(self):
        while True:
            user_input = input('Action: ').upper().split()
            if not user_input:
                continue

            action = user_input[0]
            parts = user_input[1:]
            if action in self.commands:
                if action == 'QUIT':
                    return
                self.commands[action](action, parts)
            else:
                print(f"Неизвестная команда: {action}.")

if __name__ == "__main__":
    core = Exchange()
    main = Parser(core)
    main.run()