import socket
from notification import *
s=socket.socket()
port =3389
s.bind(('',port))
s.listen(5)
email_password=input("Podaj haslo do maila: ")

while True:
    c,addr=s.accept()
    if c:
        sendEmail("officialkacper@gmail.com",email_password)
        c.send()
        c.close()
    break
