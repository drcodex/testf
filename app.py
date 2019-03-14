from flask import Flask, render_template, request
from werkzeug import secure_filename
from PIL import Image, ImageFilter
from imageai.Detection import ObjectDetection
import os 
from keras import backend as K
execution_path = 'static'
detector = ObjectDetection()
detector.setModelTypeAsRetinaNet()
detector.setModelPath( os.path.join(execution_path , "resnet50_coco_best_v2.0.1.h5"))
detector.loadModel()
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
imageRead=None
app = Flask(__name__)

UPLOAD_FOLDER = os.path.basename('static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def upload():
   return render_template('upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        path=os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
        f.save(path)
        f.save(secure_filename(f.filename))
        print(os.path.join(app.config['UPLOAD_FOLDER'],"out.jpg"))
        execution_path = 'static'
        detector = ObjectDetection()
        detector.setModelTypeAsRetinaNet()
        detector.setModelPath( os.path.join(execution_path , "resnet50_coco_best_v2.0.1.h5"))
        K.clear_session()
        detector.loadModel()
        detections = detector.detectObjectsFromImage(input_image=path, output_image_path=os.path.join(app.config['UPLOAD_FOLDER'],"out.jpg"))
        return render_template("showimage.html", user_image = 'static/out.jpg')	
if __name__ == '__main__':
   app.run(debug = True)
