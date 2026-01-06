import pytest
from src.order import Order
from src.order_book import OrderBook
from src.exchange import Exchange


#def pytest_runtest_setup(item):
#    """Запускается перед каждым тестом"""
#    print(f"\n> Starting test: {item.name}")

#def pytest_runtest_teardown(item):
#    """Запускается после каждого теста"""
#    print(f"\n> Finished test: {item.name}")

@pytest.fixture
def valid_BUY_MKT_order():
    """Валидный рыночный ордер"""
    return Order(stock="SNAP", action="BUY", action_type="MKT", quantity=100)

@pytest.fixture
def valid_SELL_MKT_order():
    """Валидный рыночный ордер"""
    return Order(stock="SNAP", action="SELL", action_type="MKT", quantity=100)

@pytest.fixture
def valid_BUY_LMT_order():
    """Валидный лимитный ордер"""
    return Order(stock="SNAP", action="BUY", action_type="LMT", quantity=100, price=100)

@pytest.fixture
def valid_SELL_LMT_order():
    """Валидный лимитный ордер"""
    return Order(stock="SNAP", action="SELL", action_type="LMT", quantity=100, price=100)

@pytest.fixture
def order_book():
    """Стакан с данными"""
    book = OrderBook(stock="SNAP")
    return book

@pytest.fixture
def exchange():
    """Биржа"""
    return Exchange()