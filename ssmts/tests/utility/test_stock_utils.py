import math
import unittest
from unittest.mock import patch, MagicMock
from ssmts.data.loaders.stock_loader import StockLoader
from ssmts.utility.stock_utils import StockUtils
from ssmts.config.constants import StockType
from ssmts.data.store.stock_registry import StockRegistry


class TestStockUtils(unittest.TestCase):
    MOCK_DATA = [
            {
                "stockId": "STK1",
                "symbol": "TEST1",
                "stockType": StockType.COMMON.value,
                "lastDivident": 10,
                "fixedDivident": None,
                "parValue": 100,
                "currentPrice": 100
            },
            {
                "stockId": "STK2",
                "symbol": "TEST2",
                "stockType": StockType.PREFERRED.value,
                "lastDivident": 20,
                "fixedDivident": 0.02,
                "parValue": 200,
                "currentPrice": 200
            },
            {
                "stockId": "STK3",
                "symbol": "TEST3",
                "stockType": StockType.COMMON.value,
                "lastDivident": 15,
                "fixedDivident": None,
                "parValue": 150,
                "currentPrice": 300
            }
        ]
    
    @classmethod
    def setUpClass(cls):
        patch('ssmts.data.loaders.stock_loader.StockLoader.getEntities', return_value=cls.MOCK_DATA).start()
        StockLoader.load()

    @classmethod
    def tearDownClass(cls):
        # Unregister all stocks from the registry
        StockRegistry.UnregisterAll()
        patch.stopall()

    def test_calculate_dividend_yield_common_stock(self):
        result = StockUtils.calculate_dividend_yield("STK1", 100)
        self.assertEqual(result, 0.1)

    def test_calculate_dividend_yield_preferred_stock(self):
        result = StockUtils.calculate_dividend_yield("STK2", 100)
        self.assertEqual(result, 0.04)

    def test_calculate_dividend_yield_invalid_stock_price(self):
        with self.assertRaises(ValueError):
            StockUtils.calculate_dividend_yield("STK1", 0)

    def test_calculate_pe_ratio(self):
        result = StockUtils.calculate_pe_ratio("STK1", 100)
        self.assertEqual(result, 10)

    def test_calculate_pe_ratio_zero_dividend(self):
        # Temporarily modify the stock data for this test
        StockRegistry.get("STK1").lastDivident = 0
        with self.assertRaises(ValueError):
            StockUtils.calculate_pe_ratio("STK1", 100)

    def test_calculate_all_share_index(self):
        # Update current prices to test variations
        StockRegistry.get("STK1").set_current_price(150)
        StockRegistry.get("STK2").set_current_price(250)
        StockRegistry.get("STK3").set_current_price(350)

        result = StockUtils.calculate_all_share_index()
        expected_result = math.prod([150, 250, 350])
        expected_result = expected_result ** (1/3)
        self.assertAlmostEqual(result, expected_result, places=3)

    def test_geometric_mean(self):
        prices = [100, 200, 300]
        result = StockUtils._geometric_mean(prices)
        expected_result = math.prod(prices) ** (1/3)
        self.assertAlmostEqual(result, expected_result, places=3)

    def test_geometric_mean_empty_list(self):
        with self.assertRaises(ValueError):
            StockUtils._geometric_mean([])

    def test_geometric_mean_negative_price(self):
        with self.assertRaises(ValueError):
            StockUtils._geometric_mean([100, -200, 300])


if __name__ == '__main__':
    unittest.main()
