from tkinter import *
import socket
import threading
from tkinter import simpledialog


HOST = '127.0.0.1'
PORT = 1234

class Client:
    
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        
        msg = Tk()
        msg.withdraw()
        
        self.name = simpledialog.askstring("Name", "What is your name?", parent= msg)
        ui_thread = threading.Thread(target=self.UI)
        receive_thread = threading.Thread(target=self.receive)
        
        self.ui_done = False
        self.running = True
        
        ui_thread.start()
        receive_thread.start()
        
    def UI(self):
        
        self.master = Tk()
        self.master.title("Chatter")
        self.master.resizable(None, None)
        
        # Row and column configuration
        Grid.columnconfigure(self.master, 1, weight=1)
        Grid.rowconfigure(self.master, 1, weight=1)
        
        # Messages
        self.messages = []
           
        # Canvas to display chat and scrollbar
        self.canvas = Canvas(self.master, bg="white", width=400, height=400)
        self.canvas.grid(row=1, columns=5, padx=5, pady=5, sticky="NSEW")
        self.canvas.grid_columnconfigure(0, weight=1)
        self.canvas.grid_rowconfigure(0, weight=1)
        
       # Scrollbars
        self.y_bar = Scrollbar(self.master, orient=VERTICAL, command=self.canvas.yview)
        self.y_bar.grid(row=1, column=5, sticky="ns")
        
        # Canvas configuration
        self.canvas.configure(yscrollcommand=self.y_bar.set)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.config(state='disabled')
        
        # Chat label, box and send button
        self.chat_label = Label(self.master, text="Type your message")
        self.chat_label.grid(row=4, columns=3, sticky="nsew")
        self.chat_box = Text(self.master, height=3)
        self.chat_box.grid(row=5, column=0, columnspan=3, sticky="ew", padx=5, pady=5)
        self.send_button = Button(self.master, text="Send", width="20", command=self.send)
        self.send_button.grid(row=5, column=4, padx=5, pady=5, sticky="NSEW")
        
        # Message y coordinate
        self.message_y = 2
        
        # Bind F1 to send
        self.master.bind("<F1>", self.send)
        
        
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
                    self.canvas.config(state='normal')
                    add_message = Label(self.canvas, text=message, wraplength=400, justify=LEFT, bg="white")
                    self.canvas.create_window((5, self.message_y), window=add_message, anchor="nw")
                    self.message_y += add_message.winfo_height() +10
                    self.canvas.configure(scrollregion = (0, 0, 0, self.message_y+2))
                    self.canvas.config(state='disabled')
                    
            except ConnectionAbortedError:
                break
            
            except:
                print("Error")
                self.sock.close()
                break
                
client = Client(HOST, PORT)       
        
