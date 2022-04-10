import sqlite3 as mysql  # sqlite3 for db connection
from tkinter import *  # tkinter library
from tkinter import messagebox as mb # messagebox from tkinter


class Account(object):
    """ Account class for accessing user personal details and 
    options to change userid,username, avatar and password"""

    def __init__(self,username):
        self.username = username

        self.db = mysql.connect('login_app.db')
        self.c = self.db.cursor()

        self.pro = Toplevel()

        self.backg = PhotoImage(file ="resources/background.png")

        self.acc_canvas = Canvas(self.pro,width=420,height=500)

        self.bg = 'Powder Blue'

        self.pencil = PhotoImage(file='resources/pencil-32.png')
        self.delete = PhotoImage(file='resources/delete-32.png')

        self.change_name_btn = Button(self.pro,image = self.pencil,bg=self.bg,bd=0,width=30,height=30,command=lambda : self.name_func('Name'),fg='white')
        self.change_uid_btn = Button(self.pro,image = self.pencil,bg=self.bg,bd=0,width=30,height=30,command=lambda : self.name_func('Username'),fg='white')
        self.change_pwd_btn = Button(self.pro,image = self.pencil,bg=self.bg,bd=0,width=30,height=30,command=lambda : self.name_func('Password'),fg='white')
        self.del_account_btn = Button(self.pro,image = self.delete,bg=self.bg,bd=0,width=30,height=30,command=self.del_func,fg='white')


    def account_screen(self):
        """Account setting options"""

        self.pro.geometry('420x450+220+170')
        self.pro.resizable(0,0)
        self.pro.title('Account Settings')
        self.pro.configure()

        self.acc_canvas.pack(fill ="both", expand =True)
        self.acc_canvas.create_image(0,0,image = self.backg,anchor ="nw")

        self.c.execute(f'select avatar from log_details where name = "{self.username}"')
        self.avar_no = self.c.fetchone()[0]
        self.avatar = PhotoImage(file=f'avatars/{self.avar_no}')
        self.av_button = Button(self.pro,image = self.avatar,bg=self.bg,width=126,height=139,bd=0,borderwidth=0,command=self.change_avatar)
        self.av_button.place(x=10,y=30)

        self.c.execute(f'select username from log_details where name = "{self.username}"')
        user = self.c.fetchone()[0]

        self.acc_canvas.create_text(280,100,text='@'+user,font=('Comic Sans MS',16,'bold'),fill='dark blue',activefill='blue')
        self.acc_canvas.create_text(280,80,text=self.username.title(),font=('Comic Sans MS',20,'bold'),fill='dark blue',activefill='blue')

        self.acc_canvas.create_text(120,230,text='Change Account Name',font=('Comic Sans MS',20,'bold'),fill='dark blue',activefill='blue')
        self.change_name_btn.place(x=280,y=220)

        self.acc_canvas.create_text(100,280,text='Change UserName',font=('Comic Sans MS',20,'bold'),fill='dark blue',activefill='blue')
        self.change_uid_btn.place(x=280,y=270)

        self.acc_canvas.create_text(95,330,text='Change Password',font=('Comic Sans MS',20,'bold'),fill='dark blue',activefill='blue')
        self.change_pwd_btn.place(x=280,y=320)

        self.acc_canvas.create_text(100,380,text='Delete Account',font=('Comic Sans MS',20,'bold'),fill='dark blue',activefill='blue')
        self.del_account_btn.place(x=280,y=370)

        self.pro.mainloop()

    def name_func(self,arg):
        """ Lambda function to change account name, userid and password"""
        name_win = Tk()

        name_win.geometry('250x200')
        name_win.title(f'Change {arg}')
        name_win.configure(bg=self.bg)
        name_win.resizable(0,0)


        Label(name_win, text=f'Change {arg}',font=('Comic Sans MS',20,'bold'),bg='powder blue',fg='dark blue').pack()
        Label(name_win, text='Enter Your Current Password',font=('Comic Sans MS',13),bg='powder blue',fg='dark blue').place(x=5,y=40)
        global cur_pass
        cur_pass = Entry(name_win,font=('Calibri Light',10,'bold'),show='*')
        cur_pass.place(x=5,y=70)

        Label(name_win, text=f'Enter {arg} You Want To Set',font=('Comic Sans MS',13),bg='powder blue',fg='dark blue').place(x=5,y=100)
        global req_pass
        req_pass = Entry(name_win,font=('Calibri Light',10,'bold'))
        req_pass.place(x=5,y=130)


        set_button = Button(name_win, text='Apply Changes',bd=0,bg='White',fg='dark blue',font=('Comic Sans MS',10,'bold'),command=lambda:self.change_info(arg))
        set_button.place(x=50,y=170)


    def change_info(self,arg):
        """ change information in database"""
        self.c.execute(f'select password from log_details where name = "{self.username}"')
        p = self.c.fetchone()[0]
        print(p)
        print(cur_pass.get(), 'done')

        if cur_pass.get() == p:
            req = req_pass.get()
            self.c.execute(f'update log_details set {arg} = "{req}" where name="{self.username}"')
            mb.showinfo('Done',f'{arg} Updated.\n Please Logout and login again to see changes.')
            self.db.commit()
            self.c.close()
        else:
            mb.showerror('Failed','Password Is Incorrect')

    def del_func(self):
        res = mb.askquestion('Confirm', 'Are You Sure That You Want To Delete Your Account.',icon='error')
        if res == 'yes':
            self.c.execute(f'delete from log_details where name = "{self.username}"')
            self.db.commit()
            self.c.close()
        self.pro.destroy()

    def change_avatar(self):
        """ Choose avatar and change it in account"""
        def set_av(no):
            """ lambda function to change avatar"""
            av_win.destroy()
            no = str(no)
            self.c.execute(f'update log_details set avatar = "{no}.png" where name="{self.username}"')
            self.db.commit()

            self.c.execute(f'select avatar from log_details where name = "{self.username}"')

            av_button = Button(self.pro, image=self.avatar,bg=self.bg,command=self.change_avatar,width=126,height=139,bd=0,borderwidth=0)
            av_button.configure(image=self.avatar)
            mb.showinfo('success','Avatar Changed. Please logout and log back again!')
            self.pro.destroy()
            self.c.close()


        av_win =Toplevel()

        av_win.geometry('560x650')
        av_win.resizable(0,0)
        av_win.title('Choose Avatar')
        av_win.configure()

        avframe=Frame(av_win,width=560,height=650)


        avframe.pack(expand=True, fill=BOTH)

        avcanvas = Canvas(avframe)

        avcanvas.pack(fill ="both", expand =True)

        avcanvas.create_image(0,0,image =self.backg,anchor ="nw")

        avcanvas.create_text(200,20,text='Choose Avatar',font=('Comic Sans MS',40,'bold'),fill='dark blue',activefill='blue')

        img_0 = PhotoImage(file='avatars/0.png')
        av_button0 = Button(av_win, image=img_0,bg=self.bg,command=lambda : set_av(0),width=126,height=139,bd=0,borderwidth=0)
        av_button0.place(x=10,y=50)

        img_1 = PhotoImage(file='avatars/1.png')
        av_button1 = Button(av_win, image=img_1,bg=self.bg,command=lambda : set_av(1),width=126,height=139,bd=0,borderwidth=0)
        av_button1.place(x=140,y=50)

        img_2 = PhotoImage(file='avatars/2.png')
        av_button2 = Button(av_win, image=img_2,bg=self.bg,command=lambda : set_av(2),width=126,height=139,bd=0,borderwidth=0)
        av_button2.place(x=270,y=50)

        img_11 = PhotoImage(file='avatars/11.png')
        av_button11 = Button(av_win, image=img_11,bg=self.bg,command=lambda : set_av(11),width=126,height=139,bd=0,borderwidth=0)
        av_button11.place(x=400,y=50)

        img_4 = PhotoImage(file='avatars/4.png')
        av_button4 = Button(av_win, image=img_4,bg=self.bg,command=lambda : set_av(4),width=126,height=139,bd=0,borderwidth=0)
        av_button4.place(x=140,y=200)

        img_5 = PhotoImage(file='avatars/5.png')
        av_button5 = Button(av_win, image=img_5,bg=self.bg,command=lambda : set_av(5),width=126,height=139,bd=0,borderwidth=0)
        av_button5.place(x=270,y=200)

        img_12 = PhotoImage(file='avatars/12.png')
        av_button12 = Button(av_win, image=img_12,bg=self.bg,command=lambda : set_av(12),width=126,height=139,bd=0,borderwidth=0)
        av_button12.place(x=400,y=200)

        img_6 = PhotoImage(file='avatars/6.png')
        av_button6 = Button(av_win, image=img_6,bg=self.bg,command=lambda : set_av(6),width=126,height=139,bd=0,borderwidth=0)
        av_button6.place(x=10,y=350)

        img_7 = PhotoImage(file='avatars/7.png')
        av_button7 = Button(av_win, image=img_7,bg=self.bg,command=lambda : set_av(7),width=126,height=139,bd=0,borderwidth=0)
        av_button7.place(x=140,y=350)

        img_8 = PhotoImage(file='avatars/8.png')
        av_button8 = Button(av_win, image=img_8,bg=self.bg,command=lambda : set_av(8),width=126,height=139,bd=0,borderwidth=0)
        av_button8.place(x=270,y=350)

        img_13 = PhotoImage(file='avatars/13.png')
        av_button13 = Button(av_win, image=img_13,bg=self.bg,command=lambda : set_av(13),width=126,height=139,bd=0,borderwidth=0)
        av_button13.place(x=400,y=350)

        img_9 = PhotoImage(file='avatars/9.png')
        av_button9 = Button(av_win, image=img_9,bg=self.bg,command=lambda : set_av(9),width=126,height=139,bd=0,borderwidth=0)
        av_button9.place(x=10,y=500)

        img_10 = PhotoImage(file='avatars/10.png')
        av_button10 = Button(av_win, image=img_10,bg=self.bg,command=lambda : set_av(10),width=126,height=139,bd=0,borderwidth=0)
        av_button10.place(x=140,y=500)

        img_14 = PhotoImage(file='avatars/14.png')
        av_button14 = Button(av_win, image=img_14,bg=self.bg,command=lambda : set_av(14),width=126,height=139,bd=0,borderwidth=0)
        av_button14.place(x=270,y=500)

        img_15 = PhotoImage(file='avatars/15.png')
        av_button15 = Button(av_win, image=img_15,bg=self.bg,command=lambda : set_av(15),width=126,height=139,bd=0,borderwidth=0)
        av_button15.place(x=400,y=500)

        av_win.mainloop()




