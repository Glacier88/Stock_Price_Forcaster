'''
@author: Glacier
'''
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
import math
dataobj=da.DataAccess('ML4Trading')


symbols_toread=['ML4T-000', 'ML4T-001', 'ML4T-002', 'ML4T-003', 'ML4T-004', 'ML4T-005', 'ML4T-006', 'ML4T-007', 'ML4T-008',
 'ML4T-009', 'ML4T-010', 'ML4T-011', 'ML4T-012', 'ML4T-013', 'ML4T-014', 'ML4T-015', 'ML4T-016', 'ML4T-017',
 'ML4T-018', 'ML4T-019', 'ML4T-020', 'ML4T-021', 'ML4T-022', 'ML4T-023', 'ML4T-024', 'ML4T-025', 'ML4T-026',
 'ML4T-027', 'ML4T-028', 'ML4T-029', 'ML4T-030', 'ML4T-031', 'ML4T-032', 'ML4T-033', 'ML4T-034', 'ML4T-035',
 'ML4T-036', 'ML4T-037', 'ML4T-038', 'ML4T-039', 'ML4T-040', 'ML4T-041', 'ML4T-042', 'ML4T-043', 'ML4T-044',
 'ML4T-045', 'ML4T-046', 'ML4T-047', 'ML4T-048', 'ML4T-049', 'ML4T-050', 'ML4T-051', 'ML4T-052', 'ML4T-053',
 'ML4T-054', 'ML4T-055', 'ML4T-056', 'ML4T-057', 'ML4T-058', 'ML4T-059', 'ML4T-060', 'ML4T-061', 'ML4T-062',
 'ML4T-063', 'ML4T-064', 'ML4T-065', 'ML4T-066', 'ML4T-067', 'ML4T-068', 'ML4T-069', 'ML4T-070', 'ML4T-071',
 'ML4T-072', 'ML4T-073', 'ML4T-074', 'ML4T-075', 'ML4T-076', 'ML4T-077', 'ML4T-078', 'ML4T-079', 'ML4T-080',
 'ML4T-081', 'ML4T-082', 'ML4T-083', 'ML4T-084', 'ML4T-085', 'ML4T-086', 'ML4T-087', 'ML4T-088', 'ML4T-089',
 'ML4T-090', 'ML4T-091', 'ML4T-092', 'ML4T-093', 'ML4T-094', 'ML4T-095', 'ML4T-096', 'ML4T-097', 'ML4T-098',
 'ML4T-099','ML4T-151','ML4T-292']



dtstart=dt.datetime(2000,2,01)
dtend=dt.datetime(2012,9,14)
ldttimestamps=du.getNYSEdays(dtstart,dtend,dt.timedelta(hours=16))

lsKeys = ['actual_close']


ldfdata=dataobj.get_data(ldttimestamps,symbols_toread,lsKeys)
ldfdata=np.array(ldfdata[0])

'''
Compute indicators and generate train dataset
'''
alltraindata=np.array([0,0,0,0,0,0])

for i in range(0,100):
    rdata=ldfdata[:,i]
    traindata=np.zeros((len(rdata)-21-5,6))
    
    for j in range(21,len(rdata)-5):
        m=rdata[j-21:j]
        traindata[j-21,0]=np.std(m) #Standard Deviation
        traindata[j-21,1]=(np.amax(m)-np.amin(m)) #Amplitude
        traindata[j-21,2]=np.array(m[20]-m[19])   #Change of today and yesterday
        traindata[j-21,3]=np.array((m[20]-m[19])-(m[19]-m[18])) #change of the change in three days

        fr=0
        mean=np.mean(m)
        for l in range(0,20):
            if (m[l]-mean)*(m[l+1]-mean)>0:
                fr=fr+1
        traindata[j-21,4]=fr
        traindata[j-21,5]=rdata[j+5]
    #alltraindata=alltraindata.append(traindata)
    alltraindata=np.vstack((alltraindata,traindata))
alltraindata=alltraindata[1:len(alltraindata)]
#print len(alltraindata)
            


def buildTree(data,index=1):
    
   
    # If it is a leaf node
    if len(data)==1:
        
        # MUST add[[ ]],otherwise len(leaf) will be 5!!!!!!
        leaf=[[index,-1,data[0][5],-1,-1]]
        index=index+1
           
        return leaf
    
    
    #if not leave
    else:
        
        
        #Select Feature
        feature=random.randint(0,4)
        
        redundant=True
        for i in range(0,len(data)-1):
            if (data[i][feature]!=data[i+1][feature]):
                redundant=False
        if(redundant==True):
            avg=np.mean(data[:,5])
            leafr=[[index,-1,avg,-1,-1]]
            index=index+1
            return leafr
                
     
        else:      
            #Compute split value
             randomgroup=np.random.randint(len(data),size=2)

        
             Xrandom1=randomgroup[0]
             Xrandom2=randomgroup[1]
