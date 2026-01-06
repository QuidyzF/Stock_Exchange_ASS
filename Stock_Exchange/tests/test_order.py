import pytest
from src.order import Order
from tests.conftest import valid_SELL_LMT_order, valid_BUY_LMT_order, valid_SELL_MKT_order


class TestMarketOrderCreation:
    """Тесты для рыночных ордеров"""
    def test_create_MKT_order(self, valid_BUY_MKT_order):
        """Проверка валидности созданного заказа"""
        assert valid_BUY_MKT_order.stock == "SNAP"
        assert valid_BUY_MKT_order.action == "BUY"
        assert valid_BUY_MKT_order.action_type == "MKT"
        assert valid_BUY_MKT_order.quantity == 100
        assert valid_BUY_MKT_order.price is None

    def test_has_unique_id(self):
        """Каждый ордер имеет уникальный id"""
        order_1 = Order(stock="SNAP", action="BUY", action_type="MKT", quantity=100)
        order_2 = Order(stock="SNAP", action="BUY", action_type="MKT", quantity=100)
        assert order_1.id != order_2.id
        assert order_1.id < order_2.id

    def test_start_order_status(self, valid_BUY_MKT_order):
        assert valid_BUY_MKT_order.status == "PENDING"

    def test_start_zero_filled_quantity(self, valid_BUY_MKT_order):
        assert valid_BUY_MKT_order.filled_quantity == 0

    def test_start_execution_status(self, valid_BUY_MKT_order):
        assert valid_BUY_MKT_order.execution_price is None

class TestMarketOrderValidation:
    def test_without_price_parameter(self, valid_BUY_MKT_order):
        """MKT не должен принимать цену"""
        with pytest.raises(ValueError):
            Order(stock="SNAP", action="BUY", action_type="MKT", quantity=100, price=100)

    def test_order_requires_quantity_parameter(self):
        with pytest.raises(TypeError):
            Order(stock="SNAP", action="BUY", action_type="MKT")

    def test_validation_reject_zero_quantity(self):
        with pytest.raises(ValueError):
            Order(stock="SNAP", action="BUY", action_type="MKT", quantity=0)

    def test_validation_reject_negative_quantity(self):
        with pytest.raises(ValueError):
            Order(stock="SNAP", action="BUY", action_type="MKT", quantity=-100)

class TestLimitedOrder:
    """Тесты для лимитных ордеров"""
    def test_create_LMT_order(self, valid_BUY_LMT_order):
        """Проверка валидности созданного заказа"""
        assert valid_BUY_LMT_order.stock == "SNAP"
        assert valid_BUY_LMT_order.action == "BUY"
        assert valid_BUY_LMT_order.action_type == "LMT"
        assert valid_BUY_LMT_order.quantity == 100
        assert valid_BUY_LMT_order.price is 100

    def test_has_unique_id(self):
        """Каждый ордер имеет уникальный id"""
        order_1 = Order(stock="SNAP", action="BUY", action_type="LMT", quantity=100, price=100)
        order_2 = Order(stock="SNAP", action="BUY", action_type="LMT", quantity=100, price=100)
        assert order_1.id != order_2.id
        assert order_1.id < order_2.id

    def test_start_order_status(self, valid_BUY_LMT_order):
        assert valid_BUY_LMT_order.status == "PENDING"

    def test_start_zero_filled_quantity(self, valid_BUY_LMT_order):
        assert valid_BUY_LMT_order.filled_quantity == 0

    def test_start_execution_status(self, valid_BUY_LMT_order):
        assert valid_BUY_LMT_order.execution_price is None

class TestLimitedOrderPricing:
    @pytest.mark.parametrize("action_type, price, should_fail", [
        ("LMT", None, True),
        ("LMT", 0, True),
        ("LMT", 100, False),
        ("LMT", -100, True)
    ],
     ids=[
         "LMT | None | Fail",
         "LMT | 0 | Pass",
         "LMT | 100 | Pass",
         "LMT | -100 | Pass"
     ])
    def test_order_price_validation(self, action_type, price, should_fail):
        """Проверка валидации цены для разных типов ордеров"""
        if should_fail:
            with pytest.raises(ValueError):
                Order(stock="SNAP", action="BUY", action_type=action_type, quantity=100, price=price)
        else:
            order = Order(stock="SNAP", action="BUY", action_type=action_type, quantity=100, price=price)
            assert order.action_type == action_type
            assert order.price == price

class TestOrderQuantity:
    @pytest.mark.parametrize("quantity, status_expected, should_fail", [
        (0, "PENDING", True),
        (50, "PARTIAL", False),
        (100, "FILLED", False),
        (-100, "PENDING", True)
    ])
    def test_order_quantity_min_max(self, quantity, status_expected, should_fail):
        if should_fail:
            with pytest.raises(ValueError):
                Order(stock="SNAP", action="BUY", action_type="LMT", quantity=quantity, price=100)
        else:
            order = Order(stock="SNAP", action="BUY", action_type="LMT", quantity=quantity, price=100)
            assert order.quantity == quantity