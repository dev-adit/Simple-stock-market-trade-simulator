
from datetime import datetime
from ssmts.config.constants import TradeType
from ssmts.models.base import BaseModel
from ssmts.models.trade import Trade
from collections import deque


class TradeSnapShot(BaseModel):
    """
    Trade Snapshot class representing a trade in the system.
    """
    MAX_LENGTH = 15

    def __init__(self, stockId: str, snapshot_time: datetime, trades: list[Trade], max_length = MAX_LENGTH):
        """
        Initializes a TradeSnapshot instance with the given attributes.
        Record a trade, with timestamp, quantity of shares, buy or sell indicator and
        traded price
        """
        self.stockId = stockId
        self.snapshot_time = snapshot_time
        self.max_length = max_length
        self.trades = deque(maxlen=max_length)  # Use deque for efficient appending and popping
        self.add_trades(trades)

    def add_trades(self, trades: list[Trade]):
        """
        Adds multiple trades to the snapshot. If the snapshot exceeds the max length, the oldest trades are removed.
        """
        if not isinstance(trades, list):
            raise TypeError("Trades must be a list of Trade instances.")
        
        for trade in trades:
            self.add_trade(trade)

    def add_trade(self, trade: Trade):
        """
        Adds a trade to the snapshot. If the snapshot exceeds the max length, the oldest trade is removed.
        """
        if not isinstance(trade, Trade):
            raise TypeError("Trade must be an instance of Trade.")
        
        self.trades.append(trade)
        self.snapshot_time = datetime.now() ## Update the snapshot time to the current time

    @classmethod
    def from_dict(cls, data):
        """
        Populates the Tradesnapshot instance from a dictionary.
        """
        trade = cls(
            stockId=data.get('stockId'),
            snapshot_time=datetime.fromisoformat(data.get('snapshot_time')) if data.get('snapshot_time') else datetime.now(),
            trades=[Trade.from_dict(trade_data) for trade_data in data.get('trades', [])]
        )
        return trade
    
    
    def to_dict(self):
        """
        Converts the TradeSnapshot instance to a dictionary.
        """
        return {
            'stockId': self.stockId,
            'snapshot_time': self.snapshot_time.isoformat(),
            'trades': [trade.to_dict() for trade in self.trades]
        }
    
    def __str__(self):
        """
        Returns a string representation of the TradeSnapshot instance.
        """
        return f"Stock ID: {self.stockId}, Snapshot Time: {self.snapshot_time}, Trades: {self.trades}"
    
    def __eq__(self, other):
        """
        Compares two TradeSnapshot instances for equality.
        """
        if not isinstance(other, TradeSnapShot):
            return False
        return (self.stockId == other.stockId and
                self.snapshot_time == other.snapshot_time)

    def __repr__(self):
        return f"TradeSnapshot(stockId={self.stockId}, snapshot_time={self.snapshot_time}, trades={self.trades})"