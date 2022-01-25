import socket
import socketserver
from notification import *
import json
import mariadb
import datetime
import time
from threading import Thread

class Timer():
    def __init__(self):
        self.time=datetime.datetime.now()
        self.sensorIDs=[]
        self.sensorDates=[]

    def TikTak(self):
        while True:
            time.sleep(10)
            self.time=datetime.datetime.now()
            
            for sensorID in self.sensorIDs:
                duration=Timer.time - self.sensorDates[self.sensorIDs.index(sensorID)] 
                minutes=duration.total_seconds()/60
                print(minutes)
                if minutes>2:
                    cur.execute("UPDATE sensors SET status=False WHERE sensorId=?;",(sensorID,))
                    conn.commit()

    def TikTakThread(self):
        nt=Thread(target=self.TikTak)
        nt.start()

    def Start(self):
        self.TikTakThread()
    


s=socket.socket()
print('socket created')
port =3389
s.bind(('',port))
print('socket binded to %s' %(port))
s.listen(5)
print('socket is listening')
email_password=input('Podaj haslo do maila:')

conn = mariadb.connect(
    user="landlord",
    password="hardbread",
    host="localhost",
    database="SmartLandLord")
cur= conn.cursor()
print("Uzyskano polaczenie z baza danych")

Timer=Timer()
Timer.Start()

while True:
    print(Timer.time)
    c,addr = s.accept()
    data=c.recv(4096)
    data=data.decode()
    print(data)
    data=json.loads(data)
    print(data["ID"])
    if data!=None and int(data["errorType"])!=0:
        sendEmail('officialkacper@gmail.com',email_password,int(data["errorType"]))
    elif data!=None and int(data["errorType"])==0:
        if int(data["ID"]) in Timer.sensorIDs:
            Timer.sensorDates[Timer.sensorIDs.index(int(data["ID"]))]=datetime.datetime.now()
            cur.execute("UPDATE sensors SET lastActive=NOW(), status=True WHERE sensorId=?;",(data["ID"],))
            conn.commit()
        else:
            Timer.sensorIDs.append(int(data["ID"]))
            Timer.sensorDates.append(datetime.datetime.now())

        cur.execute("UPDATE sensors SET lastActive=NOW(), status=True WHERE sensorId=?;",(data["ID"],))
        conn.commit()
        

    data=None
    c.close()


