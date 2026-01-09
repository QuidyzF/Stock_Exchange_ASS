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

class TestLimitedOrderCreation:
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

class TestLimitedOrderValidation:
    def test_requires_price_parameter(self):
        with pytest.raises(ValueError):
            Order(stock="SNAP", action="BUY", action_type="LMT", quantity=100)

    def test_rejects_zero_price(self):
        with pytest.raises(ValueError):
            Order(stock="SNAP", action="BUY", action_type="LMT", quantity=100, price=0)

    def test_rejects_negative_price(self):
        with pytest.raises(ValueError):
            Order(stock="SNAP", action="BUY", action_type="LMT", quantity=100, price=-100)

class TestLimitedOrderMethods:
    def test_get_quantity_function(self, valid_BUY_LMT_order):
        assert valid_BUY_LMT_order.get_quantity() == 100

        valid_BUY_LMT_order.filled_quantity = 30
        assert valid_BUY_LMT_order.get_quantity() == 70

        valid_BUY_LMT_order.filled_quantity = 50
        assert valid_BUY_LMT_order.get_quantity() == 50

        valid_BUY_LMT_order.filled_quantity = 100
        assert valid_BUY_LMT_order.get_quantity() == 0

    def test_filling_update_function(self, valid_BUY_LMT_order):
        valid_BUY_LMT_order.filling_update(50)
        assert valid_BUY_LMT_order.filled_quantity == 50

        valid_BUY_LMT_order.filling_update(30)
        assert valid_BUY_LMT_order.filled_quantity == 80

    def test_filling_update_function_partial_status(self, valid_BUY_LMT_order):
        valid_BUY_LMT_order.filling_update(50)
        assert valid_BUY_LMT_order.status == "PARTIAL"

    def test_filling_update_function_filled_status(self, valid_BUY_LMT_order):
        valid_BUY_LMT_order.filling_update(100)
        assert valid_BUY_LMT_order.status == "FILLED"

    def test_filling_update_function_rejects_zero_parameter(self, valid_BUY_LMT_order):
        with pytest.raises(ValueError):
            valid_BUY_LMT_order.filling_update(0)

    def test_filling_update_with_overfill(self, valid_BUY_LMT_order):
        with pytest.raises(ValueError):
            valid_BUY_LMT_order.filling_update(150)

    def test_filling_update_status_changing(self, valid_BUY_LMT_order):
        assert valid_BUY_LMT_order.status == "PENDING"

        valid_BUY_LMT_order.filling_update(30)
        assert valid_BUY_LMT_order.status == "PARTIAL"

        valid_BUY_LMT_order.filling_update(50)
        assert valid_BUY_LMT_order.status == "PARTIAL"

        valid_BUY_LMT_order.filling_update(20)
        assert valid_BUY_LMT_order.status == "FILLED"