#Very important!!! if 1,2,2,2,2 is the input data, there will still be nothing in the right dataset, here we must guarantee that this never happen!!!
             while(data[Xrandom1][feature]==data[Xrandom2][feature]):
                   randomgroup=np.random.randint(len(data),size=2)
                   Xrandom1=randomgroup[0]
                   Xrandom2=randomgroup[1]
            
            
             SplitVal=(data[Xrandom1][feature]+data[Xrandom2][feature])/2.0
        
        
        #THEN DIVIDE GROUPS
        
        #Set an initial value of leftdata and rightdata
             leftdata=[0,0,0,0,0,0]
             rightdata=[0,0,0,0,0,0]
        
             for i in range (0,len(data)):
            
            #Compute left group
                   if data[i][feature]<=SplitVal:
                            leftdata=np.vstack((leftdata,data[i]))
                #leftdata=np.append([leftdata],[data[i]],axis=0)
            #Delete the added first row and return the data array
            
            #Compute right group
                   if data[i][feature]>SplitVal:
                           rightdata=np.vstack((rightdata,data[i]))  # @IndentOk
                #rightdata=np.append([rightdata],[data[i]],axis=0)
                
             leftdata=leftdata[1:len(leftdata)]
             rightdata=rightdata[1:len(rightdata)]
        #rightdata=rightdata[1:rightdata.shape[0]]
        
        

             lefttree=buildTree(leftdata,index+1)
             righttree=buildTree(rightdata,index+len(lefttree)+1)
        
        
        #Compute Current node
        
             Cnode=[index,feature,SplitVal,index+1,index+len(lefttree)+1]
        
             index=index+1
        #Combine the left tree and the right tree
        
             tree=np.vstack((Cnode,lefttree,righttree))
             
    
             return tree
            
        
def QueryTree(Tree,Xtest):
    
    #initial i, which is the (index-1) of Tree
    i=0
    
    while(Tree[i][1]!=-1):
    
        feature=Tree[i][1]
        
        #Go left tree
        if Xtest[feature]<=Tree[i][2]:
            i=Tree[i][3]-1
        #Go right tree
        else:
            i=Tree[i][4]-1
    
    Ytest=Tree[i][2]
    
    return Ytest
    
    
def RandomForest(data,k,testdata):
    
    ka=k
    Ytest=np.zeros((len(testdata),k))
    
    while (k!=0):
        Tree=buildTree(data)
        for i in range(0,len(testdata)):
            Ytest[i,k-1]=QueryTree(Tree,testdata[i])
        k=k-1
    
    Y_randomforest=np.zeros((len(testdata)))
    
    for i in range(0,len(testdata)):
        Y_randomforest[i]=(np.sum(Ytest[i,:]))/ka
    
    return Y_randomforest  
 
 
'''Query data'''
    
'''Query data'''
    
symbols_toread=['ML4T-292']
dtstart=dt.datetime(2012,3,16)
dtend=dt.datetime(2012,9,14)
ldttimestamps=du.getNYSEdays(dtstart,dtend,dt.timedelta(hours=16))
lsKeys = ['actual_close']
ldfdata=dataobj.get_data(ldttimestamps,symbols_toread,lsKeys)
ldfdata=np.array(ldfdata[0])
rdata=ldfdata[:,0]
querydata=np.zeros((len(rdata)-21-5,6))
for i in range(21,len(rdata)-5):
    m=rdata[i-21:i]
    querydata[i-21,0]=np.std(m) #Standard Deviation
    querydata[i-21,1]=(np.amax(m)-np.amin(m)) #Amplitude
    querydata[i-21,2]=np.array(m[20]-m[19])   #Change of today and yesterday
    querydata[i-21,3]=np.array((m[20]-m[19])-(m[19]-m[18])) #change of the change in three days
    '''Compute Frequency'''
    f=0
    mean=np.mean(m)
    for l in range(0,20):
        if (m[l]-mean)*(m[l+1]-mean)<0:
            f=f+1
    querydata[i-21,4]=np.array(f)
    querydata[i-21,5]=rdata[i+5]  # real Y in the next fifth day

querydata=querydata[:,0:5]
predictedprice=RandomForest(alltraindata,20,querydata)
print predictedprice


d=np.arange(1,101,1)
plt.clf()
fig = plt.figure()
plt.plot(d,predictedprice,label='Ypredict',color='red')
plt.plot(d,ldfdata[:,0][26:126],label='Yactual')
plt.legend()                 
plt.xlabel('Days')
plt.ylabel('Prices')
plt.xlim(1,100)        # set x scale
plt.ylim(0,500)        # set y scale
plt.title('Ypredict vs Yatual for File 292-last100days',fontsize=12)

plt.savefig('Predicted vs actual 292_last100.pdf',format='pdf')
plt.close()
print "The RMS of 292 last 100 days is:",math.sqrt(((predictedprice-ldfdata[:,0][21:121])**2).mean(axis=0))
print "The correlation of 292 last 100 days is:",np.corrcoef(predictedprice,ldfdata[:,0][21:121])[1,0]





