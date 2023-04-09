from tkinter import * 

class Chatter(Frame):
    def __init__(self, master):
        self.master = master
        self.UI(master)
        
    def UI(self, master):
        master.title("Chatter")
        master.geometry("500x300")
        master.resizable(None, None)
        
        # Row and column configuration
        Grid.rowconfigure(self.master, 3, weight=1)
        Grid.columnconfigure(self.master, 1, weight=1)
         
        #Canvas to display chat
        self.canvas = Canvas(master, width=200, height=200, bg="white")
        self.canvas.grid(row=1, column=1, sticky="NSEW", padx=5, pady=5)  
          
        self.chat_label = Label(master, text="Type your message").grid(row=2, column=1)  
        self.chat_box = Text(master)
        master.bind("<:>", self.send)
        self.chat_box.grid(row=3, column=1, sticky="NEW")
        self.send_button = Button(master, text="Send", width= "20", command=self.send)
        self.send_button.grid(row=4, column=1, sticky="N")
        
        self.message_y = 2
        
        
        
    def send(self,event=None):
        self.inputText = self.chat_box.get("1.0", "end-1c")
        message = Label(self.canvas, text=self.inputText, wraplength=400, justify=LEFT, bg="white")
        self.canvas.create_window((5, self.message_y), window=message, anchor="nw")
        message.update_idletasks()
        self.message_y += message.winfo_height()
        self.chat_box.delete("1.0", "end")
        
        
        
        
        
        
              
def main():
    root = Tk()
    Chatter(root)
    root.mainloop()


if __name__ == "__main__":
    main()