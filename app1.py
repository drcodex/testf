import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from PIL import Image, ImageFilter
from imageai.Detection import ObjectDetection
execution_path = os.getcwd()
detector = ObjectDetection()
detector.setModelTypeAsRetinaNet()
detector.setModelPath( os.path.join(execution_path , "resnet50_coco_best_v2.0.1.h5"))
detector.loadModel()
UPLOAD_FOLDER = "/home/dhanraj/testf/static"
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
imageRead=None

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/',methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print (filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action = "http://127.0.0.1:5000/result" method = "POST" enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/result',methods = ['POST', 'GET'])
def result():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    image = Image.open(file)
    print(UPLOAD_FOLDER)
    print ("-----------",file.filename)
    detections = detector.detectObjectsFromImage(UPLOAD_FOLDER+file.filename)
    return detections
if __name__ == '__main__':

    app.run(debug=True)
