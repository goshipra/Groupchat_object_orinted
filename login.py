from tkinter import * # tkinter Library
from tkinter import messagebox as mb # messagebox from tkinter
import sqlite3 as sql # sqlite3 library
import main # main module


class Login:
    """Login Class to show up the login page"""

    def __init__(self,reg):
        try:
            reg.destroy()
        except Exception as e:
            pass

        self.log = Tk()
        self.username =''
        self.canvas1 = Canvas(self.log, width=420, height=450)
        self.user_entry = Entry(self.log, font=('Arial Black', 15, 'bold'), width=25, bg='white')
        self.bg = PhotoImage(file="resources/background.png")
        self.pass_entry = Entry(self.log, show='*', font=('Arial Black', 15, 'bold'), width=25, bg='white')
        self.resp = Label(self.log, text='', font=('Arial Black', 10, 'bold'), bg='powder blue')
        self.submit = Button(self.log, text='Log-in', font=('Comic Sans MS', 15, 'bold'), width=14, bd=0, fg='indigo',command=self.log_func)
        self.reg_button = Button(self.log, text='Register', font=('', 10, 'underline', 'italic'), bg='powder blue',
                            command = self.btn_reg_pressed,fg='blue')

    def btn_reg_pressed(self):
        print("btn_reg_pressed ")
        register_cls = Register(self.log)
        register_cls.register_screen()


    def log_func(self,*args):
        print("log_func  ")

        data_base = sql.connect('login_app.db')
        c = data_base.cursor()

        self.username = self.user_entry.get()
        password = self.pass_entry.get()

        try:
            c.execute(f'select Password from LOG_DETAILS where Username = "{self.username}" ')

            b = c.fetchall()

            for i in b:
                passw = i[0]

                if password == passw:
                    c.execute(f'select name from LOG_DETAILS where Username= "{self.username}"')
                    b = c.fetchall()[0][0]
                    username_name = b
                    self.resp.configure(text=f'Login Successful\n Welcome {b} ', fg='green')
                    self.log.destroy()
                    f = open('isLog.txt','w')
                    to_write = 'logged in,'+b
                    f.write(to_write)
                    f.close()
                    print("Entering Main Chat Window from login.py log_func")
                    self.calling_main_loop(b)

                else:
                    self.resp.configure(text='Wrong Password', fg='red')

        except Exception as e:
            print("")
        self.resp.configure(text=f'Username {self.username} Does Not Exist', fg='red')

    def calling_main_loop(self,username):
        print("calling main loop :  method ")
        inst = main.main_loop(username)
        inst.main_screen()


    def login_screen(self):
        # Login Tkinter
        print("Entered Login Screen method")
        self.log.title('Login Page')
        self.log.geometry('420x450+220+170')
        self.log.configure(bg='powder blue')
        self.log.resizable(0, 0)

        # Canvas for Login Page
        self.canvas1.pack(fill="both", expand=True)
        self.canvas1.create_image(0, 0, image=self.bg, anchor="nw")

        # Creating labels
        self.canvas1.create_text(200, 40, text="WETALK", font=('Comic Sans MS', 40, 'bold'), fill='dark blue',
                            activefill='blue')

        # Username Label
        self.canvas1.create_text(80, 100, text='UserName', font=('Comic Sans MS', 20, 'bold'), fill='dark blue',
                            activefill='blue')

        # User Entry Field for Username and place in the login window
        self.user_entry.place(x=30, y=120)

        # User Password Label
        self.canvas1.create_text(80, 180, text='Password ', font=('Comic Sans MS', 20, 'bold'), fill='dark blue',
                            activefill='blue')

        # User Password for Username and place in the login window
        self.pass_entry.place(x=30, y=200)

        # Response for error and other message and its place
        self.resp.place(x=30, y=300)

        # Submit the Login Details Button and its place
        self.submit.place(x=40, y=265)

        # Canvas Text for Register window
        self.canvas1.create_text(160, 360, text='Click On Register If You Don\'t Have An Account.',
                            font=('Comic Sans MS', 9, 'italic'), fill='dark blue', activefill='blue')

        # Button for Register window
        self.reg_button.place(x=60, y=370)

        # self.log.bind('<Return>', self.log_func)

        # Login page Mainloop
        self.log.mainloop()


