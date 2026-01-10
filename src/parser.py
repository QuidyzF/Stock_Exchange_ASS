from src.exchange import Exchange

class Parser:
    """Парсинг входных данных и передача в главный орган"""
    def __init__(self, core: Exchange):
        self.core = core
        self.commands = {
            'BUY': self.trade_command,
            'SELL': self.trade_command,
            'QUOTE': self.quote_command,
            'VIEW': self.view_command
        }

    def _command_parser(self, user_input: list) -> tuple:
        stock = user_input[0]

        match user_input[1:]:
            case ["LMT", price_str, quantity_str]:
                if not price_str.startswith('$'):
                    raise ValueError("Цена должна начинаться с '$'.")

                self._int_check(price_str.lstrip('$'))
                self._int_check(quantity_str)

                price = float(price_str.lstrip('$'))
                quantity = int(quantity_str)
                return stock, "LMT", price, quantity

            case ["MKT", quantity_str]:
                self._int_check(quantity_str)
                quantity = int(quantity_str)
                return stock, "MKT", None, quantity

            case ["LMT", *another]:
                raise ValueError("Для LMT заявки требуются: Продажа/Покупка, LMT, Цена, Кол-во")

            case ["MKT", *another]:
                raise ValueError("Для MKT заявки требуются: Продажа/Покупка, MKT, Кол-во")

            case _:
                raise ValueError("Указанного вида заявки не существует.")

    def trade_command(self, action, parts):
        try:
            action = action
            stock, action_type, price, quantity = self._command_parser(parts)

            order = self.core.place_order(action, stock, action_type, price, quantity)

            buy_type = "покупку" if order.action == "BUY" else "продажу"
            if action_type == 'LMT':
                msg = f"Вы разместили лимитную заявку на {buy_type} {order.quantity} акций {order.stock} по цене ${order.price} за штуку."
            else:
                msg = f"Вы разместили рыночную заявку на {buy_type} {order.quantity} акций {order.stock}."

            print(msg)
        except ValueError as e:
            print(f'Ошибка - {e}')
        except TypeError as e:
            print(f'Ошибка - {e}')

    def quote_command(self, action, parts):
        stock = parts[0]
        best_bid, best_ask, last_trade_price = self.core.books[stock].get_quote()
        print(f"SNAP BID: ${float(best_bid)} ASK: ${float(best_ask)} LAST: ${float(last_trade_price)}")

    def view_command(self, action, parts):
        if len(parts) == 1 and action == 'VIEW' and parts[0] == 'ORDERS':
            output = []
            sorted_list = self.core.get_sorted_orders_list()
            if not sorted_list:
                print("Список на данный момент пуст")
                return

            for i, order in enumerate(sorted_list, 1):
                price = order.execution_price if order.execution_price else order.price
                line = f'{i}. {order.stock} {order.action_type} {order.action} ${price} {order.quantity} {order.filled_quantity}/{order.quantity} {order.status}'
                output.append(line)
            msg = '\n'.join(output)
            print(msg)
        else:
            print("Может вы имели ввиду VIEW ORDERS ?")
            return

    def run(self):
        print('SEASS started. QUIT for exit')
        while True:
            user_input = input('Action: ').upper().split()
            if not user_input:
                continue

            action, parts = user_input[0], user_input[1:]

            if action == 'QUIT':
                return
            self.commands[action](action, parts) if action in self.commands else print(f"Неизвестная команда: {action}.")

    @staticmethod
    def _int_check(value):
        try:
            float(value)
        except ValueError:
            raise ValueError(f"Значение {value} должно быть числом")