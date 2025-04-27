
from ssmts.data.store.base_registry import BaseRegistry
from ssmts.models.trade import Trade
from ssmts.models.trade_snapshot import TradeSnapShot
import threading
from datetime import datetime
from collections import deque
 

class TradeSnapShotRegistry(BaseRegistry[TradeSnapShot]):
    """
    A registry for storing trade snapshots.
    """

    STORE_NAME = "TRADE_SNAPSHOTS"
    _updated_snapshots = deque(maxlen=15)  # deque to keep track of latest snapshots

    @classmethod
    def add_trades(cls, key, trades):
        """
        Adds a trade snapshot to the SNAPSHOTS list.
        """
        with threading.Lock():
            if not isinstance(trades, list):
                raise TypeError("Trades must be a list of Trade instances.")
            cls._store[cls.STORE_NAME].update({key: TradeSnapShot(key, datetime.now(), trades)})

    @classmethod
    def update_trade(cls, entityId: str, trade: Trade) -> None:
        """
        Update an instance in the registry.
        """
        with threading.Lock():
            if not isinstance(trade, Trade):
                raise TypeError("Trade must be an instance of Trade.")
            if entityId not in cls._store[cls.STORE_NAME]:
                # Create a new snapshot if it doesn't exist
                # ideally use add_trades method to add a new snapshot
                cls.add_trades(entityId, [trade])
            else:
                # Update the existing snapshot
                tradeSnapShot = cls._store[cls.STORE_NAME][entityId]
                tradeSnapShot.add_trade(trade)  # Assuming trades is a Trade instance
                tradeSnapShot.snapshot_time = datetime.now()
                cls._updated_snapshots.append(entityId)