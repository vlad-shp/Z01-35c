# region Import
from __future__ import print_function
import openapi_client
from openapi_client import UserSendMail1
from openapi_client.rest import ApiException
from tkinter import *
# endregion

# region Api
# Defining the host is optional and defaults to http://127.0.0.1:5000/api
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host="http://127.0.0.1:5000/api"
)


def GetMessageByUserName(userName):
    with openapi_client.ApiClient() as api_client:
        # Create an instance of the API class
        api_instance = openapi_client.MessagesApi(api_client)
        include = 'include_example'  # str | Message relationships to include (csv) (optional)
        fields_message = 'writer_user,recipient_user,text,send_time'  # str | Message fields to include (csv) (optional) (default to 'writer_user,recipient_user,text,send_time')
        varargs = userName  # str | GetMessagesByUserName arguments (optional)

        api_response = api_instance.get_messages_by_user_name0(include=include, fields_message=fields_message,
                                                               varargs=varargs)
        return api_response.meta.result


def Authentication(userName):
    with openapi_client.ApiClient() as api_client:
        # Create an instance of the API class
        api_instance = openapi_client.UsersApi(api_client)
        include = 'include_example'  # str | User relationships to include (csv) (optional)
        fields_user = 'name'  # str | User fields to include (csv) (optional) (default to 'name')
        varargs = userName  # str | GetAuthenticationStatus arguments (optional)

        api_response = api_instance.get_authentication_status0(include=include, fields_user=fields_user,
                                                               varargs=varargs)
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
            apiInstance.invoke_user_send_mail0(post_user_send_mail)
        except ApiException as e:
            print("Exception when calling UsersApi->invoke_user_send_mail0: %s\n" % e)


# endregion


def SendMessage():
    SendMail(login.get(), recipientName.get(), messageContent.get())
    message_detail_ = f'me to {recipientName.get()}:{messageContent.get()} \n'
    text.insert(END, message_detail_)
    messageContent.set("")


def GetMessages():
    messages = GetMessageByUserName(login.get())
    if len(messages.id) != 0:
        for i in range(len(messages.id)):
            message_detail_ = f'{messages.writer_user[i]} to me:{messages.text[i]} \n'
            text.insert(END, message_detail_)
    root.after(1000, GetMessages)


def IsAuthenticated():
    if Authentication(login.get()):
        root.after(1000, GetMessages)
        canvas.delete("all")

        text.pack(side="left")

        scroll_y = Scrollbar(root, orient="vertical", command=text.yview)
        scroll_y.pack(side="left", expand=True, fill="y")

        text.configure(yscrollcommand=scroll_y.set)

        canvas.config(width=300, height=250)

        label6 = Label(text=f'Login:{login.get()}')
        canvas.create_window(50, 25, window=label6)

        recipientNameEntry = Entry(textvariable=recipientName)
        label = Label(text="Recipient name:")
        canvas.create_window(50, 55, window=label)
        canvas.create_window(170, 55, window=recipientNameEntry)

        label = Label(text="Message:")
        canvas.create_window(50, 85, window=label)
        messageEntry = Entry(textvariable=messageContent)
        canvas.create_window(170, 85, window=messageEntry)
        send_button = Button(text="Send", command=SendMessage)
        canvas.create_window(150, 115, window=send_button)

    else:
        label = Label(text="This user name is already taken.")
        canvas.create_window(150, 80, window=label)



root = Tk()
root.title("Mini chat")

text = Text(root, height=15)

canvas = Canvas(width=300, height=100)

login = StringVar()
recipientName = StringVar()
messageContent = StringVar()
chatHistory = StringVar()

login_entry = Entry(textvariable=login)
canvas.create_window(150, 20, window=login_entry)
search_button = Button(text="Sign in", command=IsAuthenticated)
canvas.create_window(150, 50, window=search_button)

canvas.pack(side="right")

root.mainloop()
