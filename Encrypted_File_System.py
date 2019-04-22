# -*- coding: utf-8 -*-
from Tkinter import *
import tkMessageBox
import tkFileDialog
from PIL import Image, ImageTk
import winsound
import MySQLdb
import hashlib
from Crypto.Cipher import AES
import smtplib
from smtplib import SMTPRecipientsRefused
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os

# for aes encryption #
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

###
# database connection #
global db
db = MySQLdb.connect(host ='192.168.1.102', user ='admin', passwd = "admin", db = 'comp3335', charset ='utf8')

global cursor
cursor = db.cursor()
###

# favicon.ico path
ico_path = "./img/favicon.ico"

# bgm path

bgm_path = "./bgm/bgm.wav"

class AnimatedGIF(Label, object):
    def __init__(self, master, path, forever=True):
        self._master = master
        self._loc = 0
        self._forever = forever

        self._is_running = False

        im = Image.open(path)
        self._frames = []
        i = 0
        try:
            while True:
                photoframe = ImageTk.PhotoImage(im.copy().convert('RGBA'))
                self._frames.append(photoframe)

                i += 1
                im.seek(i)
        except EOFError: pass
        self._last_index = len(self._frames) - 1
        try:
            self._delay = im.info['duration']
        except:
            self._delay = 100
        self._callback_id = None
        super(AnimatedGIF, self).__init__(master, image=self._frames[0])

    def start_animation(self, frame=None):
        if self._is_running: return
        if frame is not None:
            self._loc = 0
            self.configure(image=self._frames[frame])
        self._master.after(self._delay, self._animate_GIF)
        self._is_running = True

    def stop_animation(self):
        if not self._is_running: return
        if self._callback_id is not None:
            self.after_cancel(self._callback_id)
            self._callback_id = None
        self._is_running = False

    def _animate_GIF(self):
        self._loc += 1
        self.configure(image=self._frames[self._loc])
        if self._loc == self._last_index:
            if self._forever:
                self._loc = 0
                self._callback_id = self._master.after(self._delay, self._animate_GIF)
            else:
                self._callback_id = None
                self._is_running = False
        else:
            self._callback_id = self._master.after(self._delay, self._animate_GIF)

    def pack(self, start_animation=True, **kwargs):
        if start_animation:
            self.start_animation()
        super(AnimatedGIF, self).pack(**kwargs)

    def grid(self, start_animation=True, **kwargs):
        if start_animation:
            self.start_animation()
        super(AnimatedGIF, self).grid(**kwargs)

    def place(self, start_animation=True, **kwargs):
        if start_animation:
            self.start_animation()
        super(AnimatedGIF, self).place(**kwargs)

    def pack_forget(self, **kwargs):
        self.stop_animation()
        super(AnimatedGIF, self).pack_forget(**kwargs)

    def grid_forget(self, **kwargs):
        self.stop_animation()
        super(AnimatedGIF, self).grid_forget(**kwargs)

    def place_forget(self, **kwargs):
        self.stop_animation()
        super(AnimatedGIF, self).place_forget(**kwargs)

