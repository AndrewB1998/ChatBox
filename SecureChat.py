from tkinter import *
from tkinter import simpledialog
import socket
import threading




HOST = '127.0.0.1'
PORT = 1234

class Client:
    
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        
        msg = Tk()
        msg.withdraw()
        
        self.name = simpledialog.askstring("Name", "What is your name?", parent= msg)
        
        ui_thread = threading.Thread(target=self.mainUI)
        receive_thread = threading.Thread(target=self.receive)
        
        self.ui_done = False
        self.running = True
        ui_thread.start()
        receive_thread.start()
        
    def mainUI(self):
        
        self.master = Tk()
        self.master.title("Chatter")
        self.master.resizable(None, None)
        
        # Row and column configuration
        Grid.columnconfigure(self.master, 1, weight=1)
        Grid.rowconfigure(self.master, 1, weight=1)
        
        # Messages
        self.messages = []
           
        
        # Scrollbar
        self.y_bar = Scrollbar(self.master, orient=VERTICAL)
        
        # Canvas to display chat and scrollbar
        self.msg_list = Listbox(self.master, width=15, height=15, yscrollcommand=self.y_bar.set)
        self.msg_list.grid(row=1, columns=5, padx=5, pady=5, sticky="NSEW")
        self.y_bar.grid(row=1, column=5, sticky="ns")
        self.msg_list.grid_columnconfigure(0, weight=1)
        self.msg_list.grid_rowconfigure(0, weight=1)

        # Chat label, box and send button
        self.chat_label = Label(self.master, text="Type your message")
        self.chat_label.grid(row=4, columns=3, sticky="nsew")
        self.chat_box = Text(self.master, height=3)
        self.chat_box.grid(row=5, column=0, columnspan=3, sticky="ew", padx=5, pady=5)
        self.send_button = Button(self.master, text="Send", width="20", command=self.send)
        self.send_button.grid(row=5, column=4, padx=5, pady=5, sticky="NSEW")
        
        # Bind F1 to send
        self.master.bind("<Return>", self.send)
        
        #Close window and loop
        self.ui_done = True
        self.master.protocol("WM_DELETE_WINDOW", self.close)
        self.master.mainloop()
        
    def send(self, event=None):
        message = f"{self.name}: {self.chat_box.get('1.0', 'end')}"
        self.messages.append(message)
        self.sock.send(message.encode('utf-8'))
        self.chat_box.delete('1.0', 'end')
        
    def close(self):
        self.running = False
        self.master.destroy()
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
                
client = Client(HOST, PORT)       
        
