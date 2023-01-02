#!/usr/bin/env python
# coding: utf-8

# <div style='font-size:120%;'>
#     <a id='nan'></a>
#     <h1 style='font-weight: bold;'>
#         <center> ScaLe Flask </center>
#     </h1>
# </div>

# In[5]:


import sys
import os
import glob
import re
import numpy as np

from __future__ import division, print_function

# Keras

from keras.applications.imagenet_utils import preprocess_input, decode_predictions
from keras.models import load_model
from keras.preprocessing import image

# Flask Utils

from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer


# In[6]:


# Define a Flask App

app = Flask(__name__)


# In[9]:


# Model saved with Keras model.save()

MODEL_PATH = 'scale-project.h5'


# In[11]:


# Load your trained model
model = load_model(MODEL_PATH)
model._make_predict_function()


# In[12]:


print('Model loaded. Check http://127.0.0.1:5000/')


# In[13]:


def model_predict(img_path, model):
    img = image.load_img(img_path, target_size=(224, 224))

    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x, mode='caffe')

    preds = model.predict(x)
    return preds


# In[14]:


@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')


# In[16]:


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


# In[17]:


@app.route('/contact', methods=['GET'])
def contact():
    return render_template('contact.html')


# In[18]:


@app.route('/home', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':

        f = request.files['file']

        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        preds = model_predict(file_path, model)

        pred_class = decode_predictions(preds, top=1)
        result = str(pred_class[0][0][1])
        return result
    return None


# In[19]:


if __name__ == '__main__':
    app.run(debug=True)


# In[ ]:




