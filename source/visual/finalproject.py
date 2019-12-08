#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import matplotlib.pyplot as plt

class findpidigit:
    def __init__(self,digit):
        self.digit=digit
        self.m1=1
        self.m2=100**(digit-1)
        self.v1=0
        self.v2=-5
        self.x1=5
        self.x2=10
        self.l1=2
        self.l2=2
        self.count=0
        self.record1=[self.v1*np.sqrt(self.m1)]
        self.record2=[self.v2*np.sqrt(self.m2)]
        self.recordx1=[self.x1]
        self.recordx2=[self.x2]
        self.timeset=[0]
        #self.times=np.array([0])
        self.time=0
        self.findpi()
        self.times=np.array(self.timeset)


    #find pi with eventdriven collision events


    def findpi(self):
        while True:
            if self.v1 >=0 and self.v2>=0 and self.v2-self.v1>=0:
                break
            if self.v1<0:
                dt=-(self.x1-self.l1/2)/(self.v1)
                self.time+=dt
                #self.times=np.append(self.times,self.time)
                self.timeset.append(self.time)
                self.x1+=dt*self.v1
                self.x2+=dt*self.v2
                self.recordx1.append(self.x1)
                self.recordx2.append(self.x2)

                self.count+=1
                self.v1 *=-1
                self.record1.append(self.v1*np.sqrt(self.m1))
                self.record2.append(self.v2*np.sqrt(self.m2))
            if self.v2-self.v1 <0 and self.v1>=0:
                dt=(np.abs(self.x1-self.x2)-(self.l1+self.l2)/2)/np.abs(self.v1-self.v2)
                self.time+=dt
                #self.times=np.append(self.times,self.time)
                self.timeset.append(self.time)
                self.x1+=self.v1*dt
                self.x2+=self.v2*dt
                self.recordx1.append(self.x1)
                self.recordx2.append(self.x2)
                u1=self.v1
                u2=self.v2
                self.count+=1
                self.v1=(u1*(self.m1-self.m2)+2*self.m2*u2)/(self.m1+self.m2)
                self.v2=(u2*(self.m2-self.m1)+2*self.m1*u1)/(self.m1+self.m2)
                self.record1.append(self.v1*np.sqrt(self.m1))
                self.record2.append(self.v2*np.sqrt(self.m2))


    #plot the phasespce graph with v1/sqrt(m1) and v2/sqrt(m2)
    def plotphase(self,sizex=4,sizey=4):
        plt.figure(figsize=(sizex,sizey))
        plt.plot(self.record2,self.record1)


    #plot the position by time graph
    def plotpos(self,sizex=6,sizey=3,stick=False):
        if not stick:
            plt.figure(figsize=(sizex,sizey))
            plt.plot(self.times,self.recordx1)
            plt.plot(self.times,self.recordx2)
        else:
            newrecordx2=self.recordx2.copy()
            for i in range(len(self.recordx2)):
                newrecordx2[i]-=(self.l1+self.l2)/2
            plt.figure(figsize=(sizex,sizey))
            plt.plot(self.times,self.recordx1)
            plt.plot(self.times,newrecordx2)


# In[2]:


from vpython import *
import numpy as np
a=findpidigit(2)
graphicon=False
dt=0.001
rateval=1/dt
wall=box(pos=vec(-0.1,0,0),size=vec(-0.1,10,10))
sbox=box(pos=vec(5,0,0),size=vec(2,2,2))
bbox=box(pos=vec(10,0,0),size=vec(2,2,2),color=color.green)
def R(r):
    global a
    global g
    global graphicon
    global phase
    if r.checked:
        g=graph(width=600,height=600
        ,xmin=1.2*a.record2[0],xmax=-1.2*a.record2[0],ymin=1.2*a.record2[0],ymax=-1.2*a.record2[0])
        phase=gcurve(color=color.blue)
        graphicon=True
    else:
        g.delete()
        graphicon=False
radio(bind=R, text='Phase space') # text to right of button

scene.append_to_caption('\n\n')

def T(s):
    global a

    a=findpidigit(s.number)

    return a


def setspeed(s):
    global rateval
    global dt
    rateval=int((1/dt)*s.value)

    wt.text='{:1.4f}'.format(s.value)
s1 = slider(min=0.05, max=1, value=0.05, length=220, bind=setspeed, right=15)
wt = wtext(text='{:1.4f}'.format(s1.value))
scene.append_to_caption(' rate\n')

scene.append_to_caption('\n\n')
scene.append_to_caption(' number of digit\n')
winput( bind=T )
numcoltext=label( height=25,pos=vec(-7,0,0), text='Number of collisions:\n{:1.0f}'.format(0))


# In[25]:


time=0
for i in range(int(a.times[-1]/dt+1)):
    rate(rateval)

    n2=len(a.times[a.times<time])
    time+=dt
    n1=len(a.times[a.times<time])
    numcoltext.text='Number of collisions:\n{:1.0f}'.format(n1-1)
    if graphicon:
        for j in range(n2,n1):
            phase.plot((a.record2[j],a.record1[j]))
    if n1!=len(a.times):
        t1=a.times[n1-1]
        t2=a.times[n1]
        x11=a.recordx1[n1-1]
        x12=a.recordx1[n1]
        x21=a.recordx2[n1-1]
        x22=a.recordx2[n1]
        sbox.pos.x=(x12-x11)/(t2-t1)*(time-t1)+x11
        bbox.pos.x=(x22-x21)/(t2-t1)*(time-t1)+x21

for k in range(1000):
    rate(rateval)
    sbox.pos.x+=a.record1[-1]*0.001
    bbox.pos.x+=a.record2[-1]*0.001/np.sqrt(a.m2)


# In[ ]:
