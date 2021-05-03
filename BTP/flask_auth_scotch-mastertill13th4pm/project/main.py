# main.py

import time
import cv2 
from flask import Flask, render_template, Response
import numpy as np
import imutils
import datetime
import os
import smtplib
import threading
import multiprocessing
from email.message import EmailMessage

from flask import Blueprint
from flask_login import login_required, current_user

main = Blueprint('main', __name__)
# app = Flask(__name__)
EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')

sub = cv2.createBackgroundSubtractorMOG2()

#global variables
gun_cascade = cv2.CascadeClassifier('D:\\flask_auth_scotch-master\\project\\cascade.xml')
cap = cv2.VideoCapture(0)

# tosend = 0

msg = EmailMessage()
msg['Subject'] = 'Alert!!! Weapon Detected!!!'
msg['From'] = EMAIL_ADDRESS
msg['To'] = 'gupta170101022@iitg.ac.in'
msg.set_content('Weapon Detected in Home')
msg.add_alternative("""\<!DOCTYPE html>
<html>
    <body>
        <h1 style="color:SlateGray;">Please Check Camera Footage!</h1>
        <a href="http://10.9.1.24:5000/">Please check here</a>
    </body>
</html>""",subtype = 'html')


@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    # return render_template('profile.html', name=current_user.name)
    return render_template('js.html', name=current_user.name)



def sendMail():
    # global tosend
    # if tosend==0:
    #     return
    
    # print(tosend)
    # msg = EmailMessage()
    # msg['Subject'] = 'Alert!!! Weapon Detected!!!'
    # msg['From'] = EMAIL_ADDRESS
    # msg['To'] = 'gupta170101022@iitg.ac.in'
    # msg.set_content('Weapon Detected in Home')
    # msg.add_alternative("""\<!DOCTYPE html>
    # <html>
    #     <body>
    #         <h1 style="color:SlateGray;">Please Check Camera Footage!</h1>
    #         <a href="http://10.9.1.24:5000/">Please check here</a>
    #     </body>
    # </html>""",subtype = 'html')

    with open('detected.jpg','rb') as f:
        file_data = f.read()
        # print(f.name)
        altu,file_type = f.name.split('.')
        file_name = f.name
        # print(file_type)

    msg.add_attachment(file_data, maintype='image',subtype=file_type,filename = file_name)
    with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
        smtp.login(EMAIL_ADDRESS,EMAIL_PASSWORD) 
        smtp.send_message(msg)

    # tosend = 0


# def wait_till():
#     gun_exist = False
    
#     (grabbed, frame) = cap.read()

#     # if the frame could not be grabbed, then we have reached the end of the video

#     if not grabbed:
#         print('not grabbed')
#         return

#     # resize the frame, convert it to grayscale, and blur it
#     frame = imutils.resize(frame, width=500)
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     gray = cv2.GaussianBlur(gray, (21, 21), 0)
    
#     gun = gun_cascade.detectMultiScale(gray, 1.3, 5, minSize = (100, 100))
#     print(len(gun))
#     if len(gun) > 0:
#         gun_exist = True


#     for (x,y,w,h) in gun:
#         frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
#         roi_gray = gray[y:y+h, x:x+w]
#         roi_color = frame[y:y+h, x:x+w]    

#     # if the first frame is None, initialize it
#     if firstFrame is None:
#         firstFrame = gray

#     # draw the text and timestamp on the frame
#     cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
#                     (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
    
#     if gun_exist:
#         print("guns detected")
#         cv2.imwrite("detected.jpg", frame)
#     else:
#         print("guns NOT detected")
#     gun_exist = False
#     frame = cv2.imencode('.jpg', frame)[1].tobytes()
#     yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def gen():
    """Video streaming generator function."""
    # gun_cascade = cv2.CascadeClassifier('D:\\flask_auth_scotch-master\\project\\cascade.xml')
    # cap = cv2.VideoCapture(0)
    firstFrame = None

    # global tosend
# loop over the frames of the video

    gun_exist = False
    # Read until video is completed
    while True:
        (grabbed, frame) = cap.read()

        # if the frame could not be grabbed, then we have reached the end of the video
        if not grabbed:
            break

        # resize the frame, convert it to grayscale, and blur it
        frame = imutils.resize(frame, width=500)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        
        gun = gun_cascade.detectMultiScale(gray, 1.3, 5, minSize = (100, 100))
        # print(len(gun))
        if len(gun) > 0:
            gun_exist = True
            
        for (x,y,w,h) in gun:
            frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]    

        # if the first frame is None, initialize it
        if firstFrame is None:
            firstFrame = gray
            continue

        # draw the text and timestamp on the frame
        cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                        (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)


        if gun_exist:
            # print("guns detected")
            cv2.imwrite("detected.jpg", frame)
            # sendMail()

            # tosend = 1
            # print(tosend)
            # t1 = threading.Thread(target=sendMail, args=())
            # # t2 = threading.Thread(target=wait_till, args=())
            # t1.start()

            p1 = multiprocessing.Process(target=sendMail)
            p1.start()

            t_end = time.time() + 20
            firstFrame1 = None
            while time.time() < t_end:
                
                gun_exist1 = False
                (grabbed1, frame1) = cap.read()

                # if the frame could not be grabbed, then we have reached the end of the video

                if not grabbed1:
                    # print('not grabbed')
                    return

                # resize the frame, convert it to grayscale, and blur it
                frame1 = imutils.resize(frame1, width=500)
                gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
                gray1 = cv2.GaussianBlur(gray1, (21, 21), 0)
                
                gun1 = gun_cascade.detectMultiScale(gray1, 1.3, 5, minSize = (100, 100))
                # print(len(gun1))
                if len(gun1) > 0:
                    gun_exist1 = True


                for (x,y,w,h) in gun1:
                    frame1 = cv2.rectangle(frame1,(x,y),(x+w,y+h),(255,0,0),2)
                    roi_gray1 = gray1[y:y+h, x:x+w]
                    roi_color1 = frame1[y:y+h, x:x+w]    

                # if the first frame is None, initialize it
                if firstFrame1 is None:
                    firstFrame1 = gray1

                # draw the text and timestamp on the frame
                cv2.putText(frame1, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                                (10, frame1.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
                
                # if gun_exist1:
                #     # print("guns detected")
                #     cv2.imwrite("detected.jpg", frame1)
                # else:
                #     print("guns NOT detected")
                gun_exist1 = False
                frame1 = cv2.imencode('.jpg', frame1)[1].tobytes()
                yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame1 + b'\r\n')
                key = cv2.waitKey(1) & 0xFF

            # t1.join()

            p1.join()
        # else:
            # print("guns NOT detected")
        gun_exist = False
        # show the frame and record if the user presses a key
        frame = cv2.imencode('.jpg', frame)[1].tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        #cv2.imshow("Security Feed", frame)
        #key = cv2.waitKey(1) & 0xFF



@main.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
    