# registration page
def register():
    def marquee(widget):
        global string1
        global instruction
        widget.pack_forget()
        temp = string1[0]
        string1 = string1[1:]
        string1 += temp
        instruction.set(string1)
        widget.pack()
        widget.after(350, marquee, widget)

    global registration
    global string1
    global instruction
    registration = Toplevel(index)
    registration.title("Register")
    registration.geometry("504x300")
    registration.resizable(0, 0)
    registration.iconbitmap(ico_path)
    l = AnimatedGIF(registration, "./img/Bg1.gif")
    l.place(x=0,y=0)

    # Register button event - registration
    def register_user():
        username_info = username.get()
        password_info = password.get()
        password_confirm_info = password_confirm.get()
        email_info = email.get()
        password_entry.delete(0, END)
        password_confirm_entry.delete(0, END)

        if (username_info != "" and password_info != "" and password_confirm_info != "" and password_confirm_info == password_info):

            # Function: Registration #

            password_sha1 = hashlib.sha1(password_info)

            password_hash = password_sha1.hexdigest() # Hash of Password

            key_concat = password_info + username_info

            key_concat_hash = hashlib.sha1(key_concat).hexdigest() # Key for aes encryption of user information (only use first 32 bits of Hash of (Password + Username))

            cipherU = AES.new(key_concat_hash[:32]) # for aes encryption of user information

            email_encrpyted = cipherU.encrypt(padding(email_info)).encode("hex") # Encrypted Email

            cursor.execute("SELECT * FROM USERS WHERE Name = %s" , (username_info,))


            rc = cursor.rowcount

            if rc > 0:

                tkMessageBox.showwarning("Warning","This username already exists")

            else:

                cursor.execute ("INSERT INTO Users (Name, Password, Email) VALUES (%s, %s, %s)" , (username_info, password_hash, email_encrpyted,)) # Insert the user info

                db.commit()
            ##########

                tkMessageBox.showinfo("COMP3335 - Encrypted File System","Your account is created successfully.")

                registration.destroy()

        else:
            if username_info == "":
                tkMessageBox.showinfo("COMP3335 - Encrypted File System","Username should not be empty")
            elif email_info =="":
                tkMessageBox.showinfo("COMP3335 - Encrypted File System","Email should not be empty")
            elif '@' not in email_info:
                tkMessageBox.showinfo("COMP3335 - Encrypted File System","Format of email is invalid.")
            elif password_info == "":
                tkMessageBox.showinfo("COMP3335 - Encrypted File System","Password should not be empty")
            elif password_confirm_info == "":
                tkMessageBox.showinfo("COMP3335 - Encrypted File System","Please confirm your password.")
            else:
                tkMessageBox.showinfo("COMP3335 - Encrypted File System","The two passwords are not the same.")

    global username
    global password
    global password_confirm
    global username_entry
    global email_entry
    global password_entry
    global password_confirm_entry

    username = StringVar()
    email = StringVar()
    password = StringVar()
    password_confirm = StringVar()

    string1 = " -- Create your own account now! -- Please input the neccessary information below."
    instruction = StringVar(registration)
    instruction.set(string1)
    show = Label(registration, textvariable=instruction,font=("Arial", 15), bg="cyan", width="300", height="1")
    show.pack()
    marquee(show)

    username_label = Label(registration, text="Username: ")
    username_label.place(x=153,y=70)
    username_entry = Entry(registration, textvariable=username)
    username_entry.place(x=220,y=72)

    email_label = Label(registration, text="Email Address: ")
    email_label.place(x=132,y=110)
    email_entry = Entry(registration, textvariable=email)
    email_entry.place(x=220,y=112)

    password_label = Label(registration, text="Password: ")
    password_label.place(x=156,y=150)
    password_entry = Entry(registration, textvariable=password, show='*')
    password_entry.place(x=220,y=152)

    password_confirm_label = Label(registration, text="Confirm Password: ")
    password_confirm_label.place(x=109,y=190)
    password_confirm_entry = Entry(registration, textvariable=password_confirm, show='*')
    password_confirm_entry.place(x=220,y=192)

    Button(registration, text="Register", width=10, height=1, bg="Gray", command = register_user).place(x=220,y=250)

