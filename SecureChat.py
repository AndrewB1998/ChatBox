from tkinter import *
from tkinter import PhotoImage

import socket
import threading
import subprocess

hostname = socket.gethostname()
HOST = socket.gethostbyname(hostname)
PORT = 1234



# Create the Tk instance
root = Tk()
root.title("Chatter")
root.resizable(False, False)
root.geometry("600x300")
class StartUI:
    def __init__(self, root):
        self.root = root
        self.frames()
        self.create_left_frame()
        self.create_right_frame()

    def frames(self):
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        self.left_frame = Frame(self.root, bg="lightblue")
        self.left_frame.grid(column=0, row=0, sticky="NSEW")
        self.left_frame.columnconfigure(0, weight=1)
        
        self.right_frame = Frame(self.root)
        self.right_frame.grid(column=1, row=0)

    def create_left_frame(self):
        self.logo_label = Label(self.left_frame, text= "ChatBox", bg="lightblue", font="Constantia 20 bold")
        self.logo_label.grid(row=0, column=0, pady=20, padx=40, sticky="NSEW")
        self.description = Label(self.left_frame, text="Host or join a chat \n Leave IP and Port empty if hosting ", bg="lightblue", font="Constantia 10")
        self.description.grid(row=1, column=0, sticky="NSEW")
    
    def create_right_frame(self):
        def raise_frame_join():
            btn_forget = [self.left_frame, self.right_frame, self.join_btn, self.host_btn, self.name_label, self.name_entry, self.save_name, self.ip_addr, self.ip_addr_entry, self.port_num, self.port_num_entry, self.port_save, self.ip_save, self.empty_row, self.logo_label]
            for btn in btn_forget:
                btn.grid_forget()
            self.client = Client(HOST, PORT, root, self.name)

        def raise_frame_host(frame):
            pass   

        def set_name():
            self.name = self.name_entry.get()
            self.join_btn.configure(text=f"Join chat as {self.name}")
            self.host_btn.configure(text=f"Host a chat as {self.name}")
            self.join_btn.configure(state=NORMAL), self.host_btn.configure(state=NORMAL)

        self.name_label = Label(self.right_frame, text="Username")
        self.name_entry = Entry(self.right_frame)
        self.save_name = Button(self.right_frame, text="Save", command=set_name, padx=5)

        self.ip_addr = Label(self.right_frame, text=f"IP: (Local:{HOST})")
        self.ip_addr_entry = Entry(self.right_frame)
        self.ip_save = Button(self.right_frame, text="Save", padx=5)

        self.port_num = Label(self.right_frame, text="Port: (Default: 1234)")
        self.port_num_entry = Entry(self.right_frame)
        self.port_save = Button(self.right_frame, text="Save", padx=5)

        self.join_btn = Button(self.right_frame, text="Join", command=lambda: raise_frame_join(), state=DISABLED, height=2)
        self.host_btn = Button(self.right_frame, text="Host", command=lambda: raise_frame_host(self.root), state=DISABLED, height=2)
        
        self.empty_row = Label(self.right_frame, text="")
        self.name_label.grid(row=0, column=0, sticky="W")
        self.name_entry.grid(row=0, column=1, padx=5)
        self.save_name.grid(row=0, column=2)
        self.ip_addr.grid(row=1, column=0, sticky="W")
        self.ip_addr_entry.grid(row=1, column=1)
        self.ip_save.grid(row=1, column=2)
        self.port_num.grid(row=2, column=0, sticky="W")
        self.port_num_entry.grid(row=2, column=1)
        self.port_save.grid(row=2, column=2)
        self.empty_row.grid(row=3)
        self.join_btn.grid(row=4, column=0, sticky="NSEW")
        self.host_btn.grid(row=4, column=1, sticky="NSEW")
        
class Client:
    def __init__(self, host, port, root, name):
        self.root = root
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        
        self.name = name
        ui_thread = threading.Thread(target=self.mainUI)
        receive_thread = threading.Thread(target=self.receive)
        
        self.ui_done = False
        self.running = True
        ui_thread.start()
        receive_thread.start()
    
    def mainUI(self):
        # Row and column configuration
        Grid.columnconfigure(self.root, 1, weight=1)
        Grid.rowconfigure(self.root, 1, weight=1)
        
        # Messages
        self.messages = []
        self.users = []   
        
        # Scrollbar
        self.y_bar = Scrollbar(self.root, orient=VERTICAL)
        
        # Listbox to display chat
        self.msg_list = Listbox(self.root, width=15, height=15, yscrollcommand=self.y_bar.set)
        self.msg_list.grid(row=1, columns=5, padx=5, pady=5, sticky="NSEW")
        self.y_bar.grid(row=1, column=5, sticky="ns")
        self.msg_list.grid_columnconfigure(0, weight=1)
        self.msg_list.grid_rowconfigure(0, weight=1)

        # Users list
        self.user_list = Listbox(self.root, width=15, height=15, yscrollcommand=self.y_bar.set)
        self.user_list.grid(row=1, column=4, padx=5, pady=5, sticky="NSEW")
        
        # Chat label, box and send button
        self.chat_label = Label(self.root, text="Type your message")
        self.chat_label.grid(row=4, columns=3, sticky="nsew")
        self.chat_box = Text(self.root, height=3)
        self.chat_box.grid(row=5, column=0, columnspan=3, sticky="ew", padx=5, pady=5)
        self.send_button = Button(self.root, text="Send", width="20", command=self.send)
        self.send_button.grid(row=5, column=4, padx=5, pady=5, sticky="NSEW")
        
        # Bind F1 to send
        self.root.bind("<Return>", self.send)
        
        #Close window and loop
        self.ui_done = True
    
    def update_users(self, names):
        self.user_list.delete(0, END)
        for name in names:
            self.users.append(name)
            self.user_list.insert(END, name)
        
    def send(self, event=None):
        message = f"{self.name}: {self.chat_box.get('1.0', 'end')}"
        self.messages.append(message)
        self.sock.send(message.encode('utf-8'))
        self.chat_box.delete('1.0', 'end')
        
    def add_users(self, names):
        self.users.extend(names)
        self.update_users(self.users)   
         
    def close(self):
        self.running = False
        self.root.destroy()
        self.sock.close()
        exit(0)
            
    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024).decode('utf-8')
                if message == "NAME":
                    self.sock.send(self.name.encode('utf-8'))
                elif message.startswith("NAMES"):
                    names = message.split()[1:]
                    print("Connected clients:", names)
                    self.update_users(names)
                    
                elif self.ui_done:
                    self.msg_list.insert(END, message)
                    
            except ConnectionAbortedError:
                break
            
            except:
                print("Error")
                self.sock.close()
                break

start = StartUI(root)
root.mainloop()