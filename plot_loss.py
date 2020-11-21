#!/usr/bin/env python
# coding: utf-8

# In[24]:


import matplotlib.pyplot as plt
import numpy as np


# In[2]:


f = open('./loss_log.txt')


# In[3]:


f.readline()


# In[4]:


D_A = []
G_A = []
cycle_A = []
idt_A = []

D_B = []
G_B = []
cycle_B = []
idt_B = []


# In[5]:


while True:
    line = f.readline()
    if not line: break
    
    values = line.split(' ')
    D_A.append(float(values[9]))
    G_A.append(float(values[11]))
    cycle_A.append(float(values[13]))
    idt_A.append(float(values[15]))
    D_B.append(float(values[17]))
    G_B.append(float(values[19]))
    cycle_B.append(float(values[21]))
    idt_B.append(float(values[23]))


# In[28]:


D_A = np.array(D_A)
G_A = np.array(G_A)
cycle_A = np.array(cycle_A)
idt_A = np.array(idt_A)

D_B = np.array(D_B)
G_B = np.array(G_B)
cycle_B = np.array(cycle_B)
idt_B = np.array(idt_B)


# In[17]:


plt.rcParams['figure.figsize'] = [12, 8]
plt.rcParams['figure.dpi'] = 100 # 200 e.g. is really fine, but slower


# In[37]:


plt.plot(D_A, label='D_A')
plt.plot(G_A, label='G_A')
plt.plot(cycle_A, label='cycle_A')
plt.plot(idt_A, label='idt_A')
plt.plot(D_B, label='D_B')
plt.plot(G_B, label='G_B')
plt.plot(cycle_B, label='cycle_B')
plt.plot(idt_B, label='idt_B')
plt.xlabel('steps')
plt.ylabel('loss')
plt.legend()
plt.savefig('losses.png')


# In[38]:
plt.cla()


plt.plot(D_A+G_A+cycle_A+idt_A, label='A')
plt.plot(D_B+G_B+cycle_B+idt_B, label='B')
plt.xlabel('steps')
plt.ylabel('loss')
plt.legend()
plt.savefig('sum_loss.png')


# In[ ]:




