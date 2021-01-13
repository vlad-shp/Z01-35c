from tkinter import *
from apiCalls import *
from Chat import Chat, helper

class Authentication:
    def __init__(self):
        self.root = Tk()
        self.root.title("Mini chat")
        self.loginVar = StringVar()
        self.passVar = StringVar()
        self.textLabel = StringVar()
        self.label1 = Label()

    def SignUp(self):
        if TryRegistration(self.loginVar.get(), self.passVar.get()):
            self.textLabel.set("[Success][Use login & password to sign in]")
            self.label1.config(fg="Green")
        else:
            self.textLabel.set("[Error][This login already exists]")
            self.label1.config(fg="Red")

    def SignIn(self):
        authenticationStatus = AuthenticationStatus(self.loginVar.get(), self.passVar.get())
        if authenticationStatus == 1:
            self.root.destroy()
            chat = Chat(self.loginVar.get())
            helper.setChat(chat)
            chat.StartGUI()


        elif authenticationStatus == 2:
            self.textLabel.set("[Error][User is online]")
            self.label1.config(fg="Red")
        else:
            self.textLabel.set("[Error][Login/password is incorrect]")
            self.label1.config(fg="Red")

    def StartGUI(self):
        canvas = Canvas(width=300, height=120)
        canvas.create_window(50, 20, window=Label(text="Login:"))
        canvas.create_window(50, 50, window=Label(text="Password:"))
        login_entry = Entry(textvariable=self.loginVar)
        canvas.create_window(150, 20, window=login_entry)
        pass_entry = Entry(textvariable=self.passVar)
        canvas.create_window(150, 50, window=pass_entry)
        canvas.create_window(120, 80, window=Button(text="Sign in", command=self.SignIn))
        canvas.create_window(180, 80, window=Button(text="Sign up", command=self.SignUp))
        self.label1 = Label(textvariable=self.textLabel)
        canvas.create_window(150, 110, window=self.label1)
        canvas.pack(side="bottom")
        self.root.mainloop()
