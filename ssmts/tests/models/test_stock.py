import unittest

from ssmts.models.stock import Stock 

class TestStock(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # This method is called once for the entire class, not for each test case.
        # You can set up any class-level resources here if needed.
        cls.stock = Stock(symbol="Test Stock", stockType="common", lastDivident=1.0, fixedDivident=0.0, parValue=100.0)

    def test_from_dict(self):
        # Test the from_dict method to ensure it populates the stock correctly
        data = {
            'stockId': 'STK1',
            'symbol': 'AAPL',
            'stockType': 'common',
            'lastDivident': 0.82,
            'fixedDivident': 0.0,
            'parValue': 100.0
        }
        stock = Stock.from_dict(data)
        self.assertIsInstance(stock, Stock)
        self.assertEqual(stock.stockId, 'STK1')
        self.assertEqual(stock.symbol, 'AAPL')
        self.assertEqual(stock.stockType, 'common')
        self.assertEqual(stock.lastDivident, 0.82)
        self.assertEqual(stock.fixedDivident, 0.0)
        self.assertEqual(stock.parValue, 100.0)

    def test_stock_initialization(self):

        stock = Stock(symbol="GOOGL", stockType="common", lastDivident=2.0, fixedDivident=0.0, parValue=1500.0)
        self.assertEqual(stock.symbol, "GOOGL")
        self.assertEqual(stock.stockType, "common")
        self.assertEqual(stock.lastDivident, 2.0)
        self.assertEqual(stock.fixedDivident, 0.0)
        self.assertEqual(stock.parValue, 1500.0)

if __name__ == "__main__":
    unittest.main()