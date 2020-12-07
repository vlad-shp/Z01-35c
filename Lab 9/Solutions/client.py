# region Import
from __future__ import print_function
import openapi_client
from openapi_client import ApiClient, UserSendMail1, UserSignIn1, UserRegistration1, \
    MessageGetMessagesByWriterAndRecipientUsers1, UserSetOffline1
from openapi_client.rest import ApiException
from tkinter import *

# endregion

# region Api
# Defining the host is optional and defaults to http://127.0.0.1:5000/api
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host="http://127.0.0.1:5000/api"
)


def SetOffline(login):
    with openapi_client.ApiClient() as api_client:
        # Create an instance of the API class
        api_instance = openapi_client.UsersApi(api_client)
        UserSetOffline = UserSetOffline1(method="SetOnline")
        UserSetOffline.args = {"login": login}

        post_user_set_offline = openapi_client.PostUserSetOffline(UserSetOffline)

        try:
            api_instance.set_online0(post_user_set_offline)
        except ApiException as e:
            print("Exception when calling UsersApi->set_online0: %s\n" % e)


def GetMessagesByWriterAndRecipient(writer_name, recipient_name):
    with openapi_client.ApiClient() as api_client:
        # Create an instance of the API class
        api_instance = openapi_client.MessagesApi(api_client)
        MGM = MessageGetMessagesByWriterAndRecipientUsers1(method="GetMessagesByWriterAndRecipientUsers")
        MGM.args = {"writer_user": writer_name, "recipient_user": recipient_name}

        post_message_get_messages_by_writer_and_recipient_users = openapi_client.PostMessageGetMessagesByWriterAndRecipientUsers(
            MGM)

        api_response = api_instance.get_messages_by_writer_and_recipient_users0(
            post_message_get_messages_by_writer_and_recipient_users)
        return api_response.meta.result.messages


def GetUsersOnline():
    with openapi_client.ApiClient() as api_client:
        # Create an instance of the API class
        api_instance = openapi_client.UsersApi(api_client)
        include = 'include_example'  # str | User relationships to include (csv) (optional)
    fields_user = 'login,password,isOnline'  # str | User fields to include (csv) (optional) (default to 'login,password,isOnline')
    varargs = 'varargs_example'  # str | GetUsersOnline arguments (optional)

    try:
        # GetUsersOnline
        api_response = api_instance.get_users_online0(include=include, fields_user=fields_user, varargs=varargs)
        return api_response.meta.result.users
    except ApiException as e:
        print("Exception when calling UsersApi->get_users_online0: %s\n" % e)


def TryRegistration(userLogin, userPassword):
    with openapi_client.ApiClient() as api_client:
        # Create an instance of the API class
        api_instance = openapi_client.UsersApi(api_client)
        UserRegistration = UserRegistration1(method="Registration")
        UserRegistration.args = {"login": userLogin, "password": userPassword}
        post_user_sign_in = openapi_client.PostUserRegistration(UserRegistration)

        api_response = api_instance.registration0(post_user_sign_in)

        if api_response.meta.result.result == 'success':
            return True
        return False


def AuthenticationStatus(userLogin, userPassword):
    with openapi_client.ApiClient() as api_client:
        # Create an instance of the API class
        api_instance = openapi_client.UsersApi(api_client)
        UserSignIn = UserSignIn1(method="SignIn")
        UserSignIn.args = {"login": userLogin, "password": userPassword}
        post_user_sign_in = openapi_client.PostUserSignIn(UserSignIn)
        api_response = api_instance.sign_in0(post_user_sign_in)

        if api_response.meta.result.result == 'success':
            return True
        return False


def SendMail(senderName, recipientName, messageContent):
    with openapi_client.ApiClient() as api_client:
        # Create an instance of the API class
        apiInstance = openapi_client.UsersApi(api_client)
        userSendMail = UserSendMail1(method="SendMail")
        userSendMail.args = {"sender_name": senderName, "recipient_name": recipientName,
                             "message_content": messageContent}
        post_user_send_mail = openapi_client.PostUserSendMail(userSendMail)  # PostUserSendMail |

        try:
            apiInstance.send_mail0(post_user_send_mail)
        except ApiException as e:
            print("Exception when calling UsersApi->invoke_user_send_mail0: %s\n" % e)


# endregion

# region MainFunctionality
def SendMessage():
    SendMail(loginVar.get(), friendUserVar.get(), messageContentVar.get())
    messageContentVar.set("")


