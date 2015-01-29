'''
@author: Glacier
'''
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.DataAccess as da

import datetime as dt
import matplotlib.pyplot as plt
import pandas

dataobj=da.DataAccess('ML4Trading')
ls_symbols=dataobj.get_all_symbols()
#print "All symbols: ",ls_symbols

symbols_toread=['ML4T-000', 'ML4T-001', 'ML4T-002', 'ML4T-003']

'''
ldt_timestamps=[]
ldt_timestamps.append(dt.datetime(2012,9,12,16))
'''

dtstart=dt.datetime(2012,8,01)
dtend=dt.datetime(2012,9,13)
ldttimestamps=du.getNYSEdays(dtstart,dtend,dt.timedelta(hours=16))

lsKeys = ['close']
# square bracket will be wrong
ldfdata=dataobj.get_data(ldttimestamps,symbols_toread,lsKeys)
#df_close = dataobj.get_data(ldttimestamps, symbols_toread, lsKeys)
print ldfdata
