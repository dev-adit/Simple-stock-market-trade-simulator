

"""
Stock class for representing stock attributes and methods.
This module defines the Stock class, which includes attributes such as symbol, stockType,
lastDivident, fixedDivident, and parValue. It also provides methods for initializing a stock instance,
populating it from a dictionary, and comparing instances for equality. 

Test:
"""


from ssmts.models.base import BaseModel


class Stock(BaseModel):
    """
    Represents a stock with its attributes and methods for manipulation.
    """
    def __init__(self, stockId=None, symbol=None, stockType=None, lastDivident=None, fixedDivident=None,\
                 parValue=None, currentPrice=None, lastTradeTime=None):
        """
        Initializes a Stock instance with the given attributes.
        
        :param stockId: The unique identifier for the stock.
        :param symbol: The stock symbol (e.g., "AAPL").
        :param stockType: The type of stock (e.g., "common", "preferred").
        :param lastDivident: The last dividend paid by the stock.
        :param fixedDivident: The fixed dividend rate for preferred stocks.
        :param parValue: The par value of the stock.
        """
        # Default values for attributes
        self.stockId = stockId if stockId is not None else ''
        self.symbol = symbol if symbol is not None else ''
        self.stockType = stockType if stockType is not None else ''
        self.lastDivident = lastDivident if lastDivident is not None else 0.0
        self.fixedDivident = fixedDivident if fixedDivident is not None else 0.0
        self.parValue = parValue if parValue is not None else 0.0
        self.currentPrice = currentPrice if currentPrice is not None else 0.0
        self.lastTradeTime = lastTradeTime if lastTradeTime is not None else None
        
    def get_last_trade_time(self):
        """
        Returns the last trade time of the stock.
        
        :return: The last trade time.
        """
        return self.lastTradeTime

    @classmethod
    def from_dict(cls, data):
        """
        Populates the Stock instance from a dictionary.
        """
        stock = cls()
        stock.stockId = data.get('stockId')
        stock.symbol = data.get('symbol')
        stock.stockType = data.get('stockType')
        stock.lastDivident = data.get('lastDivident')
        stock.fixedDivident = data.get('fixedDivident')
        stock.parValue = data.get('parValue')
        stock.currentPrice = data.get('currentPrice')
        stock.lastTradeTime = data.get('lastTradeTime')
        return stock
    
    def to_dict(self):
        """
        Converts the Stock instance to a dictionary.
        
        :return: A dictionary representation of the Stock instance.
        """
        return {
            'stockId': self.stockId,
            'symbol': self.symbol,
            'stockType': self.stockType,
            'lastDivident': self.lastDivident,
            'fixedDivident': self.fixedDivident,
            'parValue': self.parValue,
            'currentPrice': self.currentPrice,
            'lastTradeTime': self.lastTradeTime,
        }
    
    def set_current_price(self, currentPrice):
        """
        Sets the current price of the stock.
        
        :param currentPrice: The current price of the stock.
        """
        if currentPrice < 0:
            raise ValueError("Current price cannot be negative.")
        self.currentPrice = currentPrice
                
    def __str__(self):
        """
        Returns a string representation of the Stock instance.
        """
        return f"Stock(stockId={self.stockId}, symbol={self.symbol}, stockType={self.stockType}, lastDivident={self.lastDivident}, fixedDivident={self.fixedDivident}, parValue={self.parValue})"
    
    def __repr__(self):
        """
        Returns a string representation of the Stock instance for debugging.
        """
        return self.__str__()
    
    def __eq__(self, other):
        """
        Compares two Stock instances for equality.
        """
        if not isinstance(other, Stock):
            return False
        return (self.stockId == other.stockId and
                self.symbol == other.symbol and
                self.stockType == other.stockType and
                self.lastDivident == other.lastDivident and
                self.fixedDivident == other.fixedDivident and
                self.parValue == other.parValue)
    
    