from tkinter import *
from tkinter import filedialog
import socket
import threading
import subprocess
from cryptography.fernet import Fernet


hostname = socket.gethostname()
HOST = socket.gethostbyname(hostname)
PORT = 1234

# Create the Tk instance
root = Tk()
root.title("Chatter")
root.geometry("400x300")
root.minsize(600, 400)
def make_element(element,frame, text=None, bg=None, font=None, row=None, column=None, state=None, padx=None, pady=None, sticky=None, columnspan=None, rows=None, command=None, height=None, width=None, yscrollcommand=None):
        elem = element(frame, text=text, bg=bg, font=font, command=command, state=state, height=height, width=width, yscrollcommand=yscrollcommand)
        elem.grid(row=row, column=column, padx=padx, pady=pady, sticky=sticky, columnspan=columnspan, rows=rows)
        return elem

def make_button(frame, text, command, state):
        return Button(frame, text=text, command=command, state=state)
class StartUI:
    def __init__(self, root):
        self.root = root
        self.root.protocol("WM_DELETE_WINDOW", root.destroy)
        self.frames()
        self.HOST = ""
        self.PORT = ""
        self.name = ""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def frames(self):
        # Column and row configurations
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(2, weight=1)
        self.root.columnconfigure(4, weight=1)
        for i in range(5):
            self.root.rowconfigure(i, weight=1)
            
        # Split main window into two frames
        self.left_frame = Frame(self.root, bg="lightblue").grid(column=0, rows=5, sticky="NSEW")
        self.right_frame = Frame(self.root).grid(column=1, row=0)
        
        # Set name, IP and port and check if all the values are set -> join or host
        def set_name():
            self.name = self.name_entry.get()
            check_set()

        def set_ip():
            self.HOST= self.ip_entry.get()
            check_set()

        def set_port():
            self.PORT = int(self.port_entry.get())
            check_set()
        
        def check_set():
            self.join_btn.configure(text=f"Join as {self.name}, IP: {self.HOST}, Port: {self.PORT}")
            self.host_btn.configure(text=f"Host as {self.name}, IP: {self.HOST}, Port: {self.PORT}")
            if len(self.name.strip()) > 0 and self.HOST != "" and self.PORT != "":  
                self.join_btn.configure(state=NORMAL)
                self.host_btn.configure(state=NORMAL)
                
        # Deletes the elements and connects to server -> class Client 
        def raise_frame_join():
            for widget in root.winfo_children():
                widget.destroy()
            self.client = Client(self.HOST, self.PORT, root, self.name)
            
        # Starts the server.py as a subprocess
        def raise_frame_host():
            subprocess.Popen(['python', 'Server.py'])
            self.hosting_lbl = Label(self.left_frame, text=f"Server running at {self.HOST}, {self.PORT}", bg="lightblue", font="Constantia 10")
            try:
                self.sock.connect((self.HOST, self.PORT))
                self.hosting_lbl.grid(row=3, column=0, padx=40, sticky="NSEW")  
                self.join_btn.configure(text= "Open a new instance to join", state=DISABLED)
                self.host_btn.configure(text= "Close server", command=close_server)
            except:
                self.hosting_lbl.configure(text="Server failed to start")
                
        def close_server():
            subprocess.Popen(['python', 'Server.py']).terminate()
            for widget in root.winfo_children():
                widget.destroy()
            self.root.configure(bg='light blue')
            self.thankyou_label = make_element(Label, self.root, text="Thank you!", font="Constantia 30 bold", bg="lightblue", row=0, column=0, columnspan=5, padx=40, pady=40, sticky="NSEW")
            self.exit_btn = make_element(Button, self.root, text="Exit", font="Constantia 10", bg="lightblue", command=lambda: root.destroy(), row=1, column=0, columnspan=5, rows=2, padx=40, pady=40, sticky="NSEW")
        
        # Create elements and set them to the grid 
        self.title_lbl = make_element(Label, self.left_frame, text="ChatBox", bg="lightblue", font="Constantia 25 bold", row=1, column=0, padx=40)
        self.desc_lbl = make_element(Label, self.left_frame, text="Host or join a chat \n Leave IP and Port empty if hosting", bg="lightblue", font="Constantia 10", row=2, column=0, columnspan=1)

        self.name_lbl = make_element(Label, self.right_frame, text="Username", bg="SystemButtonFace", font="TkDefaultFont", row=0, column=1, columnspan=1)
        self.ip_lbl = make_element(Label, self.right_frame, text=f"IP (Local:{HOST})", bg="SystemButtonFace", font="TkDefaultFont", row=1, column=1, columnspan=1)
        self.port_lbl = make_element(Label, self.right_frame, text="Port (Default: 1234)", bg="SystemButtonFace", font="TkDefaultFont", row=2, column=1, columnspan=1)

        self.name_entry = make_element(Entry, self.right_frame, text="", bg="White", font="TkDefaultFont", sticky="EW", row=0, column=2, padx=5, columnspan=1)
        self.ip_entry = make_element(Entry, self.right_frame, text="", bg="White", font="TkDefaultFont", sticky="EW", row=1, column=2, padx=5, columnspan=1)
        self.port_entry = make_element(Entry, self.right_frame, text="", bg="White", font="TkDefaultFont", sticky="EW", row=2, column=2, padx=5, columnspan=1)

        self.name_btn = make_element(Button, self.right_frame, text="Save", command=set_name, sticky="EW", state=NORMAL, row=0, column=4, padx=5, columnspan=2)
        self.ip_btn = make_element(Button, self.right_frame, text="Save", command=set_ip, sticky="EW", state=NORMAL, row=1, column=4, padx=5, columnspan=2)
        self.port_btn = make_element(Button, self.right_frame, text="Save", command=set_port, sticky="EW", state=NORMAL, row=2, column=4, padx=5, columnspan=2)
        self.join_btn = make_element(Button, self.right_frame, text="Join a server", command=lambda: raise_frame_join(), sticky="NSEW", state=DISABLED, row=3, column=1, padx=0, columnspan=4)
        self.host_btn = make_element(Button, self.right_frame, text="Host a server", command=lambda: raise_frame_host(), sticky="NSEW", state=DISABLED, row=4, column=1, padx=0, columnspan=4)        
