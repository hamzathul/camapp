import  tensorflow
import keras
import face_recognition
import cv2

from yolo import check

id=[]
name=[]
photo=[]

landmark=[]



from DBConnection import Db
db=Db()

qry="select * from myapp_student"

res=db.select(qry)


mpath="C:\\Users\\Lenovo\\PycharmProjects\\Examhall\\media\\"

for i in res:

    id.append(i['id'])
    name.append(i['name'])
    photo.append(mpath+ i['photo'].replace("/media/",""))

    picture_of_me = face_recognition.load_image_file(mpath+ i['photo'].replace("/media/",""))
    my_face_encoding = face_recognition.face_encodings(picture_of_me)[0]

    print(my_face_encoding)
    landmark.append(my_face_encoding)

cap=cv2.VideoCapture(0)

while(True):

    ret,frame=cap.read()


    cv2.imshow("window",frame)
    cv2.waitKey(10)

    cv2.imwrite("a.jpg",frame)

    aa=check("a.jpg")
    import datetime

    fname = datetime.datetime.now().strftime("%Y%m%d%H%M%f") + ".jpg"

    cv2.imwrite(mpath + fname, frame)

    p = "/media/" + fname

    qry = "INSERT INTO myapp_abnormalactivity (DATE, TIME, TYPE, CONTENT, PHOTO) VALUES (CURDATE(), CURTIME(), 'device', '" +aa+ "','" + p + "')"
    db.insert(qry)

    picture_of_me = face_recognition.load_image_file("a.jpg")
    my_face_encoding = face_recognition.face_encodings(picture_of_me)
    print(len(my_face_encoding))

    if len(my_face_encoding)>0:

        d=0

        for i in range(0,len(my_face_encoding)):

            s=my_face_encoding[i]

            k=face_recognition.compare_faces(landmark,s,tolerance=.5)
            print(k)

            if True in k:
                d=d+1



        if len(my_face_encoding)> d:



            msa= len(my_face_encoding)- d
            import datetime

            fname= datetime.datetime.now().strftime("%Y%m%d%H%M%f")+".jpg"

            cv2.imwrite(mpath+fname, frame)

            p="/media/"+fname


            qry="INSERT INTO myapp_abnormalactivity (DATE, TIME, TYPE, CONTENT, PHOTO) VALUES (CURDATE(), CURTIME(), 'unknown person', '"+str(msa)+'count of unknown person'+"', '"+p+"')"
            db.insert(qry)





    # my_face_encoding = face_recognition.face_encodings(picture_of_me)[1]



