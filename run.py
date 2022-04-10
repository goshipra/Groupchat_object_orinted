import login # login module
import main  # main module

class WETALK:
    """Class WETALK for initiating the app"""
    def __init__(self):
        self.file = open('isLog.txt', "r")
        self.to_read = self.file.read(1024).split(',')

    def driver_method(self):
        """ If logged in already user will directly redirected to main chat
        box page else will go to login page"""

        if self.to_read[0] == 'logged in':
            print("Entered Chat Window from run.py ")
            inst = main.main_loop(self.to_read[1])
            inst.main_screen()
        else:
            print("Login Page Opened from run.py ")
            login.login_main()


# calling driver class
print("Run.py driver code")
my_app = WETALK()
my_app.driver_method()


