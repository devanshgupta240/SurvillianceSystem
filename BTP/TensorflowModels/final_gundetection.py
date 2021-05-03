#!/usr/bin/env python
# coding: utf-8

# In[1]:


from tensorflow import keras
import cv2
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


# In[18]:


#loading the model.
model = keras.models.load_model('pre-model.h5')


# In[11]:


#loading the model.
modelt = keras.models.load_model('guns.h5')


# In[32]:


#function to plot rectangle.
def plot_pred(img,z):
    fig, ax = plt.subplots(1)
    ax.imshow(img)
    rect =Rectangle((z[0][0],z[0][1]),width = z[0][3],height = z[0][2], linewidth=1,edgecolor='g',facecolor='none')
    ax.add_patch(rect)
    plt.show()


# In[44]:


#loading and preprocessing an image for testing.
img1 = cv2.imread('8.jpg')
img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
img1 = cv2.resize(img1, (416,416))


# In[46]:


y_hat = model.predict(img1.reshape(-1,416,416,3))
print(y_hat)
if y_hat[0][1]>0.35:
    img1 = cv2.cvtColor(img1, cv2.COLOR_RGB2BGR)
    z = modelt.predict(img1.reshape(-1,416,416,3))
    plot_pred(img1,z)


# In[ ]:




