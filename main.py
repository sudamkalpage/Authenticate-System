############################################# IMPORTING ################################################

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mess
import tkinter.simpledialog as tsd
import cv2,os
import csv
import numpy as np
from PIL import Image
import pandas as pd
import datetime
import time
import webbrowser

#######################################  Colours ################################################################################################################ 
      
black= "#787567"
blue= "#040a5c"
purple = "#6839ad"

############################################# FUNCTIONS ################################################

def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)

###################################################################################

def check_haarcascadefile():
    exists = os.path.isfile("haarcascade_frontalface_default.xml")
    if exists:
        pass
    else:
        mess._show(title='Some file missing', message='Please contact us for help')
        window.destroy()

###################################################################################

def save_pass():
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel\psd.txt")
    if exists1:
        tf = open("TrainingImageLabel\psd.txt", "r")
        key = tf.read()
    else:
        master.destroy()
        new_pas = tsd.askstring('Old Password not found', 'Please enter a new password below', show='*')
        if new_pas == None:
            mess._show(title='No Password Entered', message='Password not set!! Please try again')
        else:
            tf = open("TrainingImageLabel\psd.txt", "w")
            tf.write(new_pas)
            mess._show(title='Password Registered', message='New password was registered successfully!!')
            return
    op = (old.get())
    newp= (new.get())
    nnewp = (nnew.get())
    if (op == key):
        if(newp == nnewp):
            txf = open("TrainingImageLabel\psd.txt", "w")
            txf.write(newp)
        else:
            mess._show(title='Error', message='Confirm new password again!!!')
            return
    else:
        mess._show(title='Wrong Password', message='Please enter correct old password.')
        return
    mess._show(title='Password Changed', message='Password changed successfully!!')
    master.destroy()

###################################################################################

def change_pass():
    global master
    master = tk.Tk()
    master.geometry("400x160")
    master.resizable(False,False)
    master.title("Change Password")
    master.configure(background="white")
    lbl4 = tk.Label(master,text='    Enter Old Password',bg='white',font=('times', 12, ' bold '))
    lbl4.place(x=10,y=10)
    global old
    old=tk.Entry(master,width=15 ,fg="black",relief='solid',font=('times', 12, ' bold '),show='*')
    old.place(x=200,y=10)
    lbl5 = tk.Label(master, text='   Enter New Password', bg='white', font=('times', 12, ' bold '))
    lbl5.place(x=10, y=45)
    global new
    new = tk.Entry(master, width=15, fg="black",relief='solid', font=('times', 12, ' bold '),show='*')
    new.place(x=200, y=45)
    lbl6 = tk.Label(master, text='Confirm New Password', bg='white', font=('times', 12, ' bold '))
    lbl6.place(x=10, y=80)
    global nnew#
    nnew = tk.Entry(master, width=15, fg="black", relief='solid',font=('times', 12, ' bold '),show='*')
    nnew.place(x=200, y=80)
    cancel=tk.Button(master,text="Cancel", command=master.destroy ,fg="black"  ,bg=purple ,height=1,width=15 , activebackground = "white" ,font=('times', 10, ' bold '))
    cancel.place(x=200, y=120)
    save1 = tk.Button(master, text="Save", command=save_pass, fg="white", bg=blue, height = 1,width=15, activebackground="white", font=('times', 10, ' bold '))
    save1.place(x=10, y=120)
    master.mainloop()

#####################################################################################

def psw():
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel\psd.txt")
    if exists1:
        tf = open("TrainingImageLabel\psd.txt", "r")
        key = tf.read()
    else:
        new_pas = tsd.askstring('Old Password not found', 'Please enter a new password below', show='*')
        if new_pas == None:
            mess._show(title='No Password Entered', message='Password not set!! Please try again')
        else:
            tf = open("TrainingImageLabel\psd.txt", "w")
            tf.write(new_pas)
            mess._show(title='Password Registered', message='New password was registered successfully!!')
            return
    password = tsd.askstring('Password', 'Enter Password', show='*')
    if (password == key):
        TrainImages()
    elif (password == None):
        pass
    else:
        mess._show(title='Wrong Password', message='You have entered wrong password')

######################################################################################

def clear():
    txt.delete(0, 'end')
    res = "1)Take Images  >>>  2)Register"
    message1.configure(text=res)

def clear2():
    txt2.delete(0, 'end')

def clear3():
    txt3.delete(0, 'end')

def clear4():
    txt4.delete(0, 'end')

def clear5():
    txt5.delete(0, 'end')

def clear6():
    txt6.delete(0, 'end')

#######################################################################################

def CaptureImages():
    popup = lambda : tk.messagebox.showinfo(title="Info", message="Please press q to stop Capturing !")
    popup()
    check_haarcascadefile()
    columns = ['SERIAL NO.', '', 'ID', '', 'NAME', '', 'EMAIL', '', 'PASSWORD']
    assure_path_exists("StudentDetails/")
    assure_path_exists("TrainingImage/")
    serial = 0
    exists = os.path.isfile("StudentDetails\StudentDetails.csv")
    if exists:
        with open("StudentDetails\StudentDetails.csv", 'r') as csvFile1:
            reader1 = csv.reader(csvFile1)
            for l in reader1:
                serial = serial + 1
        serial = (serial // 2)
        csvFile1.close()
    else:
        with open("StudentDetails\StudentDetails.csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(columns)
            serial = 1
        csvFile1.close()
    Id = (txt.get())
    name = (txt2.get())
    email=(txt3.get())
    password=(txt6.get())
    if ((name.isalpha()) or (' ' in name)):
        cam = cv2.VideoCapture(0)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        sampleNum = 0
        while (True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                # incrementing sample number
                sampleNum = sampleNum + 1
                # saving the captured face in the dataset folder TrainingImage
                cv2.imwrite("TrainingImage\ " + name + "." + str(serial) + "." + Id + '.' + str(sampleNum) + ".jpg",
                            gray[y:y + h, x:x + w])
                # display the frame
                cv2.imshow('Taking Images', img)
            # wait for 100 miliseconds
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            # break if the sample number is morethan 100
            elif sampleNum > 100:
                break
        cam.release()
        cv2.destroyAllWindows()
        res = "Images Taken for ID : " + Id
        row = [serial, '', Id, '', name, '', email, '', password]
        with open('StudentDetails\StudentDetails.csv', 'a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        message1.configure(text=res)
    else:
        if (name.isalpha() == False):
            res = "Enter Correct name"
            message.configure(text=res)

########################################################################################

def TrainImages():
    check_haarcascadefile()
    assure_path_exists("TrainingImageLabel/")
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    faces, ID = getImagesAndLabels("TrainingImage")
    try:
        recognizer.train(faces, np.array(ID))
    except:
        mess._show(title='No Registrations', message='Please Register someone first!!!')
        return
    recognizer.save("TrainingImageLabel\Trainner.yml")
    res = "Profile Saved Successfully"
    message1.configure(text=res)
    message.configure(text='Total Registrations till now  : ' + str(ID[0]))
    popup = lambda : tk.messagebox.showinfo(title="Info", message="Sign Up was Successfull !")
    popup()

############################################################################################3

def getImagesAndLabels(path):
    # get the path of all the files in the folder
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    # create empth face list
    faces = []
    # create empty ID list
    Ids = []
    # now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        # loading the image and converting it to gray scale
        pilImage = Image.open(imagePath).convert('L')
        # Now we are converting the PIL image into numpy array
        imageNp = np.array(pilImage, 'uint8')
        # getting the Id from the image
        ID = int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(ID)
    return faces, Ids

###########################################################################################

def TrackImages():
    check_haarcascadefile()
    assure_path_exists("Attendance/")
    assure_path_exists("StudentDetails/")

    msg = ''
    i = 0
    j = 0
    recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
    exists3 = os.path.isfile("TrainingImageLabel\Trainner.yml")
    if exists3:
        recognizer.read("TrainingImageLabel\Trainner.yml")
    else:
        mess._show(title='Data Missing', message='Please click on Save Profile to reset data!!')
        return
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath);

    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Id', '', 'Name', '', 'Date', '', 'Time']
    exists1 = os.path.isfile("StudentDetails\StudentDetails.csv")
    if exists1:
        df = pd.read_csv("StudentDetails\StudentDetails.csv")
    else:
        mess._show(title='Details Missing', message='Students details are missing, please check!')
        cam.release()
        cv2.destroyAllWindows()
        window.destroy()
    wantbreak=False
    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        if wantbreak==True:
            break
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
            serial, conf = recognizer.predict(gray[y:y + h, x:x + w])
            if (conf < 50):
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                aa = df.loc[df['SERIAL NO.'] == serial]['NAME'].values
                ID = df.loc[df['SERIAL NO.'] == serial]['ID'].values
                EMAIL = str(df.loc[df['SERIAL NO.'] == serial]['EMAIL'].values[0])
                PASSWORD = str(df.loc[df['SERIAL NO.'] == serial]['PASSWORD'].values[0])
                ID = str(ID)         
                ID = ID[1:-1]
                bb = str(aa)
                bb = bb[2:-2]
                attendance = [str(ID), '', bb, '', str(date), '', str(timeStamp)]
                if aa != None:
                    print(EMAIL)
                    print(PASSWORD)
                    webbrowser.open_new('https://google.com')
                    wantbreak=True
                    break

            else:
                Id = 'Unknown'
                bb = str(Id)
            cv2.putText(im, str(bb), (x, y + h), font, 1, (255, 255, 255), 2)
        cv2.imshow('Taking Attendance', im)
        if (cv2.waitKey(1) == ord('q')):
            break
    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
    exists = os.path.isfile("Attendance\Attendance_" + date + ".csv")
    if exists:
        with open("Attendance\Attendance_" + date + ".csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(attendance)
        csvFile1.close()
    else:
        with open("Attendance\Attendance_" + date + ".csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(col_names)
            writer.writerow(attendance)
        csvFile1.close()
    with open("Attendance\Attendance_" + date + ".csv", 'r') as csvFile1:
        reader1 = csv.reader(csvFile1)
        for lines in reader1:
            i = i + 1
            if (i > 1):
                if (i % 2 != 0):
                    iidd = str(lines[0]) + '   '
    csvFile1.close()
    cam.release()
    cv2.destroyAllWindows()
 
#################################################################################################

def logIn():
    email=txt4.get()
    password= txt5.get()
    print(email,password)
    webbrowser.open_new('https://google.com')

######################################## USED STUFFS ############################################
    
global key
key = ''

ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
day,month,year=date.split("-")

mont={'01':'January',
      '02':'February',
      '03':'March',
      '04':'April',
      '05':'May',
      '06':'June',
      '07':'July',
      '08':'August',
      '09':'September',
      '10':'October',
      '11':'November',
      '12':'December'
      }

######################################## GUI FRONT-END ##########################################################################################################

window = tk.Tk()
window.geometry("1000x600")
window.resizable(True,False)
window.title("Online Food Ordering System")
window.configure(background='#A239EA')

# Add background image 
bg = tk.PhotoImage(file = "S:/Projects/face recognition/Face_recognition_based_attendance_system/bg.png")
canvas1 = tk.Canvas( window, width = 1120,height = 720)
canvas1.pack(fill = "both", expand = True)
canvas1.create_image( 0, 0, image = bg, anchor = "nw")

# Create Frames
frame1 = tk.Frame(canvas1, bg=black)
frame1.place(relx=0.05, rely=0.07, relwidth=0.39, relheight=0.80)

frame2 = tk.Frame(canvas1   , bg=black)
frame2.place(relx=0.55, rely=0.07, relwidth=0.38, relheight=0.80)


# Create Frames
head2 = tk.Label(frame2, text="            SignUp            ", fg="white",bg=blue ,font=('times', 25, ' bold ') )
head2.place(x=20, y=0 )

head1 = tk.Label(frame1, text="            Login          ", fg="white",bg=blue ,font=('times', 25, ' bold ') )
head1.place(x=40,y=0)

lb4 = tk.Label(frame1, text="Email",width=20  ,height=1  ,fg="black"  ,bg=black ,font=('times', 17, ' bold ') )
lb4.place(x=40, y=140)  

txt4 = tk.Entry(frame1,width=30 ,fg="black",font=('times', 15, ' bold '))
txt4.place(x=30, y=173)

lbl5 = tk.Label(frame1, text="Password",width=20  ,fg="black"  ,bg=black ,font=('times', 17, ' bold '))
lbl5.place(x=40, y=225)

txt5 = tk.Entry(frame1,width=30 ,show="*",fg="black",font=('times', 15, ' bold ')  )
txt5.place(x=30, y=258)

lbl = tk.Label(frame2, text="Id Number",width=20  ,height=1  ,fg="black"  ,bg=black ,font=('times', 17, ' bold ') )
lbl.place(x=40, y=140)

txt = tk.Entry(frame2,width=30 ,fg="black",font=('times', 15, ' bold '))
txt.place(x=30, y=173)

lbl2 = tk.Label(frame2, text="Your Name",width=20  ,fg="black"  ,bg=black ,font=('times', 17, ' bold '))
lbl2.place(x=40, y=55)

txt2 = tk.Entry(frame2,width=30 ,fg="black",font=('times', 15, ' bold ')  )
txt2.place(x=30, y=88)

lbl3= tk.Label(frame2, text="Email",width=20  ,fg="black"  ,bg=black ,font=('times', 17, ' bold '))
lbl3.place(x=40, y=225)

txt3 = tk.Entry(frame2,width=30 ,fg="black",font=('times', 15, ' bold ')  )
txt3.place(x=30, y=258)

lbl6= tk.Label(frame2, text="Password",width=20  ,fg="black"  ,bg=black ,font=('times', 17, ' bold '))
lbl6.place(x=40, y=310)

txt6 = tk.Entry(frame2,width=30 ,show="*",fg="black",font=('times', 15, ' bold ')  )
txt6.place(x=30, y=343)

message1 = tk.Label(frame2, text="1)Take Images  >>>  2)Save your Data" ,bg=black ,fg="black"  ,width=39 ,height=1, activebackground = blue ,font=('times', 15, ' bold '))
# message1.place(x=7, y=230)

message = tk.Label(frame2, text="" ,bg=black ,fg="black"  ,width=39,height=1, activebackground = "yellow" ,font=('times', 16, ' bold '))
# message.place(x=0, y=450)
res=0
exists = os.path.isfile("StudentDetails\StudentDetails.csv")
if exists:
    with open("StudentDetails\StudentDetails.csv", 'r') as csvFile1:
        reader1 = csv.reader(csvFile1)
        for l in reader1:
            res = res + 1
    res = (res // 2) - 1
    csvFile1.close()
else:
    res = 0
# message.configure(text='Total Registered Members : '+str(res))

##################### MENUBAR #################################

menubar = tk.Menu(window,relief='ridge')
filemenu = tk.Menu(menubar,tearoff=0)
filemenu.add_command(label='Change Password', command = change_pass)
filemenu.add_command(label='Exit',command = window.destroy)
menubar.add_cascade(label='Help',font=('times', 29, ' bold '),menu=filemenu)

###################### BUTTONS ##################################

clearButton4 = tk.Button(frame1, text="Clear", command=clear4  ,fg="black"  ,bg=purple ,width=5 , activebackground = "white" ,font=('times', 11, ' bold '))
clearButton4.place(x=315, y=172) 
clearButton5 = tk.Button(frame1, text="Clear", command=clear5  ,fg="black"  ,bg=purple  ,width=5 , activebackground = "white" ,font=('times', 11, ' bold '))
clearButton5.place(x=315, y=257) 
clearButton = tk.Button(frame2, text="Clear", command=clear2  ,fg="black"  ,bg=purple  ,width=5 ,activebackground = "white" ,font=('times', 11, ' bold '))
clearButton.place(x=315, y=86)
clearButton2 = tk.Button(frame2, text="Clear", command=clear  ,fg="black"  ,bg=purple  ,width=5 , activebackground = "white" ,font=('times', 11, ' bold '))
clearButton2.place(x=315, y=172) 
clearButton3 = tk.Button(frame2, text="Clear", command=clear3  ,fg="black"  ,bg=purple  ,width=5 , activebackground = "white" ,font=('times', 11, ' bold '))
clearButton3.place(x=315, y=257) 
clearButton6 = tk.Button(frame2, text="Clear", command=clear6  ,fg="black"  ,bg=purple  ,width=5 , activebackground = "white" ,font=('times', 11, ' bold '))
clearButton6.place(x=315, y=342)    
takeImg = tk.Button(frame2, text="Capture Images", command=CaptureImages   ,bg="#040a5c"  ,width=12  ,height=1, activebackground = "white",fg="white" ,font=('times', 15, ' bold '))
takeImg.place(x=30, y=410)
signUp = tk.Button(frame2, text="Sign Up", command=psw  ,bg=blue  ,width=10  ,height=1, activebackground = "white" ,fg="white",font=('times', 15, ' bold '))
signUp.place(x=230, y=410)
trackImg = tk.Button(frame1, text="Face Recognition", command=TrackImages  ,fg="white"  ,bg=blue  ,width=25  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
trackImg.place(x=30,y=80)
logIn = tk.Button(frame1, text="Log in", command=logIn  ,fg="white"  ,bg=blue  ,width=25 ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
logIn.place(x=30, y=350)

##################### END ######################################

window.configure(menu=menubar)
window.mainloop()




