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
        print('SEASS started. QUIT for exit')

    # Action: BUY SNAP LMT $30 100
    #         нет   0   1   2   3
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

    # Action: BUY    |  SNAP LMT $30 100
    #         action |  parts
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

    def quote_command(self, action, parts):
        stock = parts[0]
        #Дальше относимся к Exchange с обработкой команды.

    def view_command(self, action, parts):
        if len(parts) == 1 and action == 'VIEW' and parts[0] == 'ORDERS':
            print(self.core.view_orders())
            #print(self.core.books, self.core.orders_list)
        else:
            raise ValueError("Может вы имели ввиду VIEW ORDERS ?")

    def run(self):
        while True:
            user_input = input('Action: ').upper().split()
            if not user_input:
                continue

            action = user_input[0]
            parts = user_input[1:]

            if action == 'QUIT':
                return
            if action in self.commands:
                self.commands[action](action, parts)
            else:
                print(f"Неизвестная команда: {action}.")