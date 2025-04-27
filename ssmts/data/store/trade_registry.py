

from ssmts.data.store.base_registry import BaseRegistry


class TradeRegistry(BaseRegistry):
    """
    Registry for managing trade entities.
    """
    STORE_NAME = "TRADES"
    # The STORE_NAME is used to identify the registry in the BaseRegistry class.