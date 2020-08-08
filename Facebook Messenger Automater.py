from tkinter import *
from tkinter import messagebox
from tkinter import ttk

from fbchat import *
from fbchat import *
import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from datetime import timedelta
import time
import pickle
import json
from os import path

HEIGHT = 250
WIDTH = 700

cookies = {}
try:
    # Load the session cookies
    with open('session.json', 'r') as f:
        cookies = json.load(f)
except:
    # If it fails, never mind, we'll just login again
    pass

SCOPES = ['https://www.googleapis.com/auth/calendar']


def sendMessage(groupID, finalmsg):
    print(finalmsg + "\n" + groupID)
    global client
    client.sendMessage(finalmsg, thread_id=groupID, thread_type=ThreadType.GROUP)


def infoandraise():
    initializeInformation()
    raise_frame(frameSend)


def initializeInformation():
    global username, password, calendarID
    username = fbUsername.get()
    password = fbPass.get()
    calendarID = fbcalendarID.get()

    print(username)
    print(password)
    print(calendarID)

def raise_frame(frame):
    frame.tkraise()


def calendarEvents():

    ##try:
        global client
        global username
        global password
        print(username)
        print(password)
        print(calendarID)

        client = Client(username, password) #, session_cookies=cookies)
        #with open('session.json', 'w') as f:
            #json.dump(client.getSession(), f)

        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        service = build('calendar', 'v3', credentials=creds)

        # result = service.calendarList().list().execute()
        # calendar_list_entry = service.calendarList().get(calendarId=calendarID).execute()

        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        tomorrow = datetime.datetime.utcnow() + timedelta(hours=1)
        tomorrow = tomorrow.isoformat() + 'Z'
        events_result = service.events().list(calendarId=calendarID, timeMin=now, timeMax=tomorrow,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        messagebox.showinfo('Confirmation', 'Press "OK" to send messages')

        progressBar.start(10)
        progressBar.lift()

        if not events:
            print('No upcoming events found.')
        for event in events:
            # msg = event['summary'] + "\n" + event['description']
            msg = event['description']
            groupID = msg.splitlines()[-1]
            finalmsg = "\n".join(msg.split("\n")[0:-1])

            sendMessage(groupID, finalmsg)
            time.sleep(5)
            msgBox = messagebox.showinfo('Confirmation',
                                         'Messages Sent Successfully. Press "OK" to close the program. Thank you!')
            if msgBox == 'ok':
                root.destroy()
    ##except:
       ##msgBox = messagebox.showinfo('Confirmation', 'There was an error sending messages. Contact support at '
                                            ##'maxwellkappel@gmail.com\nSorry about that! The program will now close.')
       ##if msgBox == 'ok':
            ##root.destroy()

root = Tk()
root.resizable(False, False)
root.title("FBAM")
root.iconphoto(False, PhotoImage(file='optaviaLogo.png'))
root.geometry("400x250")

frameInitialize = Frame(root)
frameInitialize.place(relwidth=1, relheight=1)
bgImage1 = PhotoImage(file='Background.png')
bgLabel1 = Label(frameInitialize, image=bgImage1)
bgLabel1.place(relwidth=1, relheight=1)

labelUser = Label(frameInitialize, text='Facebook Username/Phone#')
labelUser.grid(row=0, sticky=W, padx=5, pady=10)
labelUser.config(font=('Helvetica', 10))

labelPass = Label(frameInitialize, text='Facebook Password')
labelPass.grid(row=1, sticky=W, padx=5, pady=10)
labelPass.config(font=('Helvetica', 10))

labelCal = Label(frameInitialize, text='Calendar ID')
labelCal.grid(row=2, sticky=W, padx=5, pady=10)
labelCal.config(font=('Helvetica', 10))

fbUsername = Entry(frameInitialize, width=30)
fbUsername.grid(row=0, column=1, padx=5, pady=10)

fbPass = Entry(frameInitialize, width=30)
fbPass.grid(row=1, column=1, padx=5, pady=10)

fbcalendarID = Entry(frameInitialize, width=30)
fbcalendarID.grid(row=2, column=1, padx=5, pady=10)

initializeData = Button(frameInitialize, text='Initialize Information', command=lambda: infoandraise())
initializeData.grid(row=5, column=1, padx=5, pady=10)

frameSend = Frame(root)
frameSend.place(relwidth=1, relheight=1)
bgImage = PhotoImage(file='Background.png')
bgLabel = Label(frameSend, image=bgImage)
bgLabel.place(relwidth=1, relheight=1)

progressBar = ttk.Progressbar(frameSend, orient=HORIZONTAL, length=150, mode='indeterminate')
progressBar.place(relx=0.315, rely=0.50)
progressBar.lower()

button = Button(frameSend, text="Send today's messages", command=calendarEvents)
button.place(relx=0.33, rely=0.25, relwidth=0.35, relheight=0.12)

if (str(path.exists('credentials.json')) == 'True') and (str(path.exists(
        'session.json')) == 'True'):
    raise_frame(frameSend)
else:
    raise_frame(frameInitialize)

root.mainloop()
