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
root.geometry("600x400")
class StartUI:
    def __init__(self, root):
        self.root = root
        self.frames()
        self.HOST = ""
        self.PORT = ""
        self.name = ""
        
    def frames(self):
        self.root.columnconfigure(0, weight=1)

        self.root.columnconfigure(4, weight=1)
        for i in range(5):
            self.root.rowconfigure(i, weight=1)

        self.left_frame = Frame(self.root, bg="lightblue").grid(column=0, rows=5, sticky="NSEW")
        self.right_frame = Frame(self.root).grid(column=1, row=0)

        def set_name():
            self.name = self.name_entry.get()
            self.join_btn.configure(text=f"Join as {self.name}, IP: {self.HOST}, Port: {self.PORT})")
            self.host_btn.configure(text=f"Host as {self.name}, IP: {self.HOST}, Port: {self.PORT})")
            if len(self.name.strip()) > 0 and self.HOST != "" and self.PORT != "":
                self.join_btn.configure(state=NORMAL)
                self.host_btn.configure(state=NORMAL)

        def set_ip():
            self.HOST= self.ip_entry.get()
            self.join_btn.configure(text=f"Join as {self.name}, IP: {self.HOST})")
            self.host_btn.configure(text=f"Host as {self.name}, IP: {self.HOST})")
            if len(self.name.strip()) > 0 and self.HOST != "" and self.PORT != "":
                self.join_btn.configure(state=NORMAL)
                self.host_btn.configure(state=NORMAL)
            print(self.HOST)

        def set_port():
            self.PORT = int(self.port_entry.get())
            self.join_btn.configure(text=f"Join as {self.name}, IP: {self.HOST}, Port: {self.PORT})")
            self.host_btn.configure(text=f"Host as {self.name}, IP: {self.HOST}, Port: {self.PORT})")
            if len(self.name.strip()) > 0 and self.HOST != "" and self.PORT != "":
                self.join_btn.configure(state=NORMAL)
                self.host_btn.configure(state=NORMAL)

        def make_element(element,frame, text, bg, font, row, column, padx, sticky, columnspan):
            self.name = element(frame, text=text, bg=bg, font=font)
            self.name.grid(row=row, column=column, padx=padx, sticky=sticky, columnspan=columnspan)
            return self.name

        def make_button(frame, text, command, state):
            self.name = Button(frame, text=text, command=command, state=state)
            return self.name


        self.title_lbl = make_element(Label, self.left_frame, "ChatBox", "lightblue", "Constantia 20 bold", 0, 0, 40, "",1)
        self.desc_lbl = make_element(Label, self.left_frame, "Host or join a chat \n Leave IP and Port empty if hosting ", "lightblue", "Constantia 10", 2, 0, 0, "",1)
        self.name_lbl = make_element(Label, self.right_frame, "Username", "SystemButtonFace","TkDefaultFont", 0, 1, 0, "",1)
        self.ip_lbl = make_element(Label, self.right_frame, f"IP (Local:{HOST})", "SystemButtonFace", "TkDefaultFont", 1, 1, 0, "",1)
        self.port_lbl = make_element(Label, self.right_frame, "Port (Default: 1234)", "SystemButtonFace", "TkDefaultFont", 2, 1, 0, "",1)

        self.name_entry = make_element(Entry, self.right_frame, "", "White", "TkDefaultFont", 0, 2, 5, "",1)
        self.ip_entry = make_element(Entry, self.right_frame, "", "White", "TkDefaultFont", 1, 2, 5, "",1)
        self.port_entry = make_element(Entry, self.right_frame, "", "White", "TkDefaultFont", 2, 2, 5, "",1)

        self.name_btn = make_button(self.right_frame, "Save", set_name, NORMAL)
        self.ip_btn = make_button(self.right_frame, "Save", set_ip, NORMAL)
        self.port_btn = make_button(self.right_frame, "Save", set_port, NORMAL)
        self.join_btn = make_button(self.right_frame, "Join",lambda: raise_frame_join(), DISABLED)
        self.host_btn = make_button(self.right_frame, "Host",lambda: raise_frame_host(), DISABLED)

        self.name_btn.grid(row=0, column=4, padx=5, sticky="EW", columnspan=2)
        self.ip_btn.grid(row=1, column=4, padx=5, sticky="EW", columnspan=2)
        self.port_btn.grid(row=2, column=4, padx=5, sticky="EW", columnspan=2)
        self.join_btn.grid(row=3, column=1, padx=0, sticky="NSEW", columnspan=4)
        self.host_btn.grid(row=4, column=1, padx=0, sticky="NSEW", columnspan=4)


        def raise_frame_join():
            for widget in root.winfo_children():
                widget.destroy()
            self.client = Client(self.HOST, self.PORT, root, self.name)

      

        def raise_frame_host():
            subprocess.Popen(['python', 'server.py'])
            hosting_lbl = Label(self.left_frame, text=f"Server running at {self.HOST}, {self.PORT}", bg="lightblue", font="Constantia 10")
            hosting_lbl.grid(row=3, column=0, padx=40, sticky="NSEW")
            
        
        
class Client:
    def __init__(self, host, port, root, name):
        self.host = host
        self.port = port
        self.root = root
        self.name = name
        
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
                    print(f"Client {names} sent message")
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