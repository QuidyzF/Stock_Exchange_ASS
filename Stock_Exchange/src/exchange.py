from src.order import Order
from src.order_book import OrderBook

class Exchange:
    """Главное управление всей биржей. Команды пользователя и хранит историю сделок/статусы заявок"""
    def __init__(self):
        self.books = {}
        self.orders_list = {}

    def _get_or_create_order(self, stock):
        if stock not in self.books:
            self.books[stock] = OrderBook(stock)
        return self.books[stock]

    # Action: BUY SNAP LMT $30 100
    #         нет   0   1   2   3
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
            return f"Вы разместили лимитную заявку на покупку {quantity} акций {stock} по цене ${price} за штуку."
        return f"Вы разместили рыночную заявку на покупку {quantity} акций {stock}."

    def view_orders(self):
        # Список на вывод
        output = []

        # Сортируем наш список акций по id
        sorted_order_list = sorted(self.orders_list.values(), key=lambda x: x.id)

        # Перебираем отсортированный список, нумеруем и подготавливаем к выводу
        #for i, order in enumerate(sorted_order_list, 1):
        #    if order.action_type == 'MKT' and order.price is None:
        #        line = f'{i}. {order.stock} {order.action_type} {order.action} ${order.execution_price} {order.quantity} {order.filled_quantity}/{order.quantity} {order.status}'
        #    else:
        #        line = f'{i}. {order.stock} {order.action_type} {order.action} ${order.price} {order.quantity} {order.filled_quantity}/{order.quantity} {order.status}'
        #    output.append(line)
        for i, order in enumerate(sorted_order_list, 1):
            line = f'{i}. {order.stock} {order.action_type} {order.action} ${order.execution_price} {order.quantity} {order.filled_quantity}/{order.quantity} {order.status}'
            output.append(line)
        return '\n'.join(output)