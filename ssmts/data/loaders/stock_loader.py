
from ssmts.config.constants import DEFAULT_STOCKS
from ssmts.data.loaders.base_loader import BaseLoader
from ssmts.data.store.stock_registry import StockRegistry
from ssmts.models.stock import Stock
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class StockLoader(BaseLoader[Stock]):
    """
    StockLoader is responsible for loading stock data into the StockRegistry.
    It uses the BaseLoader interface to ensure that all loaders implement the load method.
    """
    
    PRIMARY_KEY = "stockId"
    ENTITY: Stock = Stock
    ENTITY_STORE = StockRegistry  # The registry where the stock entities will be stored
    
    @classmethod
    def getEntities(cls):
        """
        Returns a list of stock entities. This can be replaced with a database call or any other data source.
        """
        return DEFAULT_STOCKS  # Replace with actual data source if needed