def GetMessages():
    root.after(1000, GetMessages)
    if loginVar.get() == "" or friendUserVar.get() == "":
        return

    messages = GetMessagesByWriterAndRecipient(loginVar.get(), friendUserVar.get())
    messages.sort(key=lambda x: x.send_time)

    text.configure(state='normal')
    if len(messages) != 0:
        if text_first_line.get().find(
                messages[0].writer_user + " " + messages[0].text) == -1 or text_last_line.get().find(
            messages[len(messages) - 1].text + " " + messages[len(messages) - 1].send_time) == -1:
            text_first_line.set(messages[0].writer_user + " " + messages[0].text)
            text_last_line.set(messages[len(messages) - 1].text + " " + messages[len(messages) - 1].send_time)
            text.delete('1.0', END)
            for msg in messages:
                message_detail_ = f'{"me" if msg.writer_user == loginVar.get() else msg.writer_user} to {"me" if msg.recipient_user == loginVar.get() else msg.recipient_user}:{msg.text} \n'
                text.insert(END, message_detail_)
            text.yview(END)
    else:
        text.delete('1.0', END)
        text_first_line.set("")
        text_last_line.set("")
    text.configure(state='disabled')


def UpdateOnlineUsersList():
    select = list(box.curselection())
    if len(select) == 0:
        select = [0]

    box.delete('0', 'end')
    for user in GetUsersOnline():
        if user != loginVar.get():
            box.insert(END, user)

    root.after(5000, UpdateOnlineUsersList)


# endregion

# region GUI


def onUserOnlineListSelect(event):
    widget = event.widget
    if len(widget.curselection()) == 0:
        return
    idx = int(widget.curselection()[0])
    value = widget.get(idx)
    friendUserVar.set(value)


def SignIn():
    if AuthenticationStatus(loginVar.get(), passVar.get()):
        GetMessages()
        UpdateOnlineUsersList()
        root.title(f"Mini chat, login:{loginVar.get()}")
        canvas.destroy()
        text.pack(side="left")
        scroll_y = Scrollbar(f_botH, orient="vertical", command=text.yview)
        scroll_y.pack(side="left", expand=True, fill="y")
        text.configure(yscrollcommand=scroll_y.set)

        box.pack(side="right")
        scroll = Scrollbar(f_OnlineUsers, command=box.yview)
        scroll.pack(side="left", expand=True, fill="y")
        box.config(yscrollcommand=scroll.set)
        box.bind('<<ListboxSelect>>', onUserOnlineListSelect)

        f_botH.pack(side="top")
        f_bot = LabelFrame(f_History, text="Send message")
        messageEntry = Entry(f_bot, textvariable=messageContentVar, width=105)
        send_button = Button(f_bot, text="Send", command=SendMessage)
        messageEntry.pack(side="left")
        send_button.pack(side="left")
        f_bot.pack(side="bottom")
    else:
        textLabel.set("Login/password isn't correct")



def SignUp():
    if TryRegistration(loginVar.get(), passVar.get()):
        textLabel.set("Use login & password to sign in")
    else:
        textLabel.set("This login already exists")


def onClosing():
    SetOffline(loginVar.get())
    root.destroy()


root = Tk()
root.title("Mini chat")
root.protocol("WM_DELETE_WINDOW", onClosing)

f_History = LabelFrame(root, text="Chat")
f_OnlineUsers = LabelFrame(root, text="Online users")

f_History.pack(side="left")
f_OnlineUsers.pack(side="left")

f_botH = LabelFrame(f_History, text="History")
text = Text(f_botH, height=15)
box = Listbox(f_OnlineUsers, height=19)

canvas = Canvas(width=300, height=120)

friendUserVar = StringVar()

text_first_line = StringVar()
text_last_line = StringVar()
loginVar = StringVar()
passVar = StringVar()
recipientNameVar = StringVar()
messageContentVar = StringVar()
chatHistory = StringVar()

canvas.create_window(50, 20, window=Label(text="Login:"))
canvas.create_window(50, 50, window=Label(text="Password:"))
login_entry = Entry(textvariable=loginVar)
canvas.create_window(150, 20, window=login_entry)
pass_entry = Entry(textvariable=passVar)
canvas.create_window(150, 50, window=pass_entry)
canvas.create_window(120, 80, window=Button(text="Sign in", command=SignIn))
canvas.create_window(180, 80, window=Button(text="Sign up", command=SignUp))

textLabel=StringVar()
canvas.create_window(150, 110, window=Label(textvariable=textLabel))
canvas.pack(side="bottom")

root.mainloop()
# endregion
