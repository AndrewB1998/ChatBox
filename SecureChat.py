from tkinter import *
from tkinter import simpledialog
import socket
import threading
import subprocess

hostname = socket.gethostname()
HOST = socket.gethostbyname(hostname)
PORT = 1234

# Pitää asettaa alku UI erilliseks tost initist, eli aluks valitsee nimen, sit host tai join ja sit vasta käynnisttää servu

# Create the Tk instance
root = Tk()
root.title("Chatter")
root.resizable(None, None)

class Client:
    
    def __init__(self, host, port, root):
        self.root = root
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        
        self.name = simpledialog.askstring("Name", "What is your name?", parent=root)
        ui_thread = threading.Thread(target=self.mainUI)
        receive_thread = threading.Thread(target=self.receive)
        
        self.ui_done = False
        self.running = True
        ui_thread.start()
        receive_thread.start()
    
    def mainUI(self):
        
        def raise_frame(frame):
            frame.tkraise()
        
        self.chat_ui= Frame(root)
        self.host_join_ui = Frame(root)
        
        for frame in (self.chat_ui,self.host_join_ui):
            frame.grid(row=0, column=0, sticky='news')
        
        Button(self.host_join_ui, text='Join a chat', command=lambda:raise_frame(self.chat_ui)).grid(row=1, column=0, padx=5, pady=5, sticky="NSEW")
        Label(self.host_join_ui, text='Welcome to Chatter').grid(row=0, column=0, padx=5, pady=5, sticky="NSEW")
        
        Button(self.host_join_ui, text='Host a chat', command=lambda:raise_frame(self.chat_ui)).grid(row=3, column=0, padx=5, pady=5, sticky="NSEW")
        Label(self.host_join_ui, text='Welcome to Chatter').grid(row=4, column=0, padx=5, pady=5, sticky="NSEW")
        
        # Row and column configuration
        Grid.columnconfigure(self.chat_ui, 1, weight=1)
        Grid.rowconfigure(self.chat_ui, 1, weight=1)
        
        # Messages
        self.messages = []
        self.users = []   
        
        # Scrollbar
        self.y_bar = Scrollbar(self.chat_ui, orient=VERTICAL)
        
        # Listbox to display chat
        self.msg_list = Listbox(self.chat_ui, width=15, height=15, yscrollcommand=self.y_bar.set)
        self.msg_list.grid(row=1, columns=5, padx=5, pady=5, sticky="NSEW")
        self.y_bar.grid(row=1, column=5, sticky="ns")
        self.msg_list.grid_columnconfigure(0, weight=1)
        self.msg_list.grid_rowconfigure(0, weight=1)

        # Users list
        self.user_list = Listbox(self.chat_ui, width=15, height=15, yscrollcommand=self.y_bar.set)
        self.user_list.grid(row=1, column=4, padx=5, pady=5, sticky="NSEW")
        
        # Chat label, box and send button
        self.chat_label = Label(self.chat_ui, text="Type your message")
        self.chat_label.grid(row=4, columns=3, sticky="nsew")
        self.chat_box = Text(self.chat_ui, height=3)
        self.chat_box.grid(row=5, column=0, columnspan=3, sticky="ew", padx=5, pady=5)
        self.send_button = Button(self.chat_ui, text="Send", width="20", command=self.send)
        self.send_button.grid(row=5, column=4, padx=5, pady=5, sticky="NSEW")
        
        # Bind F1 to send
        self.root.bind("<Return>", self.send)
        
        #Close window and loop
        self.ui_done = True
    
    
    
        
    def send(self, event=None):
        message = f"{self.name}: {self.chat_box.get('1.0', 'end')}"
        self.messages.append(message)
        self.sock.send(message.encode('utf-8'))
        self.chat_box.delete('1.0', 'end')
        
    def close(self):
        self.running = False
        self.self.chat_ui.self.destroy()
        self.sock.close()
        exit(0)
            
    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024).decode('utf-8')
                if message == "NAME":
                    self.sock.send(self.name.encode('utf-8'))
                    
                elif self.ui_done:
                    self.msg_list.insert(END, message)
                    
            except ConnectionAbortedError:
                break
            
            except:
                print("Error")
                self.sock.close()
                break
                
client = Client(HOST, PORT, root)
root.protocol("WM_DELETE_WINDOW", client.close)
root.mainloop()