# Login page
def login_page():
    global login
    login = Toplevel(index)
    login.title("Login")
    login.geometry("504x300")
    login.resizable(0, 0)
    login.iconbitmap(ico_path)
    l = AnimatedGIF(login, "./img/Bg2.gif")
    l.place(x=0,y=0)
    Label(login, text="Please enter your username and password.", bg="cyan", width="300", height="1", font=("Arial", 15)).pack()

    # lgoin button event - login_verify
    def login_verify():
        username = username_verify.get()
        password = password_verify.get()
        username_login_entry.delete(0, END)
        password_login_entry.delete(0, END)
        if username == "":
            tkMessageBox.showwarning("Warning","Please enter your username.")
        elif password == "":
            tkMessageBox.showwarning("Warning","Please enter your password.")
        else:
            # Function: Login && Authentication #

            password_sha1 = hashlib.sha1(password)

            password_hash = password_sha1.hexdigest() # Hash of Password

            cursor.execute("SELECT Password FROM USERS WHERE Name = %s" , (username,))


            rc = cursor.rowcount

            if rc == 0: # Error if no such user

                tkMessageBox.showwarning("Warning","Password or Username is incorrect.\nPlease try again.")

            else :

                res = str(cursor.fetchone()[0])

                if password_hash != res: # Error if password is wrong

                    tkMessageBox.showwarning("Warning","Password or Username is incorrect.\nPlease try again.")

                else:

                    cursor.execute("SELECT * FROM USERS WHERE Name = %s" , (username,))

                    result = cursor.fetchone()

                    global GUid # GLOBAL Uid

                    GUid = result[0]

                    global GUsername # GLOBAL Username

                    GUsername = username

                    global GSU # GLOBAL Key for aes encryption of user info (only use first 32 bits of Hash of (Password + Username))

                    user_concat = password+GUsername

                    GSU = hashlib.sha1(user_concat).hexdigest()

                    global GCipherU # GLOBAL for aes encryption of user info

                    GCipherU = AES.new(GSU[:32])

                    global GEmail # GLOBAL Email

                    email = result[3]
                    GEmail = depadding(GCipherU.decrypt(email.decode("hex")))

                    global GSF # GLOBAL Key for aes encryption of file info (only use first 32 bits of Hash of (Password + Email))

                    file_concat = password+GEmail
                    GSF = hashlib.sha1(file_concat).hexdigest()

                    global GCipherF # GLOBAL for aes encryption of file info
                    GCipherF = AES.new(GSF[:32])

                    login.destroy()
                    menu_page()

            ##########

    global username_verify
    global password_verify

    username_verify = StringVar()
    password_verify = StringVar()

    global username_login_entry
    global password_login_entry

    login_label = Label(login, text="Username : ")
    login_label.place(x=150,y=110)
    username_login_entry = Entry(login, textvariable=username_verify)
    username_login_entry.place(x=220,y=112)
    passwd_label = Label(login, text="Password : ")
    passwd_label.place(x=153,y=150)
    password_login_entry = Entry(login, textvariable=password_verify, show= '*')
    password_login_entry.place(x=220,y=152)

    Button(login, text="Login", width=10, height=1, command = login_verify).place(x=220,y=200)

