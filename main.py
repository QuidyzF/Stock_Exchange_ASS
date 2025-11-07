from core import BirzhaCore, InputContainer, Container

class StartCore:
    def __init__(self, core: BirzhaCore):
        self.core = core
        print('SEASS started. QUIT for exit')

    def info_parser(self, user_input: list) -> InputContainer:
        if len(user_input) != 5:
            raise ValueError('Необходимо 5 аргументов')

        try:
            user_action, quote, order_type, price, count = user_input
            return InputContainer(
                user_action = user_action,
                quote = quote,
                order_type = order_type,
                price = float(price[1:]),
                count = int(count)
            )
        except ValueError as e:
            print(f"Error: {e}")


    def info_finder(self):
        while True:
            user_input = input('Action: ').upper()
            formated_user_input = user_input.split()

            if not user_input:
                print('Error: unknown command')
                continue

            user_action = formated_user_input[0] # Забирает тик действия - BUY/SELL/VIEW/QUOTE/QUIT

            if user_action == 'VIEW':
                if formated_user_input[1] == 'ORDERS':
                    pass

            if user_action == 'QUOTE':
                if formated_user_input[1] == 'SNAP':
                    pass

            if user_action == 'QUIT':
                print(InputContainer)
                break

            if user_action == 'VIEW ORDERS':
                pass

            if user_action in ('BUY', 'SELL'):
                command = self.info_parser(formated_user_input)
                print(command)
                if command:
                    result = self.core.command_maker(command)
                    print(result)
                else:
                    print('Unknown command')

            # Action: QUIT
            # Action: VIEW ORDERS
            # Action: QUOTE SNAP
            # Action: BUY SNAP LMT $30 100
            # Вы разместили лимитную заявку на покупку 100 акций SNAP по цене $30.00 за штуку.

if __name__ == "__main__":
    core = BirzhaCore()
    main = StartCore(core)
    main.info_finder()