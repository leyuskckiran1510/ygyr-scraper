# Scraping Sources
1. https://www.world.org/weo/recycle


# Scraper Structure:
 Import the abstract `Scrape` class from  `scraper.py` and
 use it as parent classes in the new file with a class Name
 `Export`

 ## example


```py
# example_website_pareser.py
from scraper import Scraper


class Export(Scraper):
    def parse_html(self,html:str)->list[str]:
        return []
    def scrape(self,keyword:str)->str:
        html = self.session.get(API+keyword)
        self.parse_html(html)
        return ""

    def data(self)->dict[str,list[str]]:
        self.scraped :dict[str,list[str]] = {}
        for class_name in self.classes:
            self.scraped[class_name] = (self.scrape(class_name))
        return self.scraped

```