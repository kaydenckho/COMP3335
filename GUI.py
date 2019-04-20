# -*- coding: utf-8 -*-
from Tkinter import *
import tkMessageBox
import tkFileDialog

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
    registration.geometry("500x340")
    registration.resizable(0, 0)
    registration.iconbitmap("py.ico")

    # Register button event - registration
    def register_user():
        username_info = username.get()
        password_info = password.get()
        password_confirm_info = password_confirm.get()
        email_info = email.get()

        username_entry.delete(0, END)
        password_entry.delete(0, END)
        password_confirm_entry.delete(0, END)
        email_entry.delete(0, END)

        if (username_info != "" and password_info != "" and password_confirm_info != "" and password_confirm_info == password_info):
            file = open(username_info, "w")
            file.write(username_info + "\n")
            file.write(password_info)
            file.close()
            tkMessageBox.showinfo("COMP3335 - Encrypted File System","Your account is created successfully.")
            registration.destroy()
        else:
            if username_info == "":
                Label(registration, width=30,text="You must enter an username!", fg="red", font=("calibri", 11)).place(x=140,y=290)
            elif email_info =="":
                Label(registration,width=30, text="You must enter an Email Address!", fg="red", font=("calibri", 11)).place(x=140,y=290)
            elif password_info == "":
                Label(registration,width=30, text="You must enter a password!", fg="red", font=("calibri", 11)).place(x=140,y=290)
            elif password_confirm_info == "":
                Label(registration,width=30, text="Please confirm your password!", fg="red", font=("calibri", 11)).place(x=140,y=290)
            else:
                Label(registration, width=30,text="The two passwords are different!", fg="red", font=("calibri", 11)).place(x=140,y=290)

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
    show = Label(registration, textvariable=instruction,font=("Arial", 15), bg="cyan", width="300", height="3")
    show.pack()
    marquee(show)

    username_label = Label(registration, text="Username: ")
    username_label.place(x=150,y=90)
    username_entry = Entry(registration, textvariable=username)
    username_entry.place(x=220,y=92)

    email_label = Label(registration, text="Email Address: ")
    email_label.place(x=130,y=130)
    email_entry = Entry(registration, textvariable=email)
    email_entry.place(x=220,y=132)

    password_label = Label(registration, text="Password: ")
    password_label.place(x=150,y=170)
    password_entry = Entry(registration, textvariable=password, show='*')
    password_entry.place(x=220,y=172)

    password_confirm_label = Label(registration, text="Confirm Password: ")
    password_confirm_label.place(x=110,y=210)
    password_confirm_entry = Entry(registration, textvariable=password_confirm, show='*')
    password_confirm_entry.place(x=220,y=212)

    Button(registration, text="Register", width=10, height=1, bg="Gray", command = register_user).place(x=220,y=250)

# Login page
def login_page():
    global login
    login = Toplevel(index)
    login.title("Login")
    login.geometry("500x250")
    login.resizable(0, 0)
    login.iconbitmap("py.ico")
    Label(login, text="Please enter your username and password.", bg="cyan", width="300", height="2", font=("Arial", 15)).pack()
    Label(login, text="").pack()

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
            try:
                with open(username, "r") as f:
                    uname = f.readline().rstrip("\n")
                    passwd = f.readline().rstrip("\n")
                    if (username == uname and password == passwd):
                        login.destroy()
                        menu_page()
                    else:
                        tkMessageBox.showwarning("Warning","Username or Password is incorrect.\nPlease try again.")
            except:
                tkMessageBox.showwarning("Warning","Username or Password is incorrect.\nPlease try again.")

    global username_verify
    global password_verify

    username_verify = StringVar()
    password_verify = StringVar()

    global username_login_entry
    global password_login_entry

    Label(login, text="Username : ").pack()
    username_login_entry = Entry(login, textvariable=username_verify)
    username_login_entry.pack()
    Label(login, text="").pack()
    Label(login, text="Password : ").pack()
    password_login_entry = Entry(login, textvariable=password_verify, show= '*')
    password_login_entry.pack()
    Label(login, text="").pack()
    Button(login, text="Login", width=10, height=1, command = login_verify).pack()

