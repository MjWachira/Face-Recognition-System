from flask import Flask, session, redirect, url_for, render_template, Response, flash
from flask import Flask, jsonify, request
from wtforms.validators import InputRequired
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
from flask_mysqldb import MySQL,MySQLdb 
from flask_wtf import FlaskForm
from datetime import datetime
import face_recognition
import urllib.request
import numpy as np
import bcrypt
import cv2
import os
import csv

app = Flask(__name__)

app.secret_key = "john-wachira"
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'facedb'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)
 
@app.route('/')
def home():
    return render_template("home.html")
 
@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (name, email, password) VALUES (%s,%s,%s)",(name,email,hash_password,))
        mysql.connection.commit()
        session['name'] = request.form['name']
        session['email'] = request.form['email']
        return redirect(url_for('home'))
 

@app.route('/login',methods=["GET","POST"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM users WHERE email=%s",(email,))
        user = curl.fetchone()
        curl.close()
        
 
        if len(user) > 1:
        #if bcrypt.hashpw(password, user["password"].encode('utf-8')) == user["password"].encode('utf-8'):
            if bcrypt.hashpw(password, user["password"].encode('utf-8')) == user["password"].encode('utf-8'):
                session['name'] = user['name']
                session['email'] = user['email']
                return render_template("home.html")
            else:
                return "Error password and email not match"
        else:
            return "Error user not found"
    else:
        return render_template("login.html")

 
@app.route('/logout')
def logout():
    session.clear()
    return render_template("home.html")



path = 'static/uploads'
images = []
Names = []
myList = os.listdir(path)
print(myList)

for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    Names.append(os.path.splitext(cl)[0])
    print(Names)

 #generating their encodings
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

encodeListKnown = findEncodings(images)
print('Encoding Complete')

 #saving names of the identified faces on a csv file
def Records(name):
    with open('Records.csv','r+') as f:
        myDataList = f.readlines() 
        nameList = []


        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])

        if name not in nameList:
            now = datetime.now()
            #dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{now}')

            send_email("mjwachira1@gmail.com", "NEW FACE DETECTED ",
                       "A new face was recently captured through the system, take action")
            

def send_email(sendto, subject, text):
    username = "smartsystems.frs@gmail.com"
    password = "nlmuvpyxlpyddwlv"
    for i in range(3):
        try:
            print("Sending Email to {} (trial {})...".format(sendto, i + 1))
            import smtplib, ssl
            # import ssl
            context = ssl.create_default_context()
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls(context=context)
            server.login(username, password)
            msg = 'Subject: {}\n\n{}'.format(subject, text)
            server.sendmail(username, sendto, msg)
            server.quit()
            print("Email sent!")
            break
        except Exception as e:
            print("Failed to send email due to Exception:")
            print(e)


#### FOR CAPTURING SCREEN RATHER THAN WEBCAM
# def captureScreen(bbox=(300,300,690+300,530+300)):
#     capScr = np.array(ImageGrab.grab(bbox))
#     capScr = cv2.cvtColor(capScr, cv2.COLOR_RGB2BGR)
#     return capScr
 
 #opens the camera

#for i in range(3):
try:
    cap = cv2.VideoCapture(0)
    #cap = cv2.VideoCapture("http://192.168.252.215:8080/video")
except Exception as e:
    print("Failed to start camera due to Exception:")
    print(e)
 
#cap = cv2.VideoCapture(0)


def gen_frames():
    while True:
        success, img = cap.read()
         #img = captureScreen()
        imgS = cv2.resize(img,(0,0),None,0.25,0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)
        for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
             #print(faceDis)
            matchIndex = np.argmin(faceDis)
            if matches[matchIndex]:
                name = Names[matchIndex].upper()
             #print(name)
             #creates a rectangle round a detected face
                y1,x2,y2,x1 = faceLoc
                y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
                cv2.rectangle(img,(x1,y1),(x2,y2),(0,0,255),2)
                cv2.rectangle(img,(x1,y2-35),(x2,y2),(0, 0, 255),cv2.FILLED)
                cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)

                Records(name)                        
                #f.writelines(f'\n{name},{dtString}')
                now = datetime.now()
                cv2.imwrite(f"static/detected/{name}.jpg", img)
          
         # send_email("mjwachira1@gmail.com", "NEW FACE DETECTED ", "A new face was recently captured through the system, take action")
        #converts frames of the video into bytes
        ret, buffer = cv2.imencode('.jpg', img)
        img = buffer.tobytes()
        yield (b'--frame\r\n' 
        b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')

        #send_email("mjwachira1@gmail.com", "NEW FACE DETECTED ", "A new face was recently captured through the system, take action")

@app.route('/face')
def index():
    #display the video on html page
    return render_template('face.html',bg_class='classy')
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/uploads', methods=["POST", "GET"])
def uploads():
    return render_template('uploads.html')
@app.route("/upload", methods=["POST", "GET"])
def upload():
    cursor = mysql.connection.cursor()
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    now = datetime.now()
    if request.method == 'POST':
        files = request.files.getlist('files[]')
        # print(files)
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                cur.execute("INSERT INTO images (file_name, uploaded_on) VALUES (%s, %s)", [filename, now])
                mysql.connection.commit()
            print(file)
        cur.close()
        flash('File(s) successfully uploaded')
    return redirect('/uploads')


UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
@app.route('/delete')
def main():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    result = cur.execute("SELECT * FROM images ORDER BY id")
    gallery = cur.fetchall()
    return render_template('delete.html', gallery=gallery)
@app.route('/delete/<int:get_ig>')
def delete(get_ig):
    cursor = mysql.connection.cursor()
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    result = cur.execute("SELECT * FROM images WHERE id = %s", [get_ig])
    data = cur.fetchone()
    filename = data['file_name']
    os.unlink(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    cur.execute('DELETE FROM images WHERE id = {0}'.format(get_ig))
    mysql.connection.commit()
    cur.close()
    print('File successfully deleted!')
    msg = 'Success deleted'
    return jsonify(msg)


@app.route('/reports')
def reports():
    with open("Records.csv") as file:
        reader = csv.reader(file)
        return render_template("reports.html",csv=reader)

@app.route('/about')
def about():
    return render_template("about.html")

if __name__=='__main__':
    app.run(debug=True)