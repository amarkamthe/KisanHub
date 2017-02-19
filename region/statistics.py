import pandas as pd
import requests
from numpy import random
from io import StringIO
import json
import itertools
from .models import *

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
        def float_cust(val):
            v=''
            if val:
                try:
                    v= float(val)
                except:
                    v=""
            return v
        convert = {'Year':int,'JAN':float_cust, 'FEB':float_cust, 'MAR':float_cust, 'APR':float_cust, 'MAY':float_cust,
                    'JUN':float_cust, 'JUL':float_cust, 'AUG':float_cust, 'SEP':float_cust, 'OCT':float_cust,
                    'NOV':float_cust, 'DEC':float_cust, 'WIN':float_cust, 'SPR':float_cust, 'SUM':float_cust,
                    'AUT':float_cust, 'ANN':float_cust}
        rows = pd.read_table(StringIO(data),header=0, index_col=0 , skiprows=6, delim_whitespace=True, na_values="-1", keep_default_na=False, converters=convert)
        for row in rows.iterrows():
            self.database_save(int(row[0]), list(row[1]))

    def fetch(self):
        for component in COMPONENT_TYPE_CHOICES:
            self.component = component[0]
            self.url = settings.STATISTICAL_DATA_URL.format(component[1], self.region.file_name)
            self.parse()

def region_statistical_data(region_id, component):
    region = Region.objects.get(id=region_id)
    rainfall = StatisticalData.objects.filter(region=region,component=component).select_related('region').order_by('year')
    rainfall_year = itertools.groupby(rainfall, key=lambda x:x.region.name)
    region_data = {}
    for key, regions in rainfall_year:
        rainfall_data = {}
        for rain in regions:
            data = json.loads(rain.blob)
            rainfall_data[rain.year]=data
        region_data[key]=rainfall_data
    return region_data
