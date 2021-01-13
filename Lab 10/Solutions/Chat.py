import datetime
from tkinter import *
from apiCalls import *
import socketio

sio = socketio.Client()


@sio.event
def userSignIn(data):
    if data['name'] != helper.getChat().login:
        helper.getChat().UpdateOnlineUsersList()


@sio.event
def userSignOut(data):
    if data['name'] != helper.getChat().login:
        helper.getChat().UpdateOnlineUsersList()


@sio.event
def userSendMessage(msg):
    if msg['recipient_name'] == helper.getChat().login:
        if helper.getChat().selectedUser == msg['sender_name']:
            print(msg)
            msgN = InlineResponse200MetaResultMessages(
                send_time=msg['send_date'],
                text=msg['text'], writer_user=msg['sender_name'], is_read=True)
            SetMessageStatus(msg['id'])
            helper.getChat().CreateMessage(msgN, 15)
        else:
            helper.getChat().UpdateOnlineUsersList()

@sio.event
def userReadMessage(msg):
    print("userReadMessage")
    print(msg)
    if msg['writer'] == helper.getChat().login:
        if helper.getChat().selectedUser == msg['recipient']:
            helper.getChat().UpdateMessages()


class Chat:
    def __init__(self, login):
        self.root = Tk()
        self.root.title("Mini chat" + ", login:[" + login + "]")
        self.login = login
        self.root.protocol("WM_DELETE_WINDOW", self.onClosing)
        self.box = Listbox()
        self.messageHistory = Canvas()
        self.messageHistoryYOffset = 50
        self.messageEntry = StringVar()
        self.verticalScrollBar = Scrollbar()
        self.selectedUser = ""
        self.frameMessages = LabelFrame()

    def onClosing(self):
        SignOut(self.login)
        sio.disconnect()
        self.root.destroy()

    def SendMessage(self, event=None):

        SendMail(self.login, self.selectedUser, self.messageEntry.get())

        msg = InlineResponse200MetaResultMessages(send_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
                                                  text=self.messageEntry.get(), writer_user="Me")
        self.messageEntry.set("")

        self.CreateMessage(msg, 480)

    def CreateMessage(self, msg, xOffset):
        writer = msg.writer_user if msg.writer_user != self.login else "Me"
        isRead = "Read" if msg.is_read else "Unread"
        sendDate = writer + "[" + datetime.datetime.strptime(msg.send_time, '%Y-%m-%d %H:%M:%S.%f').strftime(
            "%m/%d/%Y, %H:%M:%S") + "]["+isRead+"]"
        frameMessage = LabelFrame(self.messageHistory, text=sendDate, bg="white")
        Label(frameMessage, text=msg.text, width=15, anchor='w',
              font=("comic sans ms", 8), bg="white").pack()

        self.messageHistory.create_window(xOffset, self.messageHistoryYOffset,
                                          window=frameMessage, anchor='w')

        self.messageHistoryYOffset += 40

        if self.messageHistoryYOffset > 250:
            self.messageHistory.config(scrollregion=(0, 0, 0, self.messageHistoryYOffset))

            self.messageHistory.update_idletasks()
            self.messageHistory.yview_moveto(1)

        # return frameMessage

    def UpdateMessages(self):
        self.messageHistory.delete("all")
        self.messageHistoryYOffset = 50

        messageHistoryXOffset = 15
        messages = GetAllMessageBerween2Users(self.login, self.selectedUser)
        messages.sort(key=lambda x: x.send_time)
        for msg in messages:
            helper.getChat().UpdateOnlineUsersList()
            if msg.recipient_user == self.login:
                messageHistoryXOffset = 15
            else:
                messageHistoryXOffset = 480

            self.CreateMessage(msg, messageHistoryXOffset)

        if self.messageHistoryYOffset < 250:
            self.messageHistory.config(scrollregion=(0, 0, 0, self.messageHistoryYOffset))

            self.messageHistory.update_idletasks()
            self.messageHistory.yview_moveto(0)

    def OnUserOnlineListSelect(self, event):
        widget = event.widget
        if len(widget.curselection()) == 0:
            return

        idx = int(widget.curselection()[0])
        value = widget.get(idx)

        self.selectedUser = value.split(" [")[0]
        self.frameMessages.config(text="Messages [" + self.selectedUser + "]")
        self.UpdateMessages()

    def StartGUI(self):
        sio.connect('http://127.0.0.1:5000')
        frameUsers = LabelFrame(self.root, text="Users")
        frameUsers.pack(side=LEFT, fill=BOTH)
        self.box = Listbox(frameUsers, height=19)
        self.box.pack(side="right", fill=BOTH)
        verticalScrollBarBox = Scrollbar(frameUsers, command=self.box.yview)
        verticalScrollBarBox.pack(side="left", expand=True, fill="y")
        self.box.config(yscrollcommand=verticalScrollBarBox.set)
        self.box.bind('<<ListboxSelect>>', self.OnUserOnlineListSelect)

        self.frameMessages = LabelFrame(self.root, text="Messages")
        self.frameMessages.pack(side=LEFT, fill=BOTH)
        self.messageHistory = Canvas(self.frameMessages, bg='#FFFFFF')
        self.verticalScrollBar = Scrollbar(self.messageHistory, orient=VERTICAL)
        self.verticalScrollBar.pack(side=RIGHT, fill=Y)
        self.verticalScrollBar.config(command=self.messageHistory.yview)
        self.messageHistory.config(yscrollcommand=self.verticalScrollBar.set)
        self.messageHistory.pack(side=TOP, expand=True, fill=BOTH)

        frameNewMessage = LabelFrame(self.frameMessages, text="New message")
        frameNewMessage.pack(side=BOTTOM, fill=BOTH)
        messageEntry = Entry(frameNewMessage, textvariable=self.messageEntry, width=110)
        messageEntry.bind('<Return>', self.SendMessage)
        messageEntry.pack(side="left")
        Button(frameNewMessage, text="Send", command=self.SendMessage).pack(side="left")
        frameNewMessage.pack(side="bottom", fill=BOTH)

        self.UpdateOnlineUsersList()

        self.root.mainloop()

    def UpdateOnlineUsersList(self):
        # select = list(self.box.curselection())
        # if len(select) == 0:
        #     select = [0]

        self.box.delete('0', 'end')
        unreadMessagesInfo = GetUnreadMessagesInfo(self.login)
        usersOnline = GetUsersOnline()
        for msg in unreadMessagesInfo:
            isOnline = True if len(list(filter(lambda x: x == msg.writer, usersOnline))) != 0 else False
            userInfo = msg.writer + " [" + str(msg.count) + "] "
            userInfo += "On" if isOnline else "Off"
            if self.selectedUser == msg.writer:
                userInfo = msg.writer
            self.box.insert(END, userInfo)

        for user in usersOnline:
            if user != self.login and len(list(filter(lambda x: x.writer == user, unreadMessagesInfo))) == 0:
                self.box.insert(END, user)


class Helper():
    def __init__(self):
        self.chat: Chat = None

    def setChat(self, chat):
        self.chat = chat

    def getChat(self):
        return self.chat


helper = Helper()