class Register:
    """Register class shows the Registration Page Window"""

    # Destroying the register window
    def __init__(self,log):
        try:
            log.destroy()
        except Exception as e:
            pass


        self.reg = Tk()

        # Initiating  Global reg window Variable and Tkinter Widgets

        self.canvas2 = Canvas(self.reg, width=420, height=450)
        self.name_entry = Entry(self.reg, font=('Arial Black', 15, 'bold'), width=25, bg='white')
        self.user_entry = Entry(self.reg, font=('Arial Black', 15, 'bold'), width=25, bg='white')
        self.bg = PhotoImage(file="resources/background.png")
        self.pass_entry = Entry(self.reg, show='*', font=('Arial Black', 15, 'bold'), width=25, bg='white')
        self.submit = Button(self.reg, text='Register', font=('Comic Sans MS', 15, 'bold'), width=14, bg='powder blue', bd=0,
                        command=self.reg_func,fg='indigo')
        self.log_button = Button(self.reg, text='Log_In', font=('', 10, 'underline', 'italic'), bg='powder blue', fg='blue',
                            command=self.btn_log_pressed)
        self.username = ''

    def btn_log_pressed(self):
        print("btn_log_pressed ")
        """ create instance of Login class and pass reg window as argument
        then calling login screen window
        """
        login_cls = Login(self.reg)
        login_cls.login_screen()


    def reg_func(self,*args):
        """ registering user after taking details from new user"""
        print("reg_func ")
        data_base = sql.connect('login_app.db')
        c = data_base.cursor()

        name = self.name_entry.get().title()
        user = self.user_entry.get()
        password = self.pass_entry.get()

        if name != '' and user != '' and password != '':

            c.execute('select Username from LOG_DETAILS')

            l = c.fetchall()
            ex_t = False
            for i in l:
                if user == i[0]:
                    ex_t = True
                    break
                else:
                    ex_t = False

            if ex_t == True:
                mb.showerror('Register',f'{user} Already Exist.')
            else:
                c.execute(f'insert into LOG_DETAILS values("{name}","{user}","{password}","0.png")')
                data_base.commit()
                self.name_entry.delete(0, END)
                self.user_entry.delete(0, END)
                self.pass_entry.delete(0, END)
                self.username_name = name
                self.reg.destroy()
                f = open('isLog.txt','w')
                to_write = 'logged in,'+self.username_name
                f.write(to_write)
                f.close()
                print("Entering Main Chat Window after registration")
                inst2 = main.main_loop(self.username_name)
                inst2.main_screen()
        else:
            mb.showerror('Register','Please Fill All The Fields.')



    def register_screen(self):
        """ Register window """
        print("Entered Register Screen")
        self.reg.title('Register Page')
        self.reg.configure(bg='powder blue')
        self.reg.geometry('420x450+220+170')
        self.reg.resizable(0, 0)

        # Register Canvas
        self.canvas2.pack(fill="both", expand=True)
        self.canvas2.create_image(0, 0, image=self.bg, anchor="nw")

        # Creating labels
        self.canvas2.create_text(200, 40, text="WETALK", font=('Comic Sans MS', 40, 'bold'), fill='dark blue',
                            activefill='blue')

        # Fullname Label
        self.canvas2.create_text(90, 100, text='Full Name ', font=('Comic Sans MS', 20, 'bold'), fill='dark blue',
                            activefill='blue')

        # Fullname Entry and its place in Register Window
        self.name_entry.place(x=40, y=120)

        # Username Label
        self.canvas2.create_text(90, 180, text='UserName', font=('Comic Sans MS', 20, 'bold'), fill='dark blue',
                            activefill='blue')

        # Username Entry and its place in Register Window
        self.user_entry.place(x=40, y=200)

        # New Password Label
        self.canvas2.create_text(110, 260, text='New Password', font=('Comic Sans MS', 20, 'bold'), fill='dark blue',
                            activefill='blue')

        # New Password Entry
        self.pass_entry.place(x=40, y=280)

        # Submit button to Register user in Database and its place
        self.submit.place(x=40, y=335)

        # Already Have An Account text
        self.canvas2.create_text(110, 380, text='Already Have An Account.', font=('Comic Sans MS', 9, 'italic'),
                            fill='dark blue', activefill='blue')

        # Log_In Button to redirect on Login Class
        self.log_button.place(x=60, y=390)

        # self.reg.bind('<Return>',self.reg_func())

        # Main Loop of register Page
        self.reg.mainloop()

def login_main():
    """Main function called from run page"""
    print("login_main driver method ")
    inst = Login(None)
    inst.login_screen()
