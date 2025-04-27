

from ssmts.data.loaders.base_loader import BaseLoader
from ssmts.data.store.trade_snapshot_registry import TradeSnapShotRegistry
from ssmts.models.trade import Trade
from ssmts.models.trade_snapshot import TradeSnapShot
from datetime import datetime
from threading import Lock


class TradeSnapshotLoader(BaseLoader):
    """
    TradeSnapshotLoader is responsible for loading trade snapshot data into the TradeSnapshotRegistry.
    It uses the BaseLoader interface to ensure that all loaders implement the load method.
    """
    
    PRIMARY_KEY = "stockId"
    ENTITY = TradeSnapShot  # Assuming TradeSnapshot is defined in ssmts.models.trade_snapshot
    ENTITY_STORE = TradeSnapShotRegistry  # Assuming TradeSnapshotRegistry is defined in ssmts.data.store.trade_snapshot_registry
    
    SNAPSHOTS = {}
                

    @classmethod
    def getEntities(cls):
        """
        Returns a list of trade snapshot entities. This can be replaced with a database call or any other data source.
        """
        with Lock():
            # Return the list of snapshots
            return cls.SNAPSHOTS  # Replace with actual data source if needed
      