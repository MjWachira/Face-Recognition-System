from flask import Flask, redirect, request, send_file, url_for, render_template, Response
import cv2
import face_recognition
import numpy as np
import os
from datetime import datetime

app=Flask(__name__)

#reading pictures and their names from the folder.
path = 'MyImages'
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
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString}')

def send_email(sendto, subject, text):
    username = "smartsystems.frs@gmail.com" # Change this!
    password = "nlmuvpyxlpyddwlv" # Change this!
    for i in range(3):
        try:
            print("Sending Email to {} (trial {})...".format(sendto, i+1))
            import smtplib,ssl
           # import ssl
            context=ssl.create_default_context()
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
#cap = cv2.VideoCapture("http://192.168.137.98:8080/video")
cap = cv2.VideoCapture(0)
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
                cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                Records(name)
                send_email("mjwachira1@gmail.com", "NEW FACE DETECTED ", "A new face was recently captured through the system, take action")
            #converts frames of the video into bytes
        ret, buffer = cv2.imencode('.jpg', img)
        img = buffer.tobytes()
        yield (b'--frame\r\n' 
        b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')
@app.route('/')
def index():
    #display the video on html page
    return render_template('face.html')
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
if __name__=='__main__':
    app.run(debug=True)