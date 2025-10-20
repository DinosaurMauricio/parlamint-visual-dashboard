from abc import ABC, abstractmethod


class BaseStatistics(ABC):

    @abstractmethod
    def calculate(self):
        pass
