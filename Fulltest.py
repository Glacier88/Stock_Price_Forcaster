'''
@author: Glacier
'''
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.DataAccess as da

import datetime as dt
import matplotlib.pyplot as plt
import pandas
import numpy as np

dataobj=da.DataAccess('ML4Trading')
ls_symbols=dataobj.get_all_symbols()
#print "All symbols: ",ls_symbols

symbols_toread=['ML4T-000']

'''
ldt_timestamps=[]
ldt_timestamps.append(dt.datetime(2012,9,12,16))
'''

dtstart=dt.datetime(2012,8,01)
dtend=dt.datetime(2012,9,13)
ldttimestamps=du.getNYSEdays(dtstart,dtend,dt.timedelta(hours=16))

lsKeys = ['open', 'high', 'low', 'close', 'volume']
# square bracket will be wrong
ldfdata=dataobj.get_data(ldttimestamps,symbols_toread,lsKeys)
#df_close = dataobj.get_data(ldttimestamps, symbols_toread, lsKeys)
ldfdata=np.array(ldfdata[0])
print ldfdata