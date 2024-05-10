from bs4.element import Tag
from typing_extensions import override
from requests import Session
from scraper import Scraper
from bs4 import BeautifulSoup, NavigableString
from difflib import SequenceMatcher


class Export(Scraper):

    ROOT_API = "https://www.world.org/"
    BASE_API = f"{ROOT_API}weo/recycle"
    def __init__(self) -> None:
        self.session = Session()
        res = self.session.get(self.BASE_API)
        if not self.status_valid(res.status_code):
            raise Exception(f"Server did not respond with 2xx [{res.status_code}]")
        self.base_html = res.text
        self.base_soup = BeautifulSoup(self.base_html,"html.parser")
        self.table = self.find_table()
        self.endpoints:dict[str,str] = self.find_endpoints()
        super().__init__()


    def status_valid(self,code:int):
        return (200<=code<300)
    
    def resolve(self,url:str):
        if url.startswith("http"):
            return url
        elif url.startswith("/"):
            return f"{self.BASE_API}{url}"
        elif url.startswith(".."):
            return self.ROOT_API+url[2:]
        return f"{self.BASE_API}/{url}"


    def find_endpoints(self):
        links:dict[str,str] = {}
        atags:list[NavigableString] = self.table.findAll("a")
        if not atags:
            return links
        for atag in atags:
            if isinstance(atag,Tag):
                links[atag.text] = self.resolve(atag.get("href"))
        return links

    def find_table(self):
        # xpath
        # "/html/body/font/center/table[2]/tbody/tr/td[2]/div/table/tbody/tr/td/font/table"
        outer_tables = self.base_soup.findAll("table")
        if len(outer_tables)<3 and not isinstance(outer_tables[0],BeautifulSoup):
            return None
        first_inner_tbl = outer_tables[3].find("table") if outer_tables[3] else None # type:ignore[Any]
        if not isinstance(first_inner_tbl,Tag):
            return None
        return first_inner_tbl


    def findCloseMatch(self,class_name:str):
        for endpoint_name in self.endpoints:
            if SequenceMatcher(None,endpoint_name,class_name).ratio()>0.8:
                return endpoint_name
        return None

    @override
    def parser(self,html:str)->list[str]:
        howtos:list[str] = []
        fonts:list[Tag] = BeautifulSoup(html,"html.parser").findAll("font")
        if len(fonts)<6:
            return []
        data_font_tag = fonts[5]
        ul = data_font_tag.find("ul")
        if ul and isinstance(ul,Tag) :
            lis :list[Tag] = ul.findAll("li") 
            for li in lis:
                howtos.append(li.text)

        return howtos
        
    @override
    def scrape(self,keyword:str)->list[str]:
        if not self.endpoints:
            return []
        url =self.endpoints[keyword]
        res = self.session.get(url)
        if not self.status_valid(res.status_code):
            return []
        return self.parser(res.text)

    @override
    def data(self)->dict[str,list[str]]:
        self.scraped :dict[str,list[str]] = {}
        for class_name in self.classes:
            if cls_name:=self.findCloseMatch(class_name):
                self.scraped[class_name] = self.scrape(cls_name)
        return self.scraped