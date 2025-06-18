from flask import Flask, request, render_template, send_from_directory,flash
# from pylab import *
import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model



app=Flask(__name__)
app.secret_key='random string'


pathlis=os.listdir(r'Data')
classess=[]
for i in pathlis:
    classess.append(i)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/upload/<filename>')
def send_image(filename):

    return send_from_directory('images',filename)

@app.route("/upload", methods=["POST","GET"])
def upload():
    print('a')
    if request.method=='POST':
        myfile = request.files['file']
        print("sdgfsdgfdf")
        fn = myfile.filename
        mypath = os.path.join('images/', fn)
        myfile.save(mypath)

        print("{} is the file name", fn)
        print("Accept incoming file:", fn)
        print("Save it to:", mypath)
        
        new_model = load_model(r'Mobilenet.h5')
        test_image = image.load_img(mypath, target_size=(128,128))
        test_image = image.img_to_array(test_image)
        test_image = test_image / 255
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis=0)
        result = new_model.predict(test_image)

        prediction = classess[np.argmax(result)]
        if prediction=='Bellyache bush (Green)':
            msg='Меdicinal use: The most frequent reports concern its antihypertensive, anti-inflammatory, antiophidian, analgesic, antipyretic, antimicrobial, healing, antianemic, antidiabetic, and antihemorrhagic activities'
        elif prediction=='Cape Gooseberry':
            msg='Medicinal Uses: It is high in protein (16%) and has antihistamine (allergies), anti-carcinogenic (cancer), antiviral, anti-inflammatory and antioxidant properties. In folk medicine it has been used for cancer, malaria, asthma, hepatitis, dermatitis and rheumatism.'
        elif prediction=='Crown flower':
            msg="Medicinal uses: The plant is reported as effective in treating skin, digestive, respiratory, circulatory and neurological disorders and was used to treat fevers, elephantiasis, nausea, vomiting, and diarrhea. The milky juice of Calotropis procera was used against arthritis, cancer, and as an antidote for snake bite."
        elif prediction=='Holy Basil':
            msg="Medicinal uses: medicinal herb used to combat stress and help address high blood sugar, inflammation, arthritis, and more. Medicinal preparations are made from holy basil's leaves, stems, and seeds of the plant."
        elif prediction=='Indian Stinging Nettle':
            msg='Medicinal uses: Stinging nettle has been used for hundreds of years to treat painful muscles and joints, eczema, arthritis, gout, and anemia. Today, many people use it to treat urinary problems during the early stages of an enlarged prostate (called benign prostatic hyperplasia or BPH).'
        elif prediction=='Indian wormwood':
            msg='Medicinal uses: Wormwood is an herb. The above-ground plant parts and oil are used for medicine. Wormwood is used for various digestion problems such as loss of appetite, upset stomach, gall bladder disease, and intestinal spasms'
        elif prediction=='Madagascar Periwinkle':
            msg='Medicinal uses: Madagascar periwinkle is a plant. The parts that grow above the ground and the root are used to make medicine. Madagascar periwinkle is used for diabetes, cancer, sore throat, cough, insect bite, and many other conditions,'
        elif prediction=='Mexican Mint':
            msg='Medicinal uses: improve the health of your skin, detoxify the body, defend against colds, ease the pain of arthritis, relieve stress and anxiety, treat certain kinds of cancer, and optimize digestion'
        elif prediction=='Nalta Jute':
            msg="Medicinal uses: Jute leaves are packed with vitamin K. This vitamin is useful in blood clotting. It also helps to reduce the chances of jaundice and poor absorption of nutrients. Chances of developing other common diseases, including colitis, Crohn's disease"
        elif prediction=='Night blooming Cereus':
            msg='Medicinal uses:  chest pain (angina), fluid retention associated with weak heart function (heart failure), and as a heart stimulant'

        return render_template("template.html", image_name=fn, text=prediction, message=msg)
    return render_template("index.html")



if __name__=='__main__':
    app.run(debug=True,host="0.0.0.0")