class Client:
    def __init__(self, host, port, root, name):
        self.host = host
        self.port = port
        self.root = root
        
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.fernet = None
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        self.name = name
        self.enc_mode = False
        ui_thread = threading.Thread(target=self.mainUI)
        receive_thread = threading.Thread(target=self.receive)
        self.key_received = False
        self.name_received = False
        
        self.running = True
        ui_thread.start()
        receive_thread.start()

    def mainUI(self):
        self.users = []   
        self.messages = []
        self.enc_messages = []
        self.root.bind("<Return>", self.send)
        
        root.configure(bg="lightblue")
        
        # Reset previous row and column configurations and set
        for i in range(5):
            self.root.rowconfigure(i, weight=0)
            self.root.columnconfigure(i, weight=0)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
       
        # Make chat elements
        self.y_bar = Scrollbar(self.root, orient=VERTICAL)
        self.msg_list = make_element(Listbox, self.root, width=15, height=15, yscrollcommand=self.y_bar.set, row=1, column=0, columnspan=5, padx=5, pady=5, sticky="NSEW")
        self.msg_lbl = make_element(Label, self.root, text="Messages", bg="lightblue", row=0, column=0, sticky="NS")
        self.user_list = make_element(Listbox, self.root, width=15, height=15, row=1, column=4, padx=10, pady=5, sticky="NSEW")
        self.users_lbl = make_element(Label, self.root, text="Participants", bg="lightblue", row=0, column=4, sticky="NSEW")
        self.chat_lbl = make_element(Label, self.root, text="Type your message", bg="lightblue", row=4, column=0, sticky="NS")
        self.chat_txt = make_element(Text, self.root, height=3, row=5, column=0, columnspan=3, sticky="ew", padx=5, pady=5)
        self.send_btn = make_element(Button, self.root, text="Send", width="20", bg="lightblue", command=self.send, row=5, column=4, padx=5, pady=5, sticky="NSEW")       
        self.enc_btn = make_element(Button, self.root, text="Encrypt", bg="lightblue", width="20", command=self.encrypt, row=4, column=1, padx=5, pady=5, sticky="NSEW")
        self.save_chat_btn = make_element(Button, self.root, text="Save chat", bg="lightblue", width="20", command=self.save_chat, row=4, column=4, padx=5, pady=5, sticky="E")
        self.y_bar.config(command=self.msg_list.yview)
        self.y_bar.grid(row=0, column=5, rowspan=6, sticky="NS")
        
    def encrypt(self):
        self.msg_list.delete(0, END)
        self.user_list.delete(0, END)
        for message in self.enc_messages:
            self.msg_list.insert(END, message)
        
        self.enc_mode = True
        self.enc_btn.config(text="Decrypt", command=self.decrypt)
        self.send_btn.config(text= "Decrypt to chat",state=DISABLED)
        
    def decrypt(self):
        self.msg_list.delete(0, END)
        self.user_list.delete(0, END)
        for message in self.messages:
            self.msg_list.insert(END, message)
        
        for user in self.users:
            if user not in self.users:
                self.user_list.insert(END, user)
            
        self.enc_mode = False
        self.enc_btn.config(text="Encrypt", command=self.encrypt)
        self.send_btn.config(text="Send", state=NORMAL)
        
    def save_chat(self):
        for i in range(self.msg_list.size()):
            self.messages.append(self.msg_list.get(i))
        if file_path := filedialog.asksaveasfilename(defaultextension=".txt"):
                with open(file_path, "w") as f:
                    f.write("\n".join(self.messages))
        chat_save =  f"{self.name} saved chat!"
        print(self.msg_list)
        self.msg_list.insert(END, chat_save)   
     
    # Update the users window    
    def update_users(self, name):
        self.user_list.delete(0, END)
        for i in name:
            self.user_list.insert(END, i)
            self.users.append(i)
            
    # Send message to server and delete the text box    
    def send(self, event=None):
        message = f"{self.name}: {self.chat_txt.get('1.0', 'end')}"
        enc_message = self.fernet.encrypt(message.encode('utf-8')) 
        self.sock.send(enc_message)
        self.chat_txt.delete('1.0', 'end') 
         
    def close(self):
        self.running = False
        print(f"Client {self.name} left")
        self.sock.close()
        self.root.destroy()
        exit(0)
            
    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024)
                try:
                    if not self.key_received:
                        message.decode()
                        key = message.split()[1][2:-1]
                        self.fernet = Fernet(key)
                        self.key_received = True
                        print("Key received:")
                    if not self.name_received:
                        self.sock.send(self.name.encode('utf-8'))
                        self.name_received = True
                    dec_message = self.fernet.decrypt(message).decode()
                    print(f"Client sent message {message}")
                    print(dec_message)
                    self.enc_messages.append(message)
                    self.messages.append(dec_message)
                    self.msg_list.insert(END, dec_message)
                    self.msg_list.see(END)
                except:
                    message = message.decode()
                    if message.startswith("Welcome"):
                        self.msg_list.insert(END, message)
                        self.msg_list.see(END)
                    elif message.startswith("NAMES"):
                        names = message.split()[1:]
                        self.update_users(names)
                    elif message.startswith("User"):
                        self.msg_list.insert(END, message)
                        self.msg_list.see(END)
                    
            except (socket.error, ConnectionAbortedError, ConnectionResetError) as e:
                            print(f"An error occurred: {e}")
                            self.close()
                            break
                        
            except Exception as e:
                print(f"An error occurred: {e}")
                self.close()
                break
            
    
if __name__ == "__main__":
    StartUI(root)
    root.mainloop()
