import _thread
from tkinter import *  # tkinter Library
import tkinter.scrolledtext as tks  # scrolledtext tkinter library
import account # To access account functions of account page
from tkinter import messagebox as mb # To print messages on pop up
import login # To redirect to login page
import socket # To establish connection with server
import json
import sqlite3 as sql # To establish connection with database
import re # To work with regex


class main_loop(object):
    """ Main loop class which send and receive messages from active users and show the
    active users in side bar
    """

    def __init__(self, username):
        self.username = username
        print("User Logged in : ", self.username)
        self.counter = 1
        # isLog.txt File
        self.file =open('isLog.txt',"w")
        # message for server dictionary
        self.message = {}
        # client
        self.client =''
        # message to write in chat box
        self.to_write = ''

        # server socket and create connection to server
        self.c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = 'localhost'
        self.port = 5000


        # sql database connection
        self.mydb = sql.connect('login_app.db')
        self.mycursor = self.mydb.cursor()

        # Tkinter design attributes
        self.win = Tk()
        self.bg = 'Powder Blue'

        # Chat Window Heading Label
        self.win_label = Label(self.win, text='', bg=self.bg, height=12, width=450, font=('arial black', 15, 'bold'),
                               relief='groove')
        self.title_label = Label(self.win, text='WETALK', bg=self.bg, fg='dark blue',
                                 font=('Comic Sans MS', 30, 'bold'))
        
        # Menu Button Image and Button
        self.menu_img = PhotoImage(file='resources/menu.png')
        self.menu_button = Button(self.win, text='Menu', image=self.menu_img, bg=self.bg, bd=0, compound='left',
                                  fg='dark blue', command=self.menu_operate_func)

        # Chat window and message Entry box
        self.chat_txt = tks.ScrolledText(self.win, height=20, width=47, font=('Cambria', 13))
        self.msg_entry = Entry(self.win, font=('Cambria', 15), width=30)

        # Message send button
        self.send_button = Button(self.win, fg='dark blue', font=('arial black', 12, 'bold'), text='Send', bg=self.bg,
                                  width=8,command =self.sendMessage)

        # Hide List Button
        self.hide_list = Button(self.win, fg='dark blue', font=('Comic Sans MS', 10, 'bold'), text='Hide User Lists',
                                bg=self.bg, width=15,command = self.hide_list_func)

        # Menu Background and user login info Background colour
        self.menu_bg = Label(self.win, text='', width=25, height=22, bg='powder blue',
                             font=('Comic Sans MS', 15, 'bold'), relief='groove')
        self.log_bg = Label(self.win, bg=self.bg, width=25, height=9, relief='groove')

        # Login info of the user after logged in
        self.login_img = PhotoImage(file='resources/login.png')
        self.log_img = Label(self.win, image=self.login_img, bg=self.bg)
        self.log_in_as = Label(self.win, text='Logged In As : ', bg=self.bg, font=('Comic Sans MS', 13), fg='dark blue')
        self.name = Label(self.win, text=self.username, bg=self.bg, font=('Comic Sans MS', 20, 'bold'), fg='dark blue')

        # Group Chat image icon and Button
        self.group_chat_img = PhotoImage(file='resources/chat-4-24.png')
        self.group_chat_btn = Button(self.win, image=self.group_chat_img, bg=self.bg, bd=0, text='           Group Chat',
                                     compound='left', fg='dark blue', font=('Comic Sans MS', 12, 'bold'),command=self.menu_operate_func)

        # User List button Image and button
        self.user_list_img = PhotoImage(file='resources/user-4-24.png')
        self.user_list_btn = Button(self.win, image=self.user_list_img, bg=self.bg, bd=0, text='           User Lists',
                                    compound='left', fg='dark blue', font=('Comic Sans MS', 12, 'bold'),command= self.user_list_func)

        # Settings image icon and Button
        self.setting_img = PhotoImage(file='resources/camera-settings-icon-white-300x300.png')
        self.setting_btn = Button(self.win, image=self.setting_img, bg=self.bg, bd=0, text='   Account Settings',
                                  compound='left', fg='dark blue', font=('Comic Sans MS', 12, 'bold'),command= self.account_func)

        # About button image icon and Button
        self.about_img = PhotoImage(file='resources/about.png')
        self.about_btn = Button(self.win, image=self.about_img, bg=self.bg, bd=0, text='                About', compound='left',
                                fg='dark blue', font=('Comic Sans MS', 12, 'bold'),command=self.about_func)

        # LogOut Button image icon and Button
        self.logout_img = PhotoImage(file='resources/logout-24.png')
        self.logout_btn = Button(self.win, image=self.logout_img, bg=self.bg, bd=0, text='              Log Out', compound='left',
                                 fg='dark blue', font=('Comic Sans MS', 12, 'bold'),command=self.logout_func)

        # User List Box of all registered users
        self.all_users_list = Label(self.win, bg='powder blue', width=14, text='All Users', fg='dark blue',
                                    font=('Comic Sans MS', 13))
        self.all_user_listbox = Listbox(self.win, width=14, height=7, font=('Cambria', 13))

        # User List Box of All active users
        self.active_user = Label(self.win, bg='powder blue', width=14, text='Active Users', fg='dark blue',
                                 font=('Comic Sans MS', 13))
        self.active_user_listbox = Listbox(self.win, width=14, height=6, font=('Cambria', 13))

    def main_screen(self):
        """ Main Chat window design"""

        print("See here:  main_screen method")

        self.win.geometry('450x487')
        self.win.resizable(0, 0)
        self.win.title('WETALK')
        self.win.configure(bg='powder blue')
        
        # Chat Window Heading Label
        self.win_label.pack()
        self.title_label.place(x=150, y=2)
        

        # Menu Button Place
        self.menu_button.place(x=8, y=7)

        # Group Chat
        self.chat_txt.place(x=10, y=50)
        self.chat_txt.yview('end')

        # message entry box and send button
        self.msg_entry.place(x=10, y=430)
        self.send_button.place(x=354, y=427)

        # Hide List Button
        self.hide_list.place(x=450, y=427)

        # All User List and Active Users List
        self.all_users_list.place(x=460, y=50)
        self.all_user_listbox.place(x=460, y=75)
        self.active_user.place(x=460, y=250)
        self.active_user_listbox.place(x=460, y=275)

        # establishing connection with server
        self.connect_with_server()
        # Add All user to active user list
        self.add_all_users_to_list()

        self.win.protocol('<WM_DELETE_WINDOW>',self.on_closing)

        # mainloop function so that window stay till
        # user click on 'X' button to
        self.win.mainloop()

    def menu_operate_func(self):
        print("See here:  menu_operate method")
        if self.counter % 2 == 0:
            self.menu_func()
            self.counter += 1
        else:
            self.home_func()
            self.counter += 1

    def menu_func(self):
        # login user background elements
        print("See here:  menu_func")
        self.log_bg.place(x=1000)
        self.log_img.place(x=1000)
        self.log_in_as.place(x=1000)
        self.name.place(x=1000)

        # Menu options
        self.menu_bg.place(x=1000)
        self.group_chat_btn.place(x=1000)
        self.user_list_btn.place(x=1000)
        self.setting_btn.place(x=1000)
        self.about_btn.place(x=1000)
        self.logout_btn.place(x=1000)

    def home_func(self):
        # login user background elements
        print("See here:  home_func")
        self.log_bg.place(x=0, y=33)
        self.log_img.place(x=50, y=50)
        self.log_in_as.place(x=40, y=120)
        self.name.place(x=35, y=145)

        # Menu options
        self.menu_bg.place(x=10, y=32)
        self.group_chat_btn.place(x=10, y=200)
        self.user_list_btn.place(x=10, y=250)
        self.setting_btn.place(x=10, y=300)
        self.about_btn.place(x=10, y=350)
        self.logout_btn.place(x=10, y=400)

    def user_list_func(self):
        """placing all user list """
        print("See here:  user_list_func")
        self.counter += 1
        self.menu_func()
        self.win.geometry('600x487')
        self.title_label.place(x=450, y=2)

    def account_func(self):
        """ account function to go to account page """
        print("See here:  account func")
        acc_inst = account.Account(self.username)
        acc_inst.account_screen()

    def about_func(self):
        """ About the aPP"""
        print("See here:  about Function")
        mb.showinfo('About',
                    '\nThis is an exclusive distribution of WETALK created By object Oriented Programming Team 2. \n'
                    '\nThis application was designed to have group and individual chats.\n'
                    ' \nThis has features like sending messages, showing all users in database, '
                    'showing all the active users, working in real-time, responsive,'
                    ' managing account settings, login, logout, register.'
                    ' \n \n Hope you like the application. '
                    '\n Please share your feedbacks.')

    def logout_func(self):
        """ log out from the account and close the window"""
        print("Log Out button pressed")
        self.to_write = 'Logged Off,'
        self.file.write(self.to_write)
        self.file.close()
        self.message={'username':self.username,'alert': 'Offline','message':'None'}
        print(self.message)
        self.c.send(str(self.message).encode('utf-8'))
        self.win.destroy()
        login.login_main()

    def hide_list_func(self):
        """ Hide list button which hide all the user and active
        user list"""
        print("hide the user list button")
        self.win.geometry('450x487')
        self.title_label.place(x=150, y=2)

    def connect_with_server(self):
        """Establishing connection with server and sending message
        to server that user logged in """
        print("See here: connect_with_server method")
        self.c.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.c.connect((self.host,self.port))
        self.message= {'username':self.username,'alert':'Online','message':'None'}
        self.c.send(str(self.message).encode('utf-8'))
        self.client = self.c
        # starting and receiving thread
        _thread.start_new_thread(self.receiving_message,(self.c, ))

    def receiving_message(self,c):
        """ Receiving the message from server """
        print("Reaching Receiving messages method")
        self.c = c
        while True:
            self.message=self.c.recv(2048).decode('utf-8')
            # print("1" + self.message)
            j= self.message.replace("'","\"")
            print("Message: " + j)
            d= json.loads(j)
            if d['alert'] == 'Online':
                self.to_write = f'                                 {d["username"]} is Online'
                print(self.to_write)
                t = self.chat_txt.get(1.0,END)
                self.chat_txt.delete(1.0,END)
                self.chat_txt.insert(INSERT,t+self.to_write+'\n')
                self.chat_txt.yview('end')
                self.list_insert(d['user_list'])
            elif d['alert'] == 'Offline':
                self.to_write = f'                                 {d["username"]} is Offline'
                print(self.to_write)
                t = self.chat_txt.get(1.0, END)
                self.chat_txt.delete(1.0, END)
                self.chat_txt.insert(INSERT, t + self.to_write+'\n')
                self.chat_txt.yview('end')
                self.list_insert(d['user_list'])

                # chat message coming from other clients
            if d['message'] != 'None':
                if d["isPrivate"] == 'true':
                    if 'receiver' in d:
                        self.to_write = f'(Direct message) Me to {d["receiver"]} :- {d["message"]}'
                    else:
                        self.to_write = f'(Direct message) {d["username"]} to Me :- {d["message"]}'
                else:
                    self.to_write = f'{d["username"]} to Everybody :- {d["message"]}'
                t = self.chat_txt.get(1.0, END)
                self.chat_txt.delete(1.0, END)
                self.chat_txt.insert(INSERT, t+ self.to_write+'\n')
                self.chat_txt.yview('end')

    def list_insert(self,list):
        """ Insert into active user list"""
        print("See here:  list_insert method")
        self.active_user_listbox.delete(0, END)
        for i in list:
            self.active_user_listbox.insert(END,i)

    def add_all_users_to_list(self):
        """" adding all users to the list"""
        print("See here:  add_all_users_to_list method")
        self.mycursor.execute(f'select name from log_details')
        p = self.mycursor.fetchall()
        for i in p:
            self.all_user_listbox.insert(END,i[0])

    def sendMessage(self,*args):
        """ Sending message to server """
        print("reached sendMessage method")
        self.message = self.msg_entry.get()
        #  Private Message format: %name% < %message%
        #  Regex used: ^.+\s<\s.+$
        match = re.search('^(.+)\s<\s(.+)$', self.message)
        self.msg_entry.delete(0, len(self.message))
        if match is None:
            self.message = str({'username':self.username,'alert':'None','message':self.message})
            print(self.message)
        else:
            self.msg_entry.insert(0, match.group(1) + ' < ')
            self.message = str({'username':self.username,'alert':'None','message':match.group(2),'receiver':match.group(1)})
        self.c.send(self.message.encode('utf-8'))

    def on_closing(self):
        """ closing the app"""
        print("See here:  on_closing method")
        res = mb.askyesnocancel('Exit','Do you want to logout and Exit?')
        if res == True:
            f =open('isLog.txt',"w")
            to_write = 'Logged Off,'
            f.write(to_write)
            f.close()
            self.win.destroy()
            msg = {'username':self.username,'alert':'Offline','message':'None'}
            self.c.send(str(msg).encode('utf-8'))

        elif res == False:
            self.win.destroy()
            msg = {'username':self.username,'alert':'Offline','message':'None'}
            self.c.send(str(msg).encode('utf-8'))


