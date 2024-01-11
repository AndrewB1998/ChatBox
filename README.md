# CipherChat (Programming course TKO_3123)
Cipherchat is a chat application that uses Fernet's symmetric-key algorithm for protection 
and utilizes Python's tkinter GUI toolkit, sockets and threading. Host a chat using your local IP-address or join an existing server

# Overview
![cipherchat chat interface](https://github.com/AndrewB1998/CipherChat/assets/71883814/e0f6d937-5ae3-4268-92e6-22d973d1b9a7)
When hosting a server, the StartUI class starts a subprocess call (subprocess.Popen(['python', 'Server.py'])) to the server.py file containing the server functionality. The server receives encrypted messages which are forwarded to all users and, upon connection, the server sends the encryption key it has generated to the connecting client.. The server can be closed with “terminate()” command, which is given as a function of the "Close server" button. The “Join a server” button activates the command “self.client = Client(self.HOST, self.PORT, root, self.name)”, which starts execution of the Client class and attempts to connect to the server with the given parameters

![cipherchat main view](https://github.com/AndrewB1998/CipherChat/assets/71883814/d3305103-94b8-4207-be7c-5c94d32e5f9c)
Chat interface. The “encrypt” button activates encrypted mode (displays messages in encrypted form, hides the participant list and locks the chat) and the decrypt button restores previous messages. While this changes the UI, the sent messages are always encrypted (tested on WireShark's packet capture feature). The “Save chat” button saves the elements of the conversation (Listbox) to the desired location as a text file using Tkinter’s filedialog- function.
<br/>
# Requirements
- Python 3.0 or above (you can check the version with terminal command *python --version* and if necessary, install python from https://www.python.org/downloads/)
- Cryptography library

# Installation
- Clone this repository or download the ZIP file and extract its contents to a directory.
- Open a terminal and navigate to the directory where the files are located.
- Install cryptography with terminal command *pip install cryptography*
- Run the following command to start the application: *python CipherChat.py*

# Usage
- In the start window, enter a username, the IP-address and port of an existing server to join, or your local IP-address to host.
- You can also host a server by running the server.py file 
- Click the "Join" button to connect to an existing server, or click the "Host" button to start a new server and wait for other clients to connect.
- Once connected, you can start chatting with other clients on the server.
- To save the chat, click save and choose a directory of your choice
- You can use the "Encrypt" button to transfrom the already received messages to ciphertext

# Troubleshoot
- Make sure that the required installations are done in the project directory
- If python is installed, but pip commands don't work, run terminal command *py -m ensurepip --upgrade* or *py get-pip.py*
- Tkinter comes along with Python but incase there is issues, use terminal command *pip install tk*
