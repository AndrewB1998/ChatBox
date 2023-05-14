# CipherChat (Programming course TKO_3123)
Cipherchat is a chat application that uses Fernet's symmetric-key algorithm for protection 
and utilizes Python's tkinter GUI toolkit, sockets and threading.

# Requirements
- Python 3.0 or above (you can check the version with terminal command *python --version* and if necessary, install python from https://www.python.org/downloads/)
- Cryptography library

# Installation
- Clone this repository or download the ZIP file and extract its contents to a directory.
- Open a terminal and navigate to the directory where the files are located.
- Install cryptography with terminal command *pip install cryptography*
- Run the following command to start the application: python CipherChat.py

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
- Tkinter comes along with Python but incase there is issues, use terminal command *pip install tk
- The client closes if a connection can't be made. Make sure that VPN is off when connecting and that there is a server running when joining
