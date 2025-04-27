
import logging

from ssmts.data.loaders.base_loader import BaseLoader
from ssmts.data.store.trade_registry import TradeRegistry
from ssmts.models.trade import Trade


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class TradeLoader(BaseLoader[Trade]):
    """
    TradeLoader is responsible for loading trade data into the TradeRegistry.
    It uses the BaseLoader interface to ensure that all loaders implement the load method.
    """
    
    PRIMARY_KEY = "tradeId"
    ENTITY: Trade = Trade
    ENTITY_STORE = TradeRegistry  # The registry where the trade entities will be stored, to be defined later
    
    INCOMING_TRADE = []

    @classmethod
    def getEntities(cls):
        """
        Returns a list of trade entities. This can be replaced with a database call or any other data source.
        """
        # Placeholder for actual data source, replace with actual implementation
        return cls.INCOMING_TRADE  # Replace with actual data source if needed
    