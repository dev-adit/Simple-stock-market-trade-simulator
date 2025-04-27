from abc import ABC, abstractmethod
from typing import TypeVar, Generic
from ssmts.data.store.base_registry import BaseRegistry
import logging

from ssmts.models.base import BaseModel


T = TypeVar('T')

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class BaseLoader(ABC, Generic[T]):
    """
    BaseLoader is an abstract class that defines the interface for loading data into a registry.
    It uses generics to allow for different types of entities to be loaded.
    """
    PRIMARY_KEY: str = None  # Primary key for the entity, to be defined in subclasses
    ENTITY: BaseModel = None  # Entity class, to be defined in subclasses
    ENTITY_STORE: BaseRegistry = None  # Registry class, to be defined in subclasses
    
    @abstractmethod
    def getEntities(cls) -> list[dict]:
        """ Must be implemented by subclasses to return a list of entities. """
        pass

    @classmethod
    def load(cls):
        """ Loading stock data """
        entities = cls.getEntities()
        for entityData in entities:
            cls.ENTITY_STORE.add(entityData[cls.PRIMARY_KEY], cls.ENTITY.from_dict(entityData))
            logger.info(f"Loaded entity: {entityData[cls.PRIMARY_KEY]}")
        logger.info("All entities loaded successfully.")

