from celery import task, shared_task,current_task
from numpy import random
from scipy.fftpack import fft
import requests
from io import StringIO
from KisanHub import celery_app
from time import sleep
import pandas as pd
lst  =['http://www.metoffice.gov.uk/pub/data/weather/uk/climate/datasets/Tmax/date/UK.txt',
       'http://www.metoffice.gov.uk/pub/data/weather/uk/climate/datasets/Tmax/date/UK.txt',
       'http://www.metoffice.gov.uk/pub/data/weather/uk/climate/datasets/Tmax/date/UK.txt',
       'http://www.metoffice.gov.uk/pub/data/weather/uk/climate/datasets/Tmax/date/UK.txt']


#@shared_task
@celery_app.task()
def fft_random():
    """
    Brainless number crunching just to have a substantial task:
    """
    fp = open('test.txt','w')
    process_percent = 0
    for link in lst:
        data = requests.get(link, headers={'User-agent':'Mozilla/5.0'}).text
        rows=pd.read_table(StringIO(data),header=0,index_col=0 , skiprows=6, delim_whitespace=True)
        for row in rows.iterrows():
            fp.write(str(row[0])+ '--'+ str(row[1]))
        process_percent += (100/len(lst))
        fft_random.update_state(state='PROGRESS',
                                    meta={'process_percent':process_percent})
    # for i in range(n):
    #     x = random.normal(0, 0.1, 2000)
    #     y = fft(x)
    #     if(i%30 == 0):
    #         process_percent = int(100 * float(i) / float(n))
    #         current_task.update_state(state='PROGRESS',
    #                                   meta={'process_percent': process_percent})
    return random.random()
