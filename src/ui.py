import customtkinter as ctk
from tkinter import filedialog
import req

# function to get summary
def getSum():
    if not file_path:
        outputBox.configure(state='normal')
        outputBox.delete(1.0, "end")
        outputBox.insert("end", "Error: No file selected")
        outputBox.configure(state='disabled')
        return
    
    summary = req.summarize_pdf(file_path)
    summary_text = f"Legal Document Summary:\n{summary}"
    
    # update output box
    outputBox.configure(state='normal')
    outputBox.delete(1.0, "end")
    outputBox.insert("end", summary_text)
    outputBox.configure(state='disabled')


# function to select file
def select_file():
    global file_path
    file_path = filedialog.askopenfilename()
    if file_path:
        fileLabel.configure(text=f"Selected File: {file_path}")

# gui function
def gui():
    global fileLabel, outputBox
    
    # window
    window = ctk.CTk()
    window.title('docSummariser')
    window.geometry('800x500')

    # label
    mainLabel = ctk.CTkLabel(master=window, text='Welcome to docSummariser', font=('Arial', 24))
    mainLabel.pack(pady=20)
    
    # file selection button
    filebtn = ctk.CTkButton(master=window, text='Select File', command=select_file)
    filebtn.pack(pady=10)
    
    # file path label
    fileLabel = ctk.CTkLabel(master=window, text='No file selected', font=('Arial', 14))
    fileLabel.pack(pady=10)

    # send button
    sendbtn = ctk.CTkButton(master=window, text='Get Summary', command=getSum)
    sendbtn.pack(pady=10)

    # output
    outputBox = ctk.CTkTextbox(master=window, height=200, width=600, wrap='word')
    outputBox.pack(pady=10)
    outputBox.configure(state='disabled') 

    window.mainloop()

gui()