# Go to main menu if login success
def menu_page():
    global menu
    menu = Toplevel(index)
    menu.title("COMP3335 - Encrypted File System")
    menu.geometry("504x300")
    menu.iconbitmap(ico_path)
    menu.resizable(0, 0)
    l = AnimatedGIF(menu, "./img/Bg3.gif")
    l.place(x=0,y=0)

    def my_files_page():
        global my_files
        my_files = Toplevel(menu)
        my_files.title("My Files")
        my_files.geometry("500x350")
        my_files.iconbitmap(ico_path)
        my_files.resizable(0, 0)

        def upload():
            filename = tkFileDialog.askopenfile(initialdir = "/",title = "Select file")
            filename = str(filename)
            quote1 = filename.find('\'')
            quote2 = filename.find('\'',filename.find('\'')+1)
            filepath = filename[quote1+1:quote2]

            # Function: Upload #

            quote = filepath.rfind('/')
            dot = filepath.rfind('.')
            Name = filepath[quote+1:dot] # name of input file

            encryptedName = GCipherF.encrypt(padding(Name)).encode("hex") # Encrypted input file name

            Extension = filepath[dot+1:] # extension of input file

            encryptedExtension = GCipherF.encrypt(padding(Extension)).encode("hex") # Encrypted input file extension

            cursor.execute ("SELECT * FROM Files WHERE Name = %s and Extension = %s and Owner = %s", (encryptedName,encryptedExtension,GUid,))

            rc = cursor.rowcount;

            if rc != 0:

                tkMessageBox.showwarning("Warning","File with name (" + Name + "." + Extension + ") already exists in your file system")

            else:

                lb.insert(END, Name+"."+Extension)

                with open(filepath, "rb") as f: # read input file content

                    Content = f.read() # content of input file

                    f.close()

                encryptedContent = GCipherF.encrypt(padding(Content)).encode("hex") # Encrypted input file content

                Permission = bin(0b1 << (GUid - 1)) # Permission (Nth bit from the right refer to the access control for user with Uid N (1: has access, 0: no access)

                cursor.execute ("INSERT INTO Files (Name, Extension, Content, Owner, Permission) VALUES (%s, %s, %s, %s, %s)" , (encryptedName, encryptedExtension, encryptedContent, GUid, Permission,)) # Insert the file info

                db.commit()

                tkMessageBox.showinfo("COMP3335 - Encrypted File System","upload " + Name + "." + Extension + " successfully")

            ##########

        def delete():
            try:
                filename = lb.get(lb.curselection())

                # Function: Delete #
                dot = filename.rfind('.')
                Name = filename[:dot] # name of file to be deleted
                Extension = filename[dot+1:] # extension of input file

                encryptedName = GCipherF.encrypt(padding(Name)).encode("hex") # Encrypted file name
                encryptedExtension = GCipherF.encrypt(padding(Extension)).encode("hex") # Encrypted input file extension

                cursor.execute ("DELETE FROM Files WHERE Name = %s and Extension = %s and Owner = %s" , (encryptedName, encryptedExtension, GUid,))

                db.commit()

                tkMessageBox.showinfo("COMP3335 - Encrypted File System","delete " + Name + "." + Extension + " successfully")

                lb.delete(lb.curselection())

                ##########

            except:
                tkMessageBox.showwarning("Warning","Please select a file.")

        def share_via_system():
            try:
                filename = lb.get(lb.curselection())
                share_form = Toplevel(my_files)
                share_form.title("Share via system")
                share_form.geometry("300x250")
                share_form.iconbitmap(ico_path)
                share_form.resizable(0, 0)

                def send_key():
                    uname = uname_receiver.get()
                    email = Email_receiver.get()
                    mail_server_passwd = mail_server_pw.get()
                    if uname != "" and email != "" and mail_server_passwd != "":
                        share_form.destroy()
                        # Function: Share via system #

                        dot = filename.rfind('.')
                        ShareFilename = filename[:dot] # name of file to be shared

                        ShareFileextension = filename[dot + 1:] # file extension of the file to be shared

                        EShareFilename = GCipherF.encrypt(padding(ShareFilename)).encode("hex") # Encrypted name of file to be shared

                        EShareFileextension = GCipherF.encrypt(padding(ShareFileextension)).encode("hex") # Encrypted name of file to be shared

                        cursor.execute ("SELECT * FROM Files WHERE Name = %s and Extension = %s and Owner = %s" , (EShareFilename, EShareFileextension, GUid,))

                        result = cursor.fetchone()

                        Fid = result[0] # file id of the file to be shared

                        old_Permission = result[5] # old Permission

                        OtherUsername = uname # id of user to whom file is shared

                        OtherEmail = email # email of user to whom file is shared

                        if OtherUsername == GUsername: # Error if the user try to share a file to himself/herself

                            tkMessageBox.showwarning("Warning","Share to the owner is forbidden.")

                        else:

                            cursor.execute ("SELECT * FROM Users WHERE Name = %s" , (OtherUsername,))

                            rc = cursor.rowcount

                            if rc == 0: # Error if no such user

                                tkMessageBox.showwarning("Warning","No such user.")

                            else:

                                # Update Permission #
                                result = cursor.fetchone()

                                OtherUid = result[0]

                                Permission =  bin(0b1 << (OtherUid - 1)) # Permission of the receiver (Nth bit from the right refer to the access control for user with Uid N (1: has access, 0: no access))

                                newPermission = bin(int(Permission, 2) | int(old_Permission, 2)) # new Permission
                                ##########

                                # Send Encryption Key to the target user via email #
                                try:
                                    sender = GEmail

                                    recipient = OtherEmail

                                    password = mail_server_passwd

                                    subject = "Encrypted File System: Decryption key for " + ShareFilename + "." + ShareFileextension + " shared by " + GUsername

                                    text = GUsername + " recently share a file to you. Decryption key for " + ShareFilename + " is " + GSF +". Please DON'T share this key to the others."

                                    message = "Subject: {}\n\n{}".format(subject, text)

                                    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)

                                    server.login(sender, password)

                                    server.sendmail(sender, recipient, message) # send the key via email

                                    cursor.execute ("UPDATE Files SET Permission = %s WHERE Fid = %s" , (newPermission, Fid,)) # update the Permission of the file

                                    db.commit()

                                    server.quit()

                                    tkMessageBox.showinfo("COMP3335 - Encrypted File System","share the key of " +  ShareFilename + "." + ShareFileextension + " to " + recipient + " successfully")

                                except smtplib.SMTPAuthenticationError:
                                    tkMessageBox.showwarning("Warning","Wrong password for email")
                                except SMTPRecipientsRefused:
                                    tkMessageBox.showwarning("Warning","Invalid email")
                                ##########

                        ##########
                    else:
                        tkMessageBox.showwarning("Warning","Please enter all the information required.")

                uname_receiver = StringVar()
                Email_receiver = StringVar()
                mail_server_pw = StringVar()

                Label(share_form, text="Username of receiver:").pack()
                e1 = Entry(share_form,textvariable=uname_receiver).pack()
                Label(share_form,text="").pack()
                Label(share_form, text="Email address of receiver:").pack()
                e2 = Entry(share_form,textvariable=Email_receiver).pack()
                Label(share_form,text="").pack()
                Label(share_form, text="Password of mail server:").pack()
                e3 = Entry(share_form,textvariable=mail_server_pw, show= '*').pack()
                Label(share_form,text="").pack()
                ok_btn = Button(share_form,text="OK", height="1", width="7", command=send_key).pack()

            except:
                tkMessageBox.showwarning("Warning","Please select a file.")

        def share_via_email():
            try:
                filename = lb.get(lb.curselection())
                share_form = Toplevel(my_files)
                share_form.title("Share via email")
                share_form.geometry("300x250")
                share_form.iconbitmap(ico_path)
                share_form.resizable(0, 0)

                def send_email():
                    uname = uname_receiver.get()
                    email = Email_receiver.get()
                    mail_server_passwd = mail_server_pw.get()
                    if uname != "" and email != "" and mail_server_passwd != "":
                        share_form.destroy()
                        # Function: Share via email #

                        dot = filename.rfind('.')
                        ShareFilename = filename[:dot] # name of file to be shared

                        ShareFileextension = filename[dot + 1:] # file extension of the file to be shared

                        EShareFilename = GCipherF.encrypt(padding(ShareFilename)).encode("hex") # Encrypted name of file to be shared

                        EShareFileextension = GCipherF.encrypt(padding(ShareFileextension)).encode("hex") # Encrypted name of file to be shared

                        cursor.execute ("SELECT * FROM Files WHERE Name = %s and Extension = %s and Owner = %s" , (EShareFilename, EShareFileextension, GUid,))

                        result = cursor.fetchone()

                        Fid = result[0] # file id of the file to be shared

                        result_Filecontent = result[3] # Encrypted file content of the file to be shared

                        ShareFilecontent = depadding(GCipherF.decrypt(result_Filecontent.decode("hex"))) # file content of the file to be shared

                        OtherUsername = uname # id of user to whom file is shared

                        OtherEmail = email # email of user to whom file is shared

                        if OtherUsername == GUsername: # Error if the user try to share a file to himself/herself

                            tkMessageBox.showwarning("Warning","Share to the owner is forbidden.")

                        else:

                            cursor.execute ("SELECT * FROM Users WHERE Name = %s" , (OtherUsername,))

                            rc = cursor.rowcount

                            if rc == 0: # Error if no such user

                                tkMessageBox.showwarning("Warning","No such user.")

                            else:

                                # Send Encryption Key to the target user via email #
                                try:
                                    sender = GEmail

                                    recipient = OtherEmail

                                    password = mail_server_passwd

                                    subject = "Encrypted File System: " + ShareFilename + "." + ShareFileextension + " shared by " + GUsername

                                    text = GUsername + " recently share a file to you.\n"

                                    message = MIMEMultipart()

                                    message.attach(MIMEText(text))

                                    message['Subject'] = subject

                                    message['To'] = recipient

                                    message['From'] = sender

                                    message.attach(MIMEApplication(ShareFilecontent, name=os.path.basename(ShareFilename + "." + ShareFileextension)))

                                    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)

                                    server.login(sender, password)

                                    server.sendmail(message['From'], message['To'], message.as_string())

                                    server.quit()

                                    tkMessageBox.showinfo("COMP3335 - Encrypted File System","share the " +  ShareFilename + "." + ShareFileextension + " to " + recipient + " successfully")
                                except smtplib.SMTPAuthenticationError:
                                    tkMessageBox.showwarning("Warning","Wrong password for email")
                                except SMTPRecipientsRefused:
                                    tkMessageBox.showwarning("Warning","Invalid email")
                                ##########

                        ##########
                    else:
                        tkMessageBox.showwarning("Warning","Please enter all the information required.")

                uname_receiver = StringVar()
                Email_receiver = StringVar()
                mail_server_pw = StringVar()

                Label(share_form, text="Username of receiver:").pack()
                e1 = Entry(share_form,textvariable=uname_receiver).pack()
                Label(share_form,text="").pack()
                Label(share_form, text="Email address of receiver:").pack()
                e2 = Entry(share_form,textvariable=Email_receiver).pack()
                Label(share_form,text="").pack()
                Label(share_form, text="Password of mail server:").pack()
                e3 = Entry(share_form,textvariable=mail_server_pw, show= '*').pack()
                Label(share_form,text="").pack()
                ok_btn = Button(share_form,text="OK", height="1", width="7", command=send_email).pack()
            except:
                tkMessageBox.showwarning("Warning","Please select a file.")

        def download():
            try:
                filename = lb.get(lb.curselection())

                destination = tkFileDialog.askdirectory()
                dot = filename.rfind('.')
                Filename_noExtension = filename[:dot] # name of file to be shared
                extension = filename[dot + 1:] # file extension of the file to be shared
                EFilename_noExtension = GCipherF.encrypt(padding(Filename_noExtension)).encode("hex")
                EExtension = GCipherF.encrypt(padding(extension)).encode("hex")

                result = cursor.execute ("SELECT * FROM Files WHERE Name = %s AND Extension = %s AND Owner = %s" , (EFilename_noExtension, EExtension, GUid,))

                result = cursor.fetchone()

                filepath = destination + '/' + Filename_noExtension + '.' + extension

                with open(filepath,"wb") as f:
                    f.write(depadding(GCipherF.decrypt(result[3].decode("hex"))))
                    f.close()

                tkMessageBox.showinfo("COMP3335 - Encrypted File System", Filename_noExtension + "." + extension + " has been downloaded in " + destination + " successfully.")
            except:
                tkMessageBox.showwarning("Warning","Please select a file.")

        def get_owned_files():
            list = cursor.execute("SELECT * FROM Files WHERE Owner = %s" , (GUid,))
            list = cursor.fetchall()
            for row in list:
                filename = depadding(GCipherF.decrypt(row[1].decode("hex")))
                extension = depadding(GCipherF.decrypt(row[2].decode("hex")))
                lb.insert(END,filename+"."+extension)

        lb=Listbox(my_files,width=56,height=20)
        lb.place(x=20,y=10)
        get_owned_files()
        upload_btn = Button(my_files,text="Upload", height="2", width="15", command=upload)
        upload_btn.place(x=370,y=30)
        delete_btn = Button(my_files,text="Delete", height="2", width="15", command=delete)
        delete_btn.place(x=370,y=80)
        share_btn1 = Button(my_files,text="Share via System", height="2", width="15", command=share_via_system)
        share_btn1.place(x=370,y=130)
        share_btn2 = Button(my_files,text="Share via Email", height="2", width="15", command=share_via_email)
        share_btn2.place(x=370,y=180)
        download_btn = Button(my_files,text="Download", height="2", width="15", command=download)
        download_btn.place(x=370,y=230)

    def shared_files_page():
        def shared_file_list():
            def download():
                try:
                    filename = lb.get(lb.curselection())
                    destination = tkFileDialog.askdirectory()
                    dot = filename.rfind('.')
                    Filename_noExtension = filename[:dot] # name of file
                    extension = filename[dot + 1:] # file extension
                    EFilename_noExtension = SCipherF.encrypt(padding(Filename_noExtension)).encode("hex")
                    EExtension = SCipherF.encrypt(padding(extension)).encode("hex")
                    result = cursor.execute("SELECT * FROM Files WHERE Name = %s AND Extension = %s \
                                            AND Owner = %s" , (EFilename_noExtension,EExtension,senderUid,))
                    result = cursor.fetchone() # get the encrypted file content
                    filepath = destination + '/' + Filename_noExtension + '.' + extension
                    with open(filepath,"wb") as f: # download the file in the designated path
                        f.write(depadding(SCipherF.decrypt(result[3].decode("hex"))))
                        f.close()
                    tkMessageBox.showinfo("COMP3335 - Encrypted File System",Filename_noExtension + '.' + extension + " has been downloaded in " + destination + " successfully.")
                except:
                        tkMessageBox.showwarning("Warning","Please select a file.")

            def remove():
                try:
                    filename = lb.get(lb.curselection())
                    dot = filename.rfind('.')
                    Filename_noExtension = filename[:dot] # name of file
                    extension = filename[dot + 1:] # file extension
                    EFilename_noExtension = SCipherF.encrypt(padding(Filename_noExtension)).encode("hex")
                    EExtension = SCipherF.encrypt(padding(extension)).encode("hex")
                    result = cursor.execute("SELECT * FROM Files WHERE Name = %s AND Extension = %s AND Owner = %s" , (EFilename_noExtension,EExtension,senderUid,))
                    result = cursor.fetchone() # get the file permission
                    permission = bin(0b1 << (GUid - 1)) # access permission of receiver
                    newPermission = bin(int(result[5],2) ^ int(permission,2)) # remove the access permission of receiver
                    cursor.execute("UPDATE Files SET Permission = %s WHERE Name = %s AND Extension = %s AND Owner = %s" , (newPermission,EFilename_noExtension,EExtension,senderUid,))
                    db.commit()
                    tkMessageBox.showinfo("COMP3335 - Encrypted File System", Filename_noExtension + "." + extension + " has been removed successfully.")
                    lb.delete(lb.curselection())
                except:
                    tkMessageBox.showwarning("Warning","Please select a file.")

            senderUsername = senderUname_info.get() # received from receiver's email and input by receiver
            senderKey = senderKey_info.get() # received from receiver's email and input by receiver
            senderUname_info.set("")
            senderKey_info.set("")
            if senderUsername == "":
                tkMessageBox.showwarning("Warning","Please enter the username of file owner.")
            elif senderUsername == GUsername:
                tkMessageBox.showwarning("Warning","You should not enter your username.")
            elif senderKey == "":
                tkMessageBox.showwarning("Warning","Please enter the decryption key of the file.")
            else:
                global SCipherF
                SCipherF = AES.new(senderKey[:32]) # for aes decryption of sender's file info used in shared_files_page
                result = cursor.execute("SELECT UID FROM Users WHERE Name = %s", (senderUsername,))
                rc = cursor.rowcount
                if rc == 0:
                    tkMessageBox.showwarning("Warning","User not found.")
                else:
                    result = cursor.fetchone()
                    global senderUid
                    senderUid = result[0]
                    global shared_files
                    shared_files = Toplevel(menu)
                    shared_files.title("Shared Files")
                    shared_files.geometry("500x350")
                    shared_files.iconbitmap(ico_path)
                    shared_files.resizable(0, 0)
                    share_file_page_form.destroy()
                    lb=Listbox(shared_files,width=56,height=20)
                    lb.place(x=20,y=10)

                    # Get the list of shared files of sender from database
                    permission = bin(0b1 << (GUid - 1)) # access permission of receiver
                    cursor.execute("SELECT * FROM Files WHERE Owner = %s", (senderUid,)) # get the list of file owned by the sender
                    list = cursor.fetchall()
                    for row in list:
                        Permissioncheck =  bin(int(permission, 2) & int(row[5], 2))
                        Permissionfail = bin(0b0)
                        if Permissioncheck != Permissionfail: # receiver has access permission to a file of the sender
                            filename = depadding(SCipherF.decrypt(row[1].decode("hex"))) # file name
                            extension = depadding(SCipherF.decrypt(row[2].decode("hex"))) # file extension
                            lb.insert(END,filename+"."+extension) # add the file to the interface
                    # Get the list of shared files of sender from database

                    remove_btn = Button(shared_files,text="Remove", height="2", width="15", command=remove)
                    remove_btn.place(x=370,y=30)
                    download_btn = Button(shared_files,text="Download", height="2", width="15", command=download)
                    download_btn.place(x=370,y=80)

        global share_file_page_form
        share_file_page_form = Toplevel(menu)
        share_file_page_form.geometry("300x200")
        share_file_page_form.title("Shared with me")
        share_file_page_form.iconbitmap(ico_path)
        share_file_page_form.resizable(0, 0)
        senderUname_info = StringVar()
        senderKey_info = StringVar()
        Label(share_file_page_form, text="Please enter the username of file owner:").pack()
        en1 = Entry(share_file_page_form,textvariable=senderUname_info).pack()
        Label(share_file_page_form,text="").pack()
        Label(share_file_page_form, text="Please enter the key of the file:").pack()
        en2 = Entry(share_file_page_form,textvariable=senderKey_info,show='*').pack()
        Label(share_file_page_form,text="").pack()
        ok_btn = Button(share_file_page_form,text="OK", height="1", width="7", command=shared_file_list).pack()


    def setting_page():
        global setting
        setting = Toplevel(menu)
        setting.title("Setting")
        setting.geometry("500x350")
        setting.iconbitmap(ico_path)
        setting.resizable(0, 0)

        def edit():
            def change_email():
                new_email = new_email_info.get()
                passwd = passwd_info.get()
                if new_email == "":
                    tkMessageBox.showwarning("Warning","Email should not be empty.")
                elif passwd == "":
                    tkMessageBox.showwarning("Warning","Please enter your password.")
                else:
                    # GUI actions
                    lb.delete(choice)
                    lb.insert(choice,new_email)
                    email_form.destroy()
                    # GUI actions

                    # FOR FUTURE DEVELOPMENT..
                    pass

            def change_uname():
                new_uname = new_uname_info.get()
                passwd = passwd_info.get()
                if new_uname == "":
                    tkMessageBox.showwarning("Warning","Username should not be empty.")
                elif passwd == "":
                    tkMessageBox.showwarning("Warning","Please enter your password.")
                else:
                    # GUI actions
                    lb.delete(choice)
                    lb.insert(choice,new_uname)
                    uname_form.destroy()
                    # GUI actions

                    # FOR FUTURE DEVELOPMENT..
                    pass

            choice = str(lb.curselection())
            quote = choice.find('\'')
            choice = int(choice[quote+1])
            if choice == 0:
                uname_form = Toplevel(setting)
                uname_form.geometry("300x150")
                uname_form.title("Change Username")
                uname_form.iconbitmap(ico_path)
                uname_form.resizable(0, 0)
                new_uname_info = StringVar()
                passwd_info = StringVar()
                Label(uname_form, text="Please enter a new Username:").pack()
                e1 = Entry(uname_form,textvariable=new_uname_info).pack()
                Label(uname_form,text="").pack()
                Label(uname_form, text="Please enter your password to confirm:").pack()
                e2 = Entry(uname_form,textvariable=passwd_info,show="*").pack()
                Label(uname_form,text="").pack()
                uname_btn = Button(uname_form,text="OK", height="1", width="7", command=change_uname).pack()

            if choice == 1:
                email_form = Toplevel(setting)
                email_form.geometry("300x150")
                email_form.title("Change Email")
                email_form.iconbitmap(ico_path)
                email_form.resizable(0, 0)
                new_email_info = StringVar()
                passwd_info = StringVar()
                Label(email_form, text="Please enter a new Email:").pack()
                e3 = Entry(email_form,textvariable=new_email_info).pack()
                Label(email_form,text="").pack()
                Label(email_form, text="Please enter your password to confirm:").pack()
                e4 = Entry(email_form,textvariable=passwd_info,show="*").pack()
                Label(email_form,text="").pack()
                email_btn = Button(email_form,text="OK", height="1", width="7", command=change_email).pack()

        lb=Listbox(setting,width=35,height=10,font=("Calibri", 11))
        lb.place(x=90,y=18)
        # for demo only
        lb.insert(1,"25scsken")
        lb.insert(2,"25scsken@example.com")
        # for demo only
        edit_btn = Button(setting,text="Edit", height="2", width="15", command=edit)
        edit_btn.place(x=360,y=20)
        username_label = Label(setting,text="Username:",width="10", height="1")
        username_label.place(x=2,y=15)
        email_label = Label(setting,text="Email:",width="10", height="1")
        email_label.place(x=2,y=35)

    Label(menu,text="Menu", bg="cyan", width="300", height="1", font=("Arial", 15)).pack()
    Button(menu,text="My files", height="2", width="20", command=my_files_page).place(x=180,y=60)
    Button(menu,text="Shared with me", height="2", width="20", command=shared_files_page).place(x=180,y=140)
    Button(menu,text="Setting", height="2", width="20", command=setting_page).place(x=180,y=220)


#Index page
def index_page():
    def marquee(widget):
        global string
        global welcome
        widget.pack_forget()
        temp = string[0]
        string = string[1:]
        string += temp
        welcome.set(string)
        widget.pack()
        widget.after(350, marquee, widget)

    global index
    global string
    global welcome
    index = Tk()
    # index.resizable(0, 0)
    index.geometry("504x300")
    l = AnimatedGIF(index, "./img/Bg.gif")
    l.place(x=0,y=0)
    string = "Welcome to COMP3335 -- Encrypted File System -- Please choose Login or Register -- "
    welcome = StringVar(index)
    welcome.set(string)
    show = Label(index,textvariable=welcome,bg="cyan",font=("Arial", 15),height=1,width=300)
    show.pack()
    index.title("COMP3335 - Encrypted File System")
    index.iconbitmap(ico_path)
    index.resizable(0, 0)
    Button(text="Login", height="2", width="20", command=login_page).place(x=180,y=90)
    Button(text="Register",height="2", width="20", command=register).place(x=180,y=160)
    marquee(show)
    winsound.PlaySound(bgm_path, winsound.SND_ASYNC | winsound.SND_LOOP)
    index.mainloop()

index_page()
