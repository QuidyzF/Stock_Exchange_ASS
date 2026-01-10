import pytest
from unittest import mock
from src.parser import Parser
from src.order import Order
from src.exchange import Exchange


@pytest.fixture
def exchange_mock(mocker):
    return mocker.create_autospec(Exchange, instance=True)

@pytest.fixture
def parser(exchange_mock):
    return Parser(core = exchange_mock)

def create_mock_order(*args, **kwargs):
    defaults = {
        "stock": "SNAP",
        "action_type": "LMT",
        "action": "BUY",
        "price": 30.0,
        "execution_price": None,
        "quantity": 100,
        "filled_quantity": 100,
        "status": "FILLED"
    }
    defaults.update(kwargs)
    return mock.Mock(**defaults)

class TestTradeCommand:
    @pytest.mark.parametrize('action, parts, expected_order, expected_error', [
        # LMT orders
        ("BUY", ["SNAP", "LMT", "$30", "100"], ["BUY", "SNAP", "LMT", 30, 100],
         None),
        ("SELL", ["SNAP", "LMT", "$30", "100"], ["SELL", "SNAP", "LMT", 30, 100],
         None),
        # MKT orders
        ("BUY", ["SNAP", "MKT", "100"], ["BUY", "SNAP", "MKT", None, 100],
         None),
        ("SELL", ["SNAP", "MKT", "100"], ["SELL", "SNAP", "MKT", None, 100],
         None),
        # Ошибка: Цена должна начинаться с '$'.
        ("BUY", ["SNAP", "LMT", "30", "100"], ["BUY", "SNAP", "LMT", 30, 100],
         "Цена должна начинаться с '$'."),
        # Ошибка: Для LMT заявки требуются: Продажа/Покупка, LMT, Цена, Кол-во
        ("BUY", ["SNAP", "LMT", "$30"], ["BUY", "SNAP", "LMT", 30, 100],
         "Для LMT заявки требуются: Продажа/Покупка, LMT, Цена, Кол-во"),
        # Ошибка: Для MKT заявки требуются: Продажа/Покупка, MKT, Кол-во
        ("BUY", ["SNAP", "MKT"], ["BUY", "SNAP", "MKT", 30, 100],
         "Для MKT заявки требуются: Продажа/Покупка, MKT, Кол-во"),
        # Ошибка: Указанного вида заявки не существует.
        ("BUY", ["SNAP", "EURO"], ["BUY", "SNAP", "MKT", 30, 100],
         "Указанного вида заявки не существует."),
        ("BUY", ["snap", "lmt", "$30", "100"], ["BUY", "SNAP", "LMT", 30, 100],
         "Указанного вида заявки не существует."),
        # Ошибка: Указанное количество должно быть числом
        ("BUY", ["SNAP", "LMT", "$30", "SNAP"], ["BUY", "SNAP", "LMT", 30, 100],
         "Значение SNAP должно быть числом"),
        ("BUY", ["SNAP", "LMT", "$SNAP", "100"], ["BUY", "SNAP", "LMT", 30, 100],
         "Значение SNAP должно быть числом"),
    ],
    # ID для каждого теста
    ids = [
        "buy_lmt_OK",
        "sell_lmt_OK",
        "buy_mkt_OK",
        "sell_mkt_OK",
        "error_price_with_dollar",
        "error_lmt_order_not_correct",
        "error_mkt_order_not_correct",
        "error_action_doesnt_exist",
        "lower_name_of_actions",
        "strange_value_in_quantity",
        "strange_value_in_price",
    ])
    def test_trade_command_works_correctly(self, parser, exchange_mock, capsys, action, parts, expected_order, expected_error):
        #with mock.patch('builtins.print'):
        if expected_error:
            parser.trade_command(action, parts)
            capture = capsys.readouterr()
            assert expected_error in capture.out or expected_error in capture.err
            exchange_mock.place_order.assert_not_called()
        else:
            with mock.patch('builtins.print'):
                parser.trade_command(action, parts)
                exchange_mock.place_order.assert_called_once_with(*expected_order)

class TestViewOrdersCommand:
    def test_view_orders_without_orders(self, parser, exchange_mock, capsys):
        exchange_mock.get_sorted_orders_list.return_value = []
        parser.view_command("VIEW", ["ORDERS"])
        assert "Список на данный момент пуст" in capsys.readouterr().out

    def test_view_orders_with_data(self, parser, exchange_mock, capsys):
        order_1 = create_mock_order(action="BUY", quantity=100, filled_quantity=100)
        order_2 = create_mock_order(action="SELL", quantity=100, filled_quantity=50, status="PARTIAL")
        order_3 = create_mock_order(stock="FB", action_type="MKT", action="SELL", price=20.0, status="FILLED", filled_quantity=100, quantity=100)
        exchange_mock.get_sorted_orders_list.return_value = [order_1, order_2, order_3]
        parser.view_command("VIEW", ["ORDERS"])
        capture = capsys.readouterr().out.strip().splitlines()
        assert capture[-3] == "1. SNAP LMT BUY $30.0 100 100/100 FILLED"
        assert capture[-2] == "2. SNAP LMT SELL $30.0 100 50/100 PARTIAL"
        assert capture[-1] == "3. FB MKT SELL $20.0 100 100/100 FILLED"

    def test_view_order(self, parser, exchange_mock, capsys):
        parser.view_command("VIEW", ["ASSET"])
        assert "Может вы имели ввиду VIEW ORDERS ?" in capsys.readouterr().out

class TestQuoteCommand:
    def test_quote_command_output(self, parser, exchange_mock, capsys):
        mock_book = mock.Mock()
        mock_book.get_quote.return_value = (30, 31, 32)
        exchange_mock.books = {"SNAP": mock_book}

        parser.quote_command("QUOTE", ["SNAP"])
        assert "SNAP BID: $30.0 ASK: $31.0 LAST: $32.0" in capsys.readouterr().out

class TestRunOut:
    def test_run_quit(self, parser, capsys):
        with mock.patch('builtins.input', return_value="QUIT"):
            parser.run()

        assert "SEASS started" in capsys.readouterr().out

    def test_run_with_two_commands(self, parser, capsys):
        with mock.patch('builtins.input', side_effect=["ASSET", "QUIT"]):
            parser.run()
            assert "Неизвестная команда: ASSET" in capsys.readouterr().out