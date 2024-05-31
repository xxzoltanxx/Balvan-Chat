# Balvan Chat

![alt text](https://github.com/xxzoltanxx/Balvan-Chat/blob/master/Images/balvanlogo.png?raw=true)

Balvan Chat is a server/client self-hosted desktop chat application. It ensures secure communication with direct connections to the server's IP address, eliminating any middlemen. With complete end-to-end encryption (E2E) using AES512, your data remains private and secure, encrypted with a passphrase known only to the chat participants.

## Features

- Complete End-to-End Encryption: Utilizes Fernet (AES512 + DES) for robust security.
- Secure Passphrase: The password is never stored within the app; participants must agree on a passphrase via an external method, e.g., in person. The same is done for the salt.
- User-Friendly Interface: Built with Tkinter GUI for easy interaction.
- Customizable Usernames: Allows users to choose their display names.
- Multi-Client Architecture: Supports multiple clients connecting to the server.


![alt text](https://github.com/xxzoltanxx/Balvan-Chat/blob/master/screenshotchat.jpg?raw=true)

## Usage

- Connect to a Server: Choose Start -> Connect.
- Start a Server: Choose Start -> Start Server.

Note: When starting a server, your local IP address is displayed in the chat. You will need to provide your external IP address to clients, which can be found by searching "what is my IP" online.

Note: If a connection cannot be established, ensure port 15500 is open on your router.

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
python -m PyInstaller main.py --add-binary Images/balvanlogo.png:Images
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
