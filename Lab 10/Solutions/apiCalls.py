import openapi_client
from openapi_client import *
from openapi_client.models import *
from openapi_client.rest import ApiException


# region Api
# Defining the host is optional and defaults to http://127.0.0.1:5000/api
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host="http://127.0.0.1:5000/api"
)


def SignOut(login):
    with openapi_client.ApiClient() as api_client:
        # Create an instance of the API class
        api_instance = openapi_client.UsersApi(api_client)
        UserSignOut = UserSignOut1(method="SignOut")
        UserSignOut.args = {"login": login}

        post_user_sign_out = openapi_client.PostUserSignOut(UserSignOut)

        try:
            api_instance.sign_out0(post_user_sign_out)
        except ApiException as e:
            print("Exception when calling UsersApi->set_online0: %s\n" % e)


def GetUnreadMessagesInfo(recipient):
    with openapi_client.ApiClient() as api_client:
        # Create an instance of the API class
        api_instance = openapi_client.MessagesApi(api_client)
        MGM = MessageGetUnreadMessagesInfo1(method="GetUnreadMessagesInfo")
        MGM.args = {"login": recipient}
        post_message_get_unread_messages_info = openapi_client.PostMessageGetUnreadMessagesInfo(
            MGM)  # PostMessageGetUnreadMessagesInfo | GetUnreadMessagesInfo

        api_response = api_instance.get_unread_messages_info0(post_message_get_unread_messages_info)
        return api_response.meta.result.messages


def GetAllMessageBerween2Users(writerName, recipientName):
    with openapi_client.ApiClient() as api_client:
        # Create an instance of the API class
        api_instance = openapi_client.MessagesApi(api_client)
        MGM = MessageGetAllMessageBetween2Users1(method="GetAllMessageBetween2Users")
        MGM.args = {"writerUser": writerName, "recipientUser": recipientName}

        pmg = openapi_client.PostMessageGetAllMessageBetween2Users(
            MGM)

        api_response = api_instance.get_all_message_between2_users0(pmg)
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

def SetMessageStatus(messageId):
    with openapi_client.ApiClient() as api_client:
        # Create an instance of the API class
        api_instance = openapi_client.MessagesApi(api_client)
        MessageSetMessageStatus = MessageSetMessageStatus1(method="SetMessageStatus")
        MessageSetMessageStatus.args = {"idMessage": messageId, "messageStatus": "Read"}
        post_message_status = openapi_client.PostMessageSetMessageStatus(MessageSetMessageStatus)
        api_instance.set_message_status0(post_message_status)


def AuthenticationStatus(userLogin, userPassword):
    with openapi_client.ApiClient() as api_client:
        # Create an instance of the API class
        api_instance = openapi_client.UsersApi(api_client)
        UserSignIn = UserSignIn1(method="SignIn")
        UserSignIn.args = {"login": userLogin, "password": userPassword}
        post_user_sign_in = openapi_client.PostUserSignIn(UserSignIn)
        api_response = api_instance.sign_in0(post_user_sign_in)

        if api_response.meta.result.result == 'success':
            return 1
        if api_response.meta.result.result == 'online':
            return 2
        return 0


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