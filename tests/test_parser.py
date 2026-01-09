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

#class TestCommandParsery:
    #@pytest.mark.parametrize('action, parts, expected_order', [
    #    # LMT orders
    #    ("BUY", ["SNAP", "LMT", "$30", "100"], ["BUY", "SNAP", "LMT", 30, 100]),
    #    ("SELL", ["SNAP", "LMT", "$30", "100"], ["SELL", "SNAP", "LMT", 30, 100]),
    #    # MKT orders
    #    ("BUY", ["SNAP", "MKT", "100"], ["BUY", "SNAP", "MKT", None, 100]),
    #    ("SELL", ["SNAP", "MKT", "100"], ["SELL", "SNAP", "MKT", None, 100]),
    #])
    #def test_trade_command_works_correctly(self, parser, exchange_mock, action, parts, expected_order):
    #    exchange_mock.place_order.return_value = "OK"
    #    parser.trade_command(action, parts)
    #    exchange_mock.place_order.assert_called_once_with(*expected_order)

    #def test_trade_command_error_handling(self, parser, exchange_mock, capsys):
    #    # price check start with "$"
    #    parser.trade_command("BUY", ["SNAP", "LMT", "30", "100"])
    #    exchange_mock.place_order.assert_not_called()
    #    captured = capsys.readouterr()
    #    assert "Сработка ValueError. Ошибка - Цена должна начинаться с '$'.\n" in captured

    #def test_trade_command_error_handling_with_lenght(self, parser, exchange_mock, capsys):
    #    # user input lenght = 4
    #    parser.trade_command("BUY", ["SNAP", "LMT", "$30"])
    #    exchange_mock.place_order.assert_not_called()
    #    captured = capsys.readouterr()
    #    assert "Сработка ValueError. Ошибка - Для LMT заявки требуются: Продажа/Покупка, LMT, Цена, Кол-во\n" in captured