import pytest
from src.order import Order, ActionType, OrderType, OrderStatus
from src.order_book import OrderBook
from src.exchange import Exchange


@pytest.fixture
def valid_BUY_MKT_order():
    """Валидный рыночный ордер"""
    return Order(stock="SNAP", action=OrderType.BUY, action_type=ActionType.MARKET, quantity=100)

@pytest.fixture
def valid_SELL_MKT_order():
    """Валидный рыночный ордер"""
    return Order(stock="SNAP", action=OrderType.SELL, action_type=ActionType.MARKET, quantity=100)

@pytest.fixture
def valid_BUY_LMT_order():
    """Валидный лимитный ордер"""
    return Order(stock="SNAP", action=OrderType.BUY, action_type=ActionType.LIMIT, quantity=100, price=100)

@pytest.fixture
def valid_SELL_LMT_order():
    """Валидный лимитный ордер"""
    return Order(stock="SNAP", action=OrderType.SELL, action_type=ActionType.LIMIT, quantity=100, price=100)

@pytest.fixture
def order_book():
    """Стакан с данными"""
    book = OrderBook(stock="SNAP")
    return book

@pytest.fixture
def exchange():
    """Биржа"""
    return Exchange()