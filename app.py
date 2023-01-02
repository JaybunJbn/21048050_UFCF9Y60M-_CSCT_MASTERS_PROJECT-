#!/usr/bin/env python
# coding: utf-8

# <div style='font-size:120%;'>
#     <a id='nan'></a>
#     <h1 style='font-weight: bold;'>
#         <center> ScaLe Web Application </center>
#     </h1>
# </div>

# In[1]:


from flask import Flask, render_template, request
from keras.models import load_model
from keras.preprocessing import image


# In[2]:


app = Flask(__name__)


# In[3]:


dic = {0: 'GuayTiewRuea',
       1: 'MassamanCurry',
       2: 'PadKraPao',
       3: 'PadTaiNoodle',
       4: 'PanangCurry',
       5: 'PapayaSalad',
       6: 'ThaiGreenCurry',
       7: 'TomKhaGai',
       8: 'TomYumKung',
       9: 'YellowCurry'}


# In[4]:


model = load_model('scale-project.h5')


# In[5]:


model.make_predict_function()


# In[6]:


def predict_label(img_path):
    i = image.load_img(img_path, target_size = (224, 224))
    i = image.img_to_array(i)/255.0
    i = i.reshape(1, 224, 224, 3)
    p = model.predict_classes(i)
    return dic[p[0]]


# In[7]:


def exception_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_code = getattr(e, "code", 500)
            logger.exception("Service exception: %s", e)
            r = dict_to_json({"message": e.message, "matches": e.message, "error_code": error_code})
            return Response(r, status=error_code, mimetype='application/json')
    return wrapper


# In[8]:


@app.route('/', methods = ['GET', 'POST'])
def home_page():
    return render_template('index.html') # Add HTML: Home


# In[9]:


@app.route('/about', methods = ['GET', 'POST'])
def about_page():
    return render_template('about.html') # Add HTML: About


# In[10]:


@app.route('/contact', methods = ['GET', 'POST'])
def contact_page():
    return render_template('contact.html') # Add HTML: Contact


# In[12]:


@app.route('/home', methods = ['GET', 'POST'])
def home_page():
    if request.method == 'POST':
        img = request.files['my_image']
        
        img_path = 'static/' + img.filename
        img.save(img_path)
        
        p = predict_label(img_path)
    return render_template('home.html', prediction = p, img_path = img_path)


# In[13]:


if __name__ == '__main__':
    app.run(debug = True)


# In[ ]:




