import socket
import socketserver
from notification import *

s=socket.socket()
print('socket created')
port =3389
s.bind(('',port))
print('socket binded to %s' %(port))
s.listen(5)
print('socket is listening')
email_password=input('Podaj haslo do maila:')

while True:
    c,addr = s.accept()
    print('got connection form',addr)
    c.send('Ty for connecting'.encode())
    if c:
        print('wysylam maila')
        sendEmail("kk48302@zut.edu.pl",email_password)
    c.close()
    break


