from tkinter import *

class Chatter(Frame):
    def __init__(self, master):
        self.master = master
        self.UI(master)
        
    def UI(self, master):
        master.title("Chatter")

        master.resizable(None, None)
        
        # Row and column configuration
        Grid.columnconfigure(self.master, 1, weight=1)
        Grid.rowconfigure(self.master, 1, weight=1)
        
            
        # Canvas to display chat and scrollbar
        self.canvas = Canvas(master, bg="white", width=400, height=400)
        self.canvas.grid(row=1, columns=5, padx=5, pady=5, sticky="NSEW")
        self.canvas.grid_columnconfigure(0, weight=1)
        self.canvas.grid_rowconfigure(0, weight=1)
        
        
        # Scrollbars
        self.y_bar = Scrollbar(master, orient=VERTICAL, command=self.canvas.yview)
        self.y_bar2 = Scrollbar(master, orient=VERTICAL, command=self.canvas.yview)
        self.y_bar.grid(row=1, column=5, sticky="ns")
        self.y_bar2.grid(row=5, column=3, sticky="ns")
        
        
        #Canvas configuration
        self.canvas.configure(yscrollcommand=self.y_bar.set)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        
        # Chat label, box and send button
        self.chat_label = Label(master, text="Type your message")
        self.chat_label.grid(row=4, columns=3, sticky="nsew")
        self.chat_box = Text(master, height=5)
        self.chat_box.grid(row=5, column=0, columnspan=3, sticky="ew", padx=5, pady=5)
        self.send_button = Button(master, text="Send", width="20", command=self.send)
        self.send_button.grid(row=5, column=4, padx=5, pady=5, sticky="NSEW")

        # Message y coordinate
        self.message_y = 2
        
        # Bind F1 to send
        master.bind("<F1>", self.send)
    
    def send(self, event=None):
        self.inputText = self.chat_box.get("1.0", "end-1c")
        message = Label(self.canvas, text=self.inputText, wraplength=400, justify=LEFT, bg="white")
        self.canvas.create_window((5, self.message_y), window=message, anchor="nw")
        message.update_idletasks()
        self.message_y += message.winfo_height()
        self.chat_box.delete("1.0", "end")
        self.canvas.configure(scrollregion = (0, 0, 0, self.message_y+2))
        

def main():
    root = Tk()
    Chatter(root)
    root.mainloop()

if __name__ == "__main__":
    main()
