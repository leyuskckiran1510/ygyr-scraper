from abc import ABC
from abc import abstractmethod

class Scraper(ABC):
    classes:list[str] = ['Aluminum Foil','Gym Bags']




    @abstractmethod
    def parser(self,html:str)->list[str]:
        """
        Parser for parsing the data fetched
        """
        ...

    @abstractmethod
    def scrape(self,keyword:str)->list[str]:
        """
        Scraper for specifc domain
        """
        ...

    @abstractmethod
    def data(self)->dict[str,list[str]]:
        """
        Scrape data generator
        """
        ...
