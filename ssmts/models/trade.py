
from datetime import datetime
from ssmts.config.constants import TradeType
from ssmts.models.base import BaseModel


class Trade(BaseModel):
    """
    Trade class representing a trade in the system.
    """

    def __init__(self, tradeId: str, stockId: str, timeStamp: datetime, quantity: int, price: float, indicator: str):
        """
        Initializes a Trade instance with the given attributes.
        Record a trade, with timestamp, quantity of shares, buy or sell indicator and
        traded price
        """
        self.tradeId = tradeId
        self.stockId = stockId
        self.timeStamp = timeStamp
        self.quantity = quantity
        self.price = price
        self.indicator = indicator
        self.validate_trade()

    def validate_trade(self):
        """
        Validates the trade attributes to ensure they meet the required criteria.
        """
        if self.quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
        if self.price <= 0:
            raise ValueError("Price must be greater than zero.")
        if self.indicator not in [t.value for t in TradeType]:
            raise ValueError("Indicator must be 'buy' or 'sell'.")

    @classmethod
    def from_dict(cls, data):
        """
        Populates the Trade instance from a dictionary.
        """
        trade = cls(
            tradeId=data.get('tradeId'),
            stockId=data.get('stockId'),
            timeStamp=datetime.fromisoformat(data.get('timestamp')) if data.get('timestamp') else datetime.now(),
            quantity=data.get('quantity'),
            price=data.get('price'),
            indicator=data.get('indicator')
        )
        return trade
    
    def __str__(self):
        """
        Returns a string representation of the Trade instance.
        """
        return f"Trade ID: {self.tradeId}, Stock ID: {self.stockId}, Time: {self.timeStamp}, Quantity: {self.quantity}, Price: {self.price}, Indicator: {self.indicator}"
    
    def __eq__(self, other):
        """
        Compares two Trade instances for equality.
        """
        if not isinstance(other, Trade):
            return False
        return (self.tradeId == other.tradeId and
                self.stockId == other.stockId and
                self.timeStamp == other.timeStamp and
                self.quantity == other.quantity and
                self.price == other.price and
                self.indicator == other.indicator)

    def __repr__(self):
        return f"Trade(tradeId={self.tradeId}, stockId={self.stockId}, timeStamp={self.timeStamp}, quantity={self.quantity}, price={self.price}, indicator={self.indicator})"