from types import ModuleType
import json
from pathlib import Path
from typing import Any # type:ignore[Any]

from scraper import Scraper
from datetime import datetime

avilable_scrapers:list[str] = ["wo","wikihow"]

ROOT_DIR = Path(__file__).parent
DATE  = datetime.today()

data:dict[str,list[str]] = {}

for _class in avilable_scrapers:
    exporter:ModuleType = __import__(f"{_class}")
    export_inst:Scraper|Any = exporter.Export() # type:ignore[Any]
    if not isinstance(export_inst,Scraper):
        continue
    data.update(export_inst.data())

with open(f"data_{DATE.strftime('%Y_%m_%d')}.json","w") as fp:
    json.dump(data,fp)