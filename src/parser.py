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
            print(f'Сработка ValueError. Ошибка - {e}')
        except TypeError as e:
            print(f'Сработка TypeError. Ошибка - {e}')

    def quote_command(self, action, parts):
        stock = parts[0]
        best_bid, best_ask, last_trade_price = self.core.books[stock].get_quote()
        print(f"SNAP BID: ${best_bid} ASK: ${best_ask} LAST: ${last_trade_price}")

    def view_command(self, action, parts):
        try:
            if len(parts) == 1 and action == 'VIEW' and parts[0] == 'ORDERS':
                output = []
                sorted_list = self.core.get_sorted_orders_list()
                for i, order in enumerate(sorted_list, 1):
                    price = order.execution_price if order.execution_price else order.price
                    line = f'{i}. {order.stock} {order.action_type} {order.action} ${price} {order.quantity} {order.filled_quantity}/{order.quantity} {order.status}'
                    output.append(line)
                msg = '\n'.join(output)
                print(msg)
                #print(self.core.books, self.core.orders_list)
            else:
                raise ValueError("Может вы имели ввиду VIEW ORDERS ?")
        except ValueError as e:
            print(e)

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