# Go to main menu if login success
def menu_page():
    global menu
    menu = Toplevel(index)
    menu.title("COMP3335 - Encrypted File System")
    menu.geometry("500x300")
    menu.iconbitmap("py.ico")
    menu.resizable(0, 0)

    def my_files_page():
        global my_files
        my_files = Toplevel(menu)
        my_files.title("My Files")
        my_files.geometry("500x350")
        my_files.iconbitmap("py.ico")
        my_files.resizable(0, 0)

        def upload():
            filename = tkFileDialog.askopenfile(initialdir = "/",title = "Select file")
            filename = str(filename)
            quote1 = filename.find('\'')
            quote2 = filename.find('\'',filename.find('\'')+1)
            filename = filename[quote1:quote2+1]
            lb.insert(END,filename)
            # TO BE WRITTEN...

        def delete():
            try:
                filename = lb.get(lb.curselection())
            except:
                tkMessageBox.showwarning("Warning","Please select a file.")
            lb.delete(lb.curselection())
            # TO BE WRITTEN...

        def share_via_system():
            try:
                filename = lb.get(lb.curselection())
            except:
                tkMessageBox.showwarning("Warning","Please select a file.")
            # TO BE WRITTEN...

        def share_via_email():
            try:
                filename = lb.get(lb.curselection())
                share_form = Toplevel(my_files)
                share_form.title("Share via email")
                share_form.geometry("300x230")
                share_form.iconbitmap("py.ico")
                share_form.resizable(0, 0)

                def send_email():
                    uname = uname_receiver.get()
                    email = Email_receiver.get()
                    mail_server_passwd = mail_server_pw.get()
                    print filename
                    if uname != "" and email != "" and mail_server_passwd != "":
                        share_form.destroy()
                        # TO BE WRITTEN...
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
                e3 = Entry(share_form,textvariable=mail_server_pw).pack()
                Label(share_form,text="").pack()
                ok_btn = Button(share_form,text="OK", height="1", width="7", command=send_email).pack()
            except:
                tkMessageBox.showwarning("Warning","Please select a file.")

        def download():
            try:
                filename = lb.get(lb.curselection())
            except:
                tkMessageBox.showwarning("Warning","Please select a file.")
            # TO BE WRITTEN...

        lb=Listbox(my_files,width=56,height=20)
        lb.place(x=20,y=10)
        # FOR DEMO ONLY
        lb.insert(END,"25SCSKEN.jpg")
        # FOR DEMO ONLY
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
        global shared_files
        shared_files = Toplevel(menu)
        shared_files.title("Shared Files")
        shared_files.geometry("500x350")
        shared_files.iconbitmap("py.ico")
        shared_files.resizable(0, 0)

        def get_shared_file_list():
            # TO BE WRITTEN...
            # for demo only
            lb.insert(END,"Example_shared_file.jpg")
            # for demo only

        def delete():
            try:
                filename = lb.get(lb.curselection())
            except:
                tkMessageBox.showwarning("Warning","Please select a file.")
            lb.delete(lb.curselection())
            # TO BE WRITTEN...

        def download():
            try:
                filename = lb.get(lb.curselection())
            except:
                tkMessageBox.showwarning("Warning","Please select a file.")
            # TO BE WRITTEN...

        lb=Listbox(shared_files,width=56,height=20)
        lb.place(x=20,y=10)
        get_shared_file_list()
        delete_btn = Button(shared_files,text="Delete", height="2", width="15", command=delete)
        delete_btn.place(x=370,y=30)
        download_btn = Button(shared_files,text="Download", height="2", width="15", command=download)
        download_btn.place(x=370,y=80)

    def setting_page():
        global setting
        setting = Toplevel(menu)
        setting.title("Setting")
        setting.geometry("500x350")
        setting.iconbitmap("py.ico")
        setting.resizable(0, 0)

        def edit():
            def change_email():
                cur_email = new_email.get()
                if cur_email != "":
                    lb.delete(choice)
                    lb.insert(choice,cur_email)
                    email_form.destroy()
                    # TO BE WRITTEN...
                else:
                    tkMessageBox.showwarning("Warning","Email should not be empty.")

            def change_uname():
                cur_uname = new_uname.get()
                if cur_uname != "":
                    lb.delete(choice)
                    lb.insert(choice,cur_uname)
                    uname_form.destroy()
                    # TO BE WRITTEN...
                else:
                    tkMessageBox.showwarning("Warning","Username should not be empty.")

            choice = str(lb.curselection())
            quote = choice.find('\'')
            choice = int(choice[quote+1])
            if choice == 0:
                uname_form = Toplevel(setting)
                uname_form.geometry("300x120")
                uname_form.title("Change Username")
                uname_form.iconbitmap("py.ico")
                uname_form.resizable(0, 0)
                new_uname = StringVar()
                Label(uname_form, text="Please enter a new Username:").pack()
                e1 = Entry(uname_form,textvariable=new_uname).pack()
                Label(uname_form,text="").pack()
                uname_btn = Button(uname_form,text="OK", height="1", width="7", command=change_uname).pack()

            if choice == 1:
                email_form = Toplevel(setting)
                email_form.geometry("300x120")
                email_form.title("Change Email")
                email_form.iconbitmap("py.ico")
                email_form.resizable(0, 0)
                new_email = StringVar()
                Label(email_form, text="Please enter a new Email:").pack()
                e2 = Entry(email_form,textvariable=new_email).pack()
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

    Label(menu,text="Menu", bg="cyan", width="300", height="2", font=("Arial", 15)).pack()
    Label(menu,text="").pack()
    Button(menu,text="My files", height="2", width="30", command=my_files_page).pack()
    Label(menu,text="").pack()
    Button(menu,text="Shared with me", height="2", width="30", command=shared_files_page).pack()
    Label(menu,text="").pack()
    Button(menu,text="Setting", height="2", width="30", command=setting_page).pack()


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
    index.resizable(0, 0)
    index.geometry("500x250")
    string = "Welcome to COMP3335 -- Encrypted File System -- Please choose Login or Register -- "
    welcome = StringVar(index)
    welcome.set(string)
    show = Label(index,textvariable=welcome, font=("Arial", 15),bg="cyan",height=3,width=300)
    show.pack()
    index.title("COMP3335 - Encrypted File System")
    index.iconbitmap("py.ico")
    Button(text="Login", height="2", width="30", command=login_page).place(x=135,y=90)
    Button(text="Register",height="2", width="30", command=register).place(x=135,y=160)
    marquee(show)
    Label(index, text="©Käy_COMP3335").place(x=400,y=230)

    index.mainloop()

index_page()
