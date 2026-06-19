from abc import ABC, abstractmethod

class Promotion(ABC):
    def __init__(self, promotion_text: str):
        self.__promotion_text = promotion_text
        self.__minimum_quantity = 0
        self.__active = True

    @abstractmethod
    def set_promotion(self):
        pass

    @abstractmethod
    def get_promotion(self):
        pass

    def __str__(self):
        return self.__promotion_text

    def activate_promotion(self):
        self.__active = True

    def deactivate(self):
        self.__active = False

    def get_minimum_quantity(self):
        return self.__minimum_quantity

    def is_active(self):
        return self.__active

    @abstractmethod
    def calc_price(self, price:float, quantity:int) -> float:
        pass

class SecondHalfPrice(Promotion):

    def __init__(self, promotion_text):
        super().__init__(promotion_text)
        self._minimum_quantity = 2


    def set_promotion(self):
        pass

    def get_promotion(self) -> Promotion:
        pass

    def calc_price(self, quantity:int, price:float) -> float:
        return quantity * price - (quantity//2 * price * 0.5)


class ThirdOneFree(Promotion):

    def __init__(self, promotion_text):
        super().__init__(promotion_text)
        self.__minimum_quantity = 3

    def set_promotion(self):
        pass

    def get_promotion(self):
        pass

    def calc_price(self, price:float, quantity:int) -> float:
        return (quantity - (quantity//3)) * price


class PercentDiscount(Promotion):

    def __init__(self, promotion_text:str, percent:float):
        super().__init__(promotion_text)
        self.__discount = percent/100

    def set_promotion(self):
        pass

    def get_promotion(self):
        pass

    def calc_price(self, price:float, quantity:int) -> float:
        return (quantity * price) - (quantity * price) * self.__discount