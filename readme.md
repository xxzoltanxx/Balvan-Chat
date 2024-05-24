# Balvan Chat

![alt text](https://github.com/xxzoltanxx/Balvan-Chat/blob/master/Images/balvanlogo.png?raw=true)

Balvan Chat is a Server/Client Self-Hosted desktop chat application.
The connection is done directly to the server's IP address, and there are no middlemen in the process of your message being sent from Client 1 to Client 2.
Additionally, Balvan Chat features complete E2E enryption using AES512, with all data being encrypted with a passphrase all participants agreed on.

## Features

- Complete End to End encryption using Fernet (AES512 + DES)
- Password is written nowhere inside the app, all participants to the chat must choose a password via some other means, e.g. somewhere IRL.
- Tkinter GUI
- Name choosing


![alt text](https://github.com/xxzoltanxx/Balvan-Chat/blob/master/screenshotchat.jpg?raw=true)

## Usage

- Connect to a server by choosing Start -> Connect
- Start a server by choosing Start -> Start Server

NOTICE: When you start a server, your LOCAL IP is listed in the chat, you will have to find out your external IP address to give to clients some other way,
e.g. by googling "what is my ip"

NOTICE: If connection is not established, you may need to open port 15500 on your router.

## Installation and Running

1) Clone the repository.
2) Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the requirements: 

```bash
pip install -r requirements.txt
```

3) Run the application with:

```bash
python main.py
```

## Packaging the application as an exe file:

1) Install PyInstaller:

```bash
pip install pyinstaller
```

2) Inside the directory where the repository is, run:

```bash
python -m PyInstaller main.py --add-binary balvanlogo.png:Images
```

3) Your exe will get packaged inside the "dist/main" folder. Now we only have to place the splash image in the appropriate place:

```bash
-Navigate to dist/_internal.
-Place the Images folder inside the folder where the .exe is
```

Now you can run the app as a standalone app.



## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)