import unittest
from datetime import datetime
from ssmts.models.trade import Trade

class TestTrade(unittest.TestCase):
    def setUp(self):
        """
        Set up test data for Trade tests.
        """
        self.valid_trade_data = {
            "tradeId": "T123",
            "stockId": "S456",
            "timeStamp": datetime.now(),
            "quantity": 100,
            "price": 50.5,
            "indicator": "buy"
        }

    def test_trade_initialization(self):
        """
        Test that a Trade instance is initialized correctly.
        """
        trade = Trade(**self.valid_trade_data)
        self.assertEqual(trade.tradeId, self.valid_trade_data["tradeId"])
        self.assertEqual(trade.stockId, self.valid_trade_data["stockId"])
        self.assertEqual(trade.quantity, self.valid_trade_data["quantity"])
        self.assertEqual(trade.price, self.valid_trade_data["price"])
        self.assertEqual(trade.indicator, self.valid_trade_data["indicator"])

    def test_trade_validation_invalid_quantity(self):
        """
        Test that Trade raises a ValueError for invalid quantity.
        """
        invalid_data = self.valid_trade_data.copy()
        invalid_data["quantity"] = 0
        with self.assertRaises(ValueError):
            Trade(**invalid_data)

    def test_trade_validation_invalid_price(self):
        """
        Test that Trade raises a ValueError for invalid price.
        """
        invalid_data = self.valid_trade_data.copy()
        invalid_data["price"] = -10
        with self.assertRaises(ValueError):
            Trade(**invalid_data)

    def test_trade_validation_invalid_indicator(self):
        """
        Test that Trade raises a ValueError for invalid indicator.
        """
        invalid_data = self.valid_trade_data.copy()
        invalid_data["indicator"] = "hold"
        with self.assertRaises(ValueError):
            Trade(**invalid_data)

    def test_trade_from_dict(self):
        """
        Test that a Trade instance can be created from a dictionary.
        """
        trade_dict = {
            "tradeId": "T789",
            "stockId": "S123",
            "timeStamp": datetime.now().isoformat(),
            "quantity": 200,
            "price": 75.0,
            "indicator": "sell"
        }
        trade = Trade.from_dict(Trade, trade_dict)
        self.assertEqual(trade.tradeId, trade_dict["tradeId"])
        self.assertEqual(trade.stockId, trade_dict["stockId"])
        self.assertEqual(trade.quantity, trade_dict["quantity"])
        self.assertEqual(trade.price, trade_dict["price"])
        self.assertEqual(trade.indicator, trade_dict["indicator"])

    def test_trade_equality(self):
        """
        Test that two Trade instances with the same attributes are equal.
        """
        trade1 = Trade(**self.valid_trade_data)
        trade2 = Trade(**self.valid_trade_data)
        self.assertEqual(trade1, trade2)

    def test_trade_string_representation(self):
        """
        Test the string representation of a Trade instance.
        """
        trade = Trade(**self.valid_trade_data)
        expected_str = (f"Trade ID: {self.valid_trade_data['tradeId']}, Stock ID: {self.valid_trade_data['stockId']}, "
                        f"Time: {trade.timeStamp}, Quantity: {self.valid_trade_data['quantity']}, "
                        f"Price: {self.valid_trade_data['price']}, Indicator: {self.valid_trade_data['indicator']}")
        self.assertEqual(str(trade), expected_str)


if __name__ == "__main__":
    unittest.main()