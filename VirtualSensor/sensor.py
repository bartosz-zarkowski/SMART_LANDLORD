import time
from threading import Thread
import os
import socket
import json

class Sensor():
    def __init__(self,ID=1,OwnerID=1,SensorName="Name",LocationLatitude=1,LocationLongitude=1,LocationCity="City",LocationStreet="Street",checkTime=1,checkValue=100,maxkwhFlow=999999):
        self.ID=ID
        self.OwnerID=OwnerID
        self.SensorName=SensorName
        self.LocationLatitude=LocationLatitude
        self.LocationLongitude=LocationLongitude
        self.LocationCity=LocationCity
        self.LocationStreet=LocationStreet
        self.kWh=0
        self.kWhActuall = 0
        self.kwhFlow = [0]
        self.time=0
        self.checkTime=checkTime
        self.checkValue=checkValue
        self.maxkwhFlow=maxkwhFlow
        self.timecounter=0
        self.isSending=0

    def loop(self):
        while True:
            if self.kwhFlow[0]>0:
                self.kWhActuall+=self.kwhFlow[0]
            elif self.kWhActuall!=0 and self.kwhFlow[0]==0:
                self.kWhActuall=0
            self.kWh+=self.kwhFlow[0]
            time.sleep(1)

    def SendData(self,ErrorType):
        data = {"ID": str(self.ID), "OwnerID": str(self.OwnerID), "SensorName": str(self.SensorName),
                "LocationLatitude": str(self.LocationLatitude), "LocationLongitude": str(self.LocationLongitude),
                "LocationCity": str(self.LocationCity),
                "kWh": str(self.kWh), "kWhActuall": str(self.kWhActuall), "kwhFlow": str(self.kwhFlow),
                "time": str(self.time), "checkTime": str(self.checkTime), "checkValue": str(self.checkValue),
                "timecounter": str(self.timecounter),"errorType": str(ErrorType)}
        data = json.dumps(data)
        try:
            sock = socket.socket()
        except socket.error as err:
            print('Socket error because of %s' % (err))

        port = 3389
        address = "35.224.18.129"
        try:
            #print("Sending data")
            sock.connect((address, port))
            sock.send(data.encode())
        except socket.gaierror:

            print('There an error resolving the host')

    def SendStatusData(self):
        data = {"ID": str(self.ID), "OwnerID": str(self.OwnerID), "SensorName": str(self.SensorName),"kWh": str(self.kWh),"errorType": str(0)}
        data = json.dumps(data)
        try:
            sock = socket.socket()
        except socket.error as err:
            print('Socket error because of %s' % (err))

        port = 3389
        address = "35.224.18.129"
        try:
            #print("Sending data")
            sock.connect((address, port))
            sock.send(data.encode())
        except socket.gaierror:

            print('There an error resolving the host')

    def changeFlow(self,newFLow):
        self.kwhFlow[0]=newFLow

    def loopThread(self):
        nt = Thread(target=self.loop)
        nt.start()

    def changeFlowThread(self):
        newFlow=input("New Flow Value: ")
        newFlow=float(newFlow)
        nt = Thread(target=self.changeFlow,args=(newFlow,))
        nt.start()

    def FlowCheck(self):

        self.timecounter=0
        while True:

            if self.kwhFlow[0]==0.0:
                self.timecounter = 0
                self.kWhActuall=0

            if self.kwhFlow[0]>=self.maxkwhFlow and self.isSending==0:
                self.isSending = 1
                self.SendData(1)

            if  self.timecounter>=self.checkTime and self.kWhActuall>=self.checkValue and self.isSending==0:
                self.isSending=1
                self.SendData(2)

    def SendStatus(self):
       # print("Activated")
        while True:
            time.sleep(4)
           # print("Sending status")
            self.SendStatusData()


    def SendStatusThread(self):
        nt = Thread(target=self.SendStatus())
        nt.start()

    def Timer(self):
        time.sleep(60 - time.time() % 60)
        self.timecounter += 1

    def TimerThread(self):
        nt = Thread(target=self.Timer)
        nt.start()

    def ShowkWh(self):
        print(self.kWh)

    def ShowFLow(self):
        print(self.kwhFlow)

    def FlowCheckThread(self):
        nt = Thread(target=self.FlowCheck)
        nt.start()

    def ShowFlowThread(self):
        nt = Thread(target=self.ShowFLow)
        nt.start()

    def ShowkWhThread(self):
        nt = Thread(target=self.ShowkWh)
        nt.start()

    def Start(self):
        self.loopThread()
        self.TimerThread()
        self.FlowCheckThread()
        self.SendStatusThread()


def HomeList(Homes):
    while True:
        HomeID=input("Choose Home: ")
        Homes[int(HomeID)-1].printSensors()
        Homes[int(HomeID) - 1].printSensorOptions()

        input()
        os.system('cls')

class Home():
    def __init__(self,Sensors):
        self.SensorList=Sensors

    def printSensors(self):
        for sensor in self.SensorList:
            print(sensor.SensorName)

    def printSensorOptions(self):

        while True:
            SensorID = input("Choose sensor: ")
            print("1. Change flow")
            print("2. Show actuall flow")
            print("3. Show kWh")
            print("4. Exit")

            SensorOption = input("Choose option: ")

            if SensorOption == "1":
                self.SensorList[int(SensorID) - 1].changeFlowThread()

            elif SensorOption == "2":
                self.SensorList[int(SensorID) - 1].ShowFlowThread()

            elif SensorOption == "3":
                self.SensorList[int(SensorID) - 1].ShowkWhThread()
            elif SensorOption == "4":
                break

            input()
            os.system('cls')

if __name__=='__main__':
    s1=Sensor(1,1,"Nazwa1",1,1,"Miasto1","Ulica1",1,100,1)
    s2 = Sensor(2,2,"Nazwa2",2,2,"Miasto2","Ulica2",1,100,10000)

    nt1 = Thread(target=s1.Start)
    nt1.start()

    nt2 = Thread(target=s2.Start)
    nt2.start()

    s3 = Sensor(3, 1, "Nazwa3", 1, 1, "Miasto1", "Ulica1", 1, 100,10000)
    s4 = Sensor(4, 2, "Nazwa4", 2, 2, "Miasto2", "Ulica2", 1, 100,10000)

    nt3 = Thread(target=s3.Start)
    nt3.start()

    nt4 = Thread(target=s4.Start)
    nt4.start()

    Sensors=[s3,s4]


    dom1=Home([s1,s2])
    dom2=Home([s3,s4])


    HomeList([dom1,dom2])
    HomeList([dom1])