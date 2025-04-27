
import math
from ssmts.config.constants import StockType
from ssmts.data.store.stock_registry import StockRegistry
from ssmts.data.store.trade_snapshot_registry import TradeSnapShotRegistry


class StockUtils:

    @staticmethod
    def _get_stock(stock_id: str):
        """
        Retrieve the stock object for a given stock ID.

        :param stock_id: The ID of the stock.
        :return: The stock object.
        """
        stock = StockRegistry.get(stock_id)
        if not stock:
            raise ValueError(f"Stock with ID {stock_id} not found.")
        return stock

    @staticmethod
    def calculate_dividend_yield(stock_id:str, stock_price: float) -> float:
        """
        Calculate the dividend yield of a stock.

        :param stock_id: The ID of the stock.
        :param stock_price: The current stock price.
        :return: The dividend yield as a percentage.
        """
        _stock = StockUtils._get_stock(stock_id)
        dividend = _stock.lastDivident if _stock.stockType == StockType.COMMON.value else _stock.fixedDivident * _stock.parValue
        
        if dividend is None:
            raise ValueError(f"Dividend for stock ID {stock_id} not found.")
        if dividend < 0:
            raise ValueError("Dividend cannot be negative.")
        if stock_price < 0:
            raise ValueError("Stock price cannot be negative.")
        if stock_price == 0:
            raise ValueError("Stock price cannot be zero.")
        
        return dividend / stock_price
    

    def calculate_pe_ratio(stock_id: str, stock_price: float) -> float:
        """
        Calculate the Price-to-Earnings (P/E) ratio of a stock.

        :param stock_id: The ID of the stock.
        :param stock_price: The current stock price.
        :return: The P/E ratio.
        """
        dividend = StockUtils._get_stock(stock_id).lastDivident
        
        if dividend is None:
            raise ValueError(f"Dividend for stock ID {stock_id} not found.")
        if dividend < 0:
            raise ValueError("Dividend cannot be negative.")
        if stock_price < 0:
            raise ValueError("Stock price cannot be negative.")
        if dividend == 0:
            raise ValueError("Dividend cannot be zero.")
        return stock_price / dividend
    

    @staticmethod
    def _geometric_mean(prices: list) -> float:
        """
        Calculate the geometric mean of a list of prices.

        :param prices: A list of stock prices.
        :return: The geometric mean.
        """
        if not prices:
            raise ValueError("Price list cannot be empty.")
        if any(price <= 0 for price in prices):
            raise ValueError("All prices must be positive.")
        
        product = math.prod(prices)
        n = len(prices)
        return product ** (1/n)
    

    @staticmethod
    def calculate_all_share_index() -> float:
        """
        Calculate the All Share Index (ASI) based on a list of stock prices.

        :param prices: A list of stock prices.
        :return: The All Share Index.
        """
        prices = list(map(lambda stock_id: StockRegistry.get(stock_id).currentPrice, StockRegistry.get_all()))
        return StockUtils._geometric_mean(prices)
    
    @staticmethod
    def calculate_vwsp(stock_id: str) -> float:
        """
        Calculate the Volume Weighted Stock Price (VWSP) for a given stock ID based on the last 15 trades.
        this should be updated in real-time based on the incoming trades and snapshot.

        :param stock_id: The ID of the stock.
        :return: The VWSP.
        """
        snapShot = TradeSnapShotRegistry.get(stock_id) ### Get the snapshot of the stock (having latest 15 trades)
        trades = snapShot.trades if snapShot else []
        
        if not trades:
            raise ValueError(f"No trades found for stock ID {stock_id}.")

        total_price = sum(trade.price * trade.quantity for trade in trades)
        total_quantity = sum(trade.quantity for trade in trades)
        
        if total_quantity == 0:
            raise ValueError("Total quantity cannot be zero.")
        
        return total_price / total_quantity

