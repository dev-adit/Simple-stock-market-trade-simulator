
from ssmts.data.store.base_registry import BaseRegistry
import threading
from datetime import datetime


class StockRegistry(BaseRegistry):
    """
    Registry for managing stock entities.
    """
    STORE_NAME = "STOCKS"
    

    @classmethod
    def update_stock_price(cls, stock_id: str, price: float) -> None:
        """
        Update the stock price for a given stock ID.
        
        :param stock_id: The ID of the stock.
        :param price: The new price of the stock.
        """
        with threading.Lock():
            if stock_id in cls._store[cls.STORE_NAME]:
                cls._store[cls.STORE_NAME][stock_id].currentPrice = price
                cls._store[cls.STORE_NAME][stock_id].lastTradeTime = datetime.now()
                print(f"Stock {stock_id} price updated to {price}.")
            else:
                print(f"Stock {stock_id} not found in registry.")
