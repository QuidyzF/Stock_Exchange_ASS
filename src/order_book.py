from src.order import Order


class OrderBook:
    """Управление заявками на покупку и продажу акций"""
    def __init__(self, stock: str):
        self.stock = stock
        self.bids = [] # купить
        self.asks = [] # продать
        self.last_trade_price = None

    def _sort_books(self):
        # Сортируем завки на покупку [HIGH -> LOW]
        self.bids.sort(key=lambda x: x.price if x.price is not None else 0, reverse=True)
        # Сортируем завки на продажу [LOW -> HIGH]
        self.asks.sort(key=lambda x: x.price if x.price is not None else 0)

    def get_quote(self):
        self._sort_books()
        # Запрашиваем лучшую заявку на покупку
        best_bid = self.bids[0].price if self.bids[0].price else None
        # Запрашиваем лучшую заявку на продажу
        best_ask = self.asks[0].price if self.asks[0].price else None
        # Возвращаем данные - [покупка, продажа, последняя цена]
        return best_bid, best_ask, self.last_trade_price

    def _book_updater(self, new_order, counter_orders, price_check):
        quantity_to_close_order = new_order.get_quantity()

        for i, counter_order in enumerate(counter_orders):
            if quantity_to_close_order <= 0:
                break

            if counter_order.action_type == 'LMT' and not price_check(new_order, counter_order):
                if new_order.action_type == 'LMT':
                    break

            filling_quantity_in_this_action = min(quantity_to_close_order, counter_order.get_quantity())
            if filling_quantity_in_this_action <= 0:
                continue

            if counter_order.action_type == 'LMT':
                trade_price = counter_order.price
            elif new_order.action_type == 'LMT':
                trade_price = new_order.price
            else:
                trade_price = self.last_trade_price or 0

            if new_order.execution_price is None:
                new_order.execution_price = trade_price
            if counter_order.execution_price is None:
                counter_order.execution_price = trade_price

            new_order.filling_update(filling_quantity_in_this_action)
            counter_order.filling_update(filling_quantity_in_this_action)

            self.last_trade_price = trade_price
            quantity_to_close_order = new_order.get_quantity()

    def process_order(self, order):
        """Обработка заявки и обновление статуса"""
        if order.action == 'BUY':
            order_book = self.asks
            price_check = lambda new_order, match_order: new_order.price >= match_order.price
            remaining_book = self.bids
        else:
            order_book = self.bids
            price_check = lambda new_order, match_order: new_order.price <= match_order.price
            remaining_book = self.asks

        # Пытаемся обновить состояние акции
        self._book_updater(order, order_book, price_check)

        # Проверяем статус акции, если она не является полной -> кладём в стакан с ожидающими
        if order.get_quantity() > 0:
            remaining_book.append(order)
            self._sort_books()