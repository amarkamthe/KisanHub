import pandas as pd
import requests
from numpy import random
from io import StringIO
import json

from django.conf import settings
from .models import *

class statistics(object):
    def __init__(self, region):
        self.region = region

    def database_save(self, year, blob):
        chk_data = {'year':year,
                    'region':self.region,
                    'component':self.component}
        statistical, created = StatisticalData.objects.update_or_create(blob=json.dumps(blob), defaults=chk_data)

    def parse(self):
        data = requests.get(self.url, headers={'User-agent':'Mozilla/5.0'}).text
        # date = pd.read_table(StringIO(data), skiprows=5, nrows=0, delim_whitespace=True)
        # date = list(date)
        # date = date[len(date)-1][:-1]
        rows = pd.read_table(StringIO(data),header=0, index_col=0 , skiprows=6, delim_whitespace=True)
        for row in rows.iterrows():
            self.database_save(int(row[0]), dict(row[1]))

    def fetch(self):
        for component in COMPONENT_TYPE_CHOICES:
            self.component = component[0]
            self.url = settings.STATISTICAL_DATA_URL.format(component[1], self.region.file_name)
            self.parse()
