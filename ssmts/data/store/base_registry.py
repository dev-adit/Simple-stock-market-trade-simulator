from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from ssmts.models.base import BaseModel

T = TypeVar("T", bound="BaseModel")

class BaseRegistry(ABC, Generic[T]):
    """
    Base class for a registry that stores and manages instances of a entities.
    """
    _store: dict[str, dict[str,T]] = {} # for e.g. {"STOCKS" : {"STK1": StockObj, "STK2": StockObj}}

    STORE_NAME: str = None # Default store name

    @classmethod
    def register(cls, entityId: str, instance: T) -> None:
        """
        Register an instance with a name.
        """
        cls._store[cls.STORE_NAME][entityId] = instance

    @classmethod
    def add(cls, entityId: str, instance: T) -> None:
        """
        Add an instance to the registry.
        """
        if cls.STORE_NAME not in cls._store:
            cls._store[cls.STORE_NAME] = {}
        if entityId in cls._store[cls.STORE_NAME]:
            raise ValueError(f"Entity ID {entityId} already exists in {cls.STORE_NAME}.")   
        cls.register(entityId, instance)

    @classmethod
    def get(cls, entityId: str) -> T:
        """
        Retrieve an entity instance by its ID.
        """
        return cls._store[cls.STORE_NAME].get(entityId) or None

    @classmethod
    def get_all(cls) -> dict[str,T]:
        """
        Retrieve all entities.
        """
        return cls._store.get(cls.STORE_NAME, {})

    @classmethod
    def unregister(cls, entityId: str) -> None:
        """
        Unregister an entity instance by its ID.
        """
        if entityId not in cls._store[cls.STORE_NAME]:
            raise ValueError(f"Entity ID {entityId} does not exist in {cls.STORE_NAME}.")
        del cls._store[cls.STORE_NAME][entityId]

    @classmethod
    def UnregisterAll(cls) -> None:
        """
        Unregister all entities in the registry.
        """
        cls._store[cls.STORE_NAME] = {}
        # Clear the store for the specific store name