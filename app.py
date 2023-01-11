import os
import uuid
import flask
import urllib
from PIL import Image
from flask import Flask , render_template  , request , send_file
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img , img_to_array

app = Flask(__name__)

data_dir = os.path.dirname(os.path.abspath(__file__))
model = load_model(os.path.join(data_dir , 'scale-project.h5'))

# model.make_predict_function()

ext = set(['jpg' , 'jpeg' , 'png' , 'jfif'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ext

classes = ['Thai Boat Noodles (Guay Teow Rhua)',
'Thai Massaman Chicken Curry (Gaeng Massaman)',
'Spicy Thai Basil Chicken Stir-Fly (Pad Krapao)',
'Thai-Style Fried Noodles (Pad Thai)',
'Thai Panang Chicken Curry',
'Spicy Thai Green Papaya Salad (Som Tum)',
'Thai Green Chicken Curry (Gaeng Keow Wan)',
'Chicken Thai Coconut Soup (Tom Kha)',
'Spicy Thai Shrimp Soup (Tom Yum Goong)',
'Southern Thai Sour Curry (Kaeng Lueang)']

def predict(filename, model):
    img = load_img(filename, target_size = (224, 224))
    img = img_to_array(img)
    img = img.reshape(1, 224, 224, 3)

    img = img.astype('float32')
    img = img/255.0
    result = model.predict(img)

    dict_result = {}
    for i in range(10):
        dict_result[result[0][i]] = classes[i]

    res = result[0]
    res.sort()
    res = res[::-1]
    prob = res[:3]
    
    prob_result = []
    class_result = []
    for i in range(3):
        prob_result.append((prob[i]*100).round(2))
        class_result.append(dict_result[prob[i]])

    return class_result, prob_result

def cal(class_result):
                
    if class_result == classes[0]:
        return '360 KCal'
    elif class_result == classes[1]:
        return '317 KCal'
    elif class_result == classes[2]:
        return '271 KCal'
    elif class_result == classes[3]:
        return '343 KCal'
    elif class_result == classes[4]:
        return '259 KCal'
    elif class_result == classes[5]:
        return '246 KCal'
    elif class_result == classes[6]:
        return '215 KCal'
    elif class_result == classes[7]:
        return '260 KCal'
    elif class_result == classes[8]:
        return '230 KCal'
    else:
        return '362 KCal'

@app.route('/')
def first():
    return render_template('index.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/predict', methods = ['GET' , 'POST'])

def result():
    error = ''
    target_img = os.path.join(os.getcwd() , 'static/images')
    if request.method == 'POST':
        if(request.form):
            link = request.form.get('link')
            try :
                resource = urllib.request.urlopen(link)
                unique_filename = str(uuid.uuid4())
                filename = unique_filename+".jpg"
                img_path = os.path.join(target_img, filename)
                output = open(img_path, "wb")
                output.write(resource.read())
                output.close()
                img = filename

                class_result, prob_result = predict(img_path, model)

                predictions = {
                    "class1":class_result[0],
                    "prob1": prob_result[0],
                    "cal1": cal(class_result[0])
                }

            except Exception as e : 
                print(str(e))
                error = 'This image from this site is not accesible or inappropriate input'

            if(len(error) == 0):
                return  render_template('predict.html',img  = img ,predictions = predictions)
            else:
                return render_template('home.html', error = error) 
            
        elif (request.files):
            file = request.files['file']
            if file and allowed_file(file.filename):
                file.save(os.path.join(target_img, file.filename))
                img_path = os.path.join(target_img, file.filename)
                img = file.filename

                class_result, prob_result = predict(img_path, model)

                predictions = {
                    "class1":class_result[0],
                    "prob1": prob_result[0],
                    "cal1": cal(class_result[0])
                }

            else:
                error = "Please upload images of jpg, jpeg and png extension only"

            if(len(error) == 0):
                return  render_template('predict.html', img  = img, predictions = predictions)
            else:
                return render_template('home.html', error = error)

    else:
        return render_template('home.html')

if __name__ == '__main__':
    app.run(port = 3000, debug = True)