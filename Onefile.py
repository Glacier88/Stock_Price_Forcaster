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

symbols_toread=['ML4T-000']



dtstart=dt.datetime(2000,2,01)
dtend=dt.datetime(2012,9,14)
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
    traindata[i-21,5]=rdata[i+5]  # real Y in the next fifth day

#print traindata[:,0:4]

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
    
testdata=traindata[:,0:5]

 
predictedprice=RandomForest(traindata,3,testdata)




plt.clf()
fig = plt.figure()
plt.plot(predictedprice,traindata[:,5])
                
plt.xlabel('predicted')
plt.ylabel('actual')
plt.xlim(0,200)        # set x scale
plt.ylim(0,200)        # set y scale
plt.title('Comparison of a single file',fontsize=12)

plt.savefig('single_file.pdf',format='pdf')
plt.close()
    
   