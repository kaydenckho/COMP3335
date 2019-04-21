import pymysql
import binascii
import os
import sys
#import Crypto.Cipher
from Crypto.Cipher import AES
import hashlib

def write_file(data, filename):
    with open(filename, 'wb') as file:
        file.write(data)
        file.close()
def padding (data):

    while len(data) % 16 != 0:
        
        data = data + " "
        
    return data

def depadding (data):
    pad = 0
    index = len(data) - 1
    while data[index] == " ":       
        pad = pad + 1   
        index = index - 1
    return data[:len(data) - pad]

email = "test@gmail.com"
password= "password"

##SF = password + email
SF = hashlib.sha1(password + email).hexdigest() #Key for AES encryption

cipherF = AES.new(SF[:32])

connection = pymysql.connect(host='mysql.comp.polyu.edu.hk',port=3306,user='...',passwd="...",db='...',charset='utf8')
cursor = connection.cursor()
sql="SELECT * from databsename where FID=5"
cursor.execute(sql)
record = cursor.fetchall()
for row in record:
    print("FID = ", row[0])
    print("Name = ", depadding(cipherF.decrypt(row[1].decode("hex"))))
    print("Extension = ", depadding(cipherF.decrypt(row[2].decode("hex"))))
    image =  depadding(cipherF.decrypt(row[3].decode("hex")))
    print("Owner = ", row[4])
    print("Permission = ", row[5])
    write_file(image, "C:\Users\KenHo\Desktop\image.jpg")
