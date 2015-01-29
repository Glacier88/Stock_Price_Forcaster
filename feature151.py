'''
@author: Glacier
'''
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.DataAccess as da
import random

import datetime as dt
import matplotlib.pyplot as plt
import pandas
import numpy as np

dataobj=da.DataAccess('ML4Trading')
ls_symbols=dataobj.get_all_symbols()
#print "All symbols: ",ls_symbols

symbols_toread=['ML4T-151']



dtstart=dt.datetime(2000,2,01)
dtend=dt.datetime(2000,6,24)
ldttimestamps=du.getNYSEdays(dtstart,dtend,dt.timedelta(hours=16))

lsKeys = ['actual_close']


ldfdata=dataobj.get_data(ldttimestamps,symbols_toread,lsKeys)
ldfdata=np.array(ldfdata[0])

'''
Compute indicators and generate train dataset
'''
#print a[:,1]
rdata=ldfdata[:,0]
#print np.amax(rdata,axis=0)
#print np.amin(rdata,axis=0)
#print np.std(rdata)
#print np.mean(rdata)

traindata=np.zeros((len(ldfdata)-21-5,6))

for i in range(21,len(ldfdata)-5):
    m=rdata[i-21:i]
    traindata[i-21,0]=np.std(m) #Standard Deviation
    traindata[i-21,1]=(np.amax(m)-np.amin(m)) #Amplitude
    traindata[i-21,2]=np.array(m[20]-m[19])   #Change of today and yesterday
    traindata[i-21,3]=np.array((m[20]-m[19])-(m[19]-m[18])) #change of the change in three days
    '''Compute Frequency'''
    f=0
    mean=np.mean(m)
    for l in range(0,20):
        if (m[l]-mean)*(m[l+1]-mean)<0:
            f=f+1
    traindata[i-21,4]=np.array(f)
    traindata[i-21,5]=rdata[i+5]  

stardard_diviation=traindata[0:len(ldfdata)-26,0]
amplitute=traindata[0:len(ldfdata)-26,1]
change=traindata[0:len(ldfdata)-26,2]
changes=traindata[0:len(ldfdata)-26,3]
frequency=traindata[0:len(ldfdata)-21-5,4]

'''PLOT Function'''
    
D=np.arange(1,76,1)
plt.clf()
fig = plt.figure()
plt.plot(D+25,stardard_diviation,label='Standard deviation',color='red')
plt.plot(D+25,change,label='Price change of today and yesterday')
plt.plot(D+25,amplitute,label='Amplitude',color='cyan')
plt.plot(D+25,changes,label='Change of price changes in the last two days',color='black')
plt.plot(D+25,frequency,label='Frequency',color='magenta')
plt.legend()                 
plt.xlabel('Days')
plt.ylabel('features')
plt.xlim(1,100)        # set x scale
plt.ylim(-2,35)        # set y scale
plt.title('Features in first 100 days for File 151 ',fontsize=12)

plt.savefig('feature 151.pdf',format='pdf')
plt.close()
    