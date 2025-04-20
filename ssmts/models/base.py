from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar('T')

class BaseModel(ABC, Generic[T]):
    """
    BaseModel is an abstract class that defines the interface for a model.
    It uses generics to allow for different types of models to be created.
    """

    @abstractmethod
    def from_dict(self, data: dict) -> T:
        """ Must be implemented by subclasses to create a model from a dictionary. """
        pass