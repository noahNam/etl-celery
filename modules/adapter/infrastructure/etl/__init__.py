from abc import ABC, abstractmethod


class Transfer(ABC):
    @abstractmethod
    def start_transfer(self, *args, **kwargs):
        """
        기능 : 추출된 데이터를 변환 하는 과정

        return: 추출된 결과 데이터를 리턴함
        """
        pass
