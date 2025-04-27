import unittest
from unittest.mock import patch
from ssmts.data.loaders.stock_loader import StockLoader
from ssmts.data.store.stock_registry import StockRegistry
from ssmts.config.constants import DEFAULT_STOCKS
from ssmts.models.stock import Stock

# Mock data for testing
MOCK_DATA = [
    {"stockId": "STK1", "symbol": "TEA", "stockType": "common", "lastDivident": 0.0, "fixedDivident": 0.0, "parValue": 100.0, "currentPrice": 100.0},
    {"stockId": "STK2", "symbol": "POP", "stockType": "common", "lastDivident": 8.0, "fixedDivident": 0.0, "parValue": 100.0, "currentPrice": 120.0},
    {"stockId": "STK3", "symbol": "ALE", "stockType": "common", "lastDivident": 23.0, "fixedDivident": 0.0, "parValue": 60.0, "currentPrice": 80.0},
    {"stockId": "STK4", "symbol": "GIN", "stockType": "preferred", "lastDivident": 8.0, "fixedDivident": 0.02, "parValue": 100.0, "currentPrice": 90.0},
    {"stockId": "STK5", "symbol": "JOE", "stockType": "common", "lastDivident": 13.0, "fixedDivident": 0.0, "parValue": 250.0, "currentPrice": 110.0},
]

class TestStockLoader(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        patch('ssmts.data.loaders.stock_loader.StockLoader.getEntities', return_value=MOCK_DATA).start()

    def setUp(self):
        # Ensure the StockRegistry is empty before each test
        StockRegistry.UnregisterAll()

    def tearDown(self):
        # Clean up the StockRegistry after each test
        StockRegistry.UnregisterAll()
        super().tearDown()
        patch.stopall()
        

    
    def test_get_entities(self):
        # Act: Call the method to get entities
        entities = StockLoader.getEntities()

        # Assert: Check if the entities are as expected
        self.assertEqual(len(entities), len(MOCK_DATA))
        for entity in entities:
            self.assertIn(entity['stockId'], [stock['stockId'] for stock in MOCK_DATA])
      
    def test_load_stocks_into_registry(self):
        # Act: Load stocks using the StockLoader
        StockLoader.load()

        # Assert: Check if the stocks are loaded into the registry
        loaded_stocks = StockRegistry.get_all()
        self.assertEqual(len(loaded_stocks), 5)
        _stock = StockRegistry.get('STK1')
        self.assertTrue(_stock)
        self.assertIsInstance(_stock, Stock)
        self.assertEqual(_stock.symbol, "TEA")
        self.assertEqual(_stock.stockType, "common")
        self.assertEqual(_stock.lastDivident, 0.0)
        self.assertEqual(_stock.fixedDivident, 0.0)
        self.assertEqual(_stock.parValue, 100.0)
        self.assertEqual(_stock.currentPrice, 100.0)
        self.assertEqual(_stock.stockId, "STK1")

        self.assertFalse(StockRegistry.get("INVALID"))

        StockRegistry.UnregisterAll()
        self.assertFalse(StockRegistry.get("STK1"))
        self.assertEqual(len(StockRegistry.get_all()), 0)
    

if __name__ == '__main__':
    unittest.main()