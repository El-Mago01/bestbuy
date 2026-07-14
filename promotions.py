from abc import ABC, abstractmethod


class Promotion(ABC):
    """Promotion abstract class defining the promotion interface"""

    def __init__(self, promotion_text: str):
        self.__promotion_text = promotion_text
        self.__minimum_quantity = 0 #Defines how many products need to be in stock for the specific promotion
        self.__active = True

    @abstractmethod
    def set_promotion(self):
        """Set promotion method"""

    @abstractmethod
    def get_promotion(self):
        """Get promotion method"""

    def __str__(self):
        """String representation"""
        return self.__promotion_text

    def activate_promotion(self):
        """Activate promotion"""
        self.__active = True

    def deactivate(self):
        """Deactivate promotion"""
        self.__active = False

    def get_minimum_quantity(self):
        """Get minimum quantity"""
        return self.__minimum_quantity

    def is_active(self):
        """Is active method"""
        return self.__active

    @abstractmethod
    def calc_price(self, price: float, quantity: int) -> float:
        """Calculate price"""


class SecondHalfPrice(Promotion):
    """Second half price promotion class based on Promotion interface"""

    def __init__(self, promotion_text):
        super().__init__(promotion_text)
        self._minimum_quantity = 2

    def set_promotion(self):
        pass

    def get_promotion(self) -> Promotion:
        pass

    def calc_price(self, price: float, quantity: int) -> float:
        """Calculate price for this specific promotion"""
        return quantity * price - (quantity // 2 * price * 0.5)


class ThirdOneFree(Promotion):
    """'Third one free' promotion class based on Promotion interface"""

    def __init__(self, promotion_text):
        super().__init__(promotion_text)
        self.__minimum_quantity = 3

    def set_promotion(self):
        pass

    def get_promotion(self):
        pass

    def calc_price(self, price: float, quantity: int) -> float:
        """Calculate price for this specific promotion"""

        return (quantity - (quantity // 3)) * price


class PercentDiscount(Promotion):
    """Percent discount promotion class based on Promotion interface"""

    def __init__(self, promotion_text: str, percent: float):
        super().__init__(promotion_text)
        self.__discount = percent / 100

    def set_promotion(self):
        pass

    def get_promotion(self):
        pass

    def calc_price(self, price: float, quantity: int) -> float:
        return (quantity * price) - (quantity * price) * self.__discount
