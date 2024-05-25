from enum import Enum
import tkinter as tk
from tkinter import scrolledtext
from functools import partial
from PIL import Image, ImageTk
import threading
import Controller
import sys

class BalvanChatApp:
    def __init__(self):
        self._window = tk.Tk()
        self._controller = Controller.Controller()
        self._window.resizable(False, False)

        self._menubar = tk.Menu(self._window)
        self._optionmenu = tk.Menu(self._menubar, tearoff=0)

        self._logoImage = Image.open('Images/balvanlogo.png')
        self._logoImage = self._logoImage.resize((400, 160), resample=3)
        self._logoImage = ImageTk.PhotoImage(self._logoImage, width=10)
        self._imageLabel = tk.Label(self._window, image=self._logoImage)
        self._optionmenu.add_command(label='Connect', command=self.connectCallback)
        self._optionmenu.add_command(label='Run Server', command=self.serverCallback)
        self._menubar.add_cascade(label="Start", menu=self._optionmenu)
        self._window.config(menu=self._menubar, padx=20, pady=20)
        self._window.title("Secure Messaging")
        self._text_area = scrolledtext.ScrolledText(self._window, height = 30, width = 50)
        self._text_area.configure(state='disabled', padx=10)
        self._chat_entry = tk.Entry(self._window, width = 50)
        self._send_button = tk.Button(self._window, text= "SEND", command=self.sendClicked)

        self._imageLabel.pack()
        self._text_area.pack()
        self._chat_entry.pack(side=tk.LEFT, expand=True, fill='both', pady = 10)
        self._send_button.pack(side=tk.RIGHT, padx = 5)


        self._text_area.tag_config('user', foreground='green', font=('Helvetica', '10', 'normal'))
        self._text_area.tag_config('status', foreground='red', font=('Helvetica', '10', 'bold')) 
        self._text_area.tag_config('other', foreground='black', font=('Helvetica', '10', 'normal')) 


        self._window.bind('<Return>', self.enterTapped)
        self._window.after(200, self.pollMessagesOutOfController)
        tk.mainloop()

    def pollMessagesOutOfController(self):
        if (self._controller.shouldExit):
            sys.exit(1)
        potentialTuple = self._controller.pollStatusMessage()
        if potentialTuple != None:
            self.addToTextField(potentialTuple[0], potentialTuple[1])
        self._window.after(200, self.pollMessagesOutOfController)

    def serverCallback(self):
        self.popup_server(self._controller.runServer)

    def connectCallback(self):
        self.popup_connect(self._controller.connect)

    def popup_connect(self, callback):
        
        win = tk.Toplevel(width=50, height=50, padx=10,pady=10,)
        win.wm_title("Connection Options")
        win.resizable(False, False)

        l = tk.Label(win, text='IP ADDRESS:')
        l.grid(row=0, column=0)

        ip = tk.Entry(win, width=20)
        ip.grid(row=1, column=0)

        l2 = tk.Label(win, text='NAME:')
        l2.grid(row=2, column=0)

        name = tk.Entry(win, width=20)
        name.grid(row=3, column=0)

        l3 = tk.Label(win, text='PASSWORD (SHARE WITH CLIENT):')
        l3.grid(row=4, column=0)

        password = tk.Entry(win, width=20, show='*')
        password.grid(row=5, column=0)

        l4 = tk.Label(win, text='SALT (SHARE WITH CLIENT):')
        l4.grid(row=6, column=0)

        salt = tk.Entry(win, width=20, show='*')
        salt.grid(row=7, column=0)

        def destroyCallback(input, password, name, salt):
           ipText = input.get()
           passText = password.get()
           nameText = name.get()
           saltText = salt.get()
           win.destroy()
           callback(ipText, passText, nameText, saltText)

        b = tk.Button(win, text="Connect", command=partial(destroyCallback, ip, password, name, salt))
        b.grid(row=9, column=0, pady=5)

    def popup_server(self, callback):
        
        win = tk.Toplevel(width=50, height=50, padx=10,pady=10,)
        win.wm_title("Connection Options")
        win.resizable(False, False)

        l2 = tk.Label(win, text='NAME:')
        l2.grid(row=1, column=0)

        name = tk.Entry(win, width=20)
        name.grid(row=2, column=0)

        l3 = tk.Label(win, text='PASSWORD (SHARE WITH CLIENT):')
        l3.grid(row=3, column=0)

        password = tk.Entry(win, width=20, show='*')
        password.grid(row=4, column=0)

        l4 = tk.Label(win, text='SALT (SHARE WITH CLIENT):')
        l4.grid(row=5, column=0)

        salt = tk.Entry(win, width=20, show='*')
        salt.grid(row=6, column=0)

        def destroyCallback(password, name, salt):
           passText = password.get()
           nameText = name.get()
           saltText = salt.get()
           win.destroy()
           callback(passText, nameText, saltText)

        b = tk.Button(win, text="Connect", command=partial(destroyCallback, password, name, salt))
        b.grid(row=8, column=0, pady=5)

    def addToTextField(self, text, tag):
        self._text_area.configure(state='normal')
        self._text_area.insert(tk.INSERT,'\n' + text, tag)
        self._text_area.see(tk.END)
        self._text_area.configure(state='disabled')

    def sendClicked(self):
        text = self._chat_entry.get()
        self._chat_entry.delete(0, tk.END)
        if (self._controller.isConnected):
            self._controller.send(text)
            self.addToTextField(self._controller.getName() + ':' + text, 'user')
        else:
            self.addToTextField('You are not connected.', 'status')

    def enterTapped(self, event):
        self.sendClicked()
    
    
