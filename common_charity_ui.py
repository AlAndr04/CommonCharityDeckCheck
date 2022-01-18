from deck_check import *
from tkinter import *
from tkinter import filedialog, ttk
glob_filename = ""
def browseFiles():
    global glob_filename
    filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("Ydk files",
                                                        "*.ydk*"),
                                                       ("all files",
                                                        "*.*")))
      
    path_label.configure(text=filename)
    glob_filename = filename
def log_update_card_list():
    log_text.config(state='normal')
    get_card_list()
    log_text.insert('end',"Card list updated.\n\n")
    log_text.config(state='disabled')
def log_update_common_list():
    log_text.config(state='normal')
    create_common_list_files()
    log_text.insert('end',"Common card list updated.\n\n")
    log_text.config(state='disabled')

def log_check_deck_commons():
    log_text.config(state='normal')
    if glob_filename == "":
        result = "ERROR: The filename is empty. Please enter a choose a file\n"
    else:
        result = check_deck_for_commons(glob_filename)
    log_text.insert('end',result+"\n")
    log_text.config(state='disabled')

window = Tk()
window.title("Common Charity Deck Check")
title = Label(text="Common Charity Deck Check")
title.config(font=("Courier", 44))
title.pack()
frame1 = Frame(window)
frame1.pack(fill=BOTH, expand=True)
update_card_list = Button(frame1, text="Update Card List",
                             command = log_update_card_list)
update_card_list.pack(padx=10, pady=10, side=LEFT)
update_common = Button(frame1, text="Update Common Card List",
                command = log_update_common_list)
update_common.pack(padx=10, pady=10, side=RIGHT)
frame2 = Frame(window)
frame2.pack()
path_label = Label(frame2, bg="white", width = 50,
                   relief="ridge", borderwidth=2,height = 2,
                   font=("Helvetica", 11))
path_label.grid(row=0,column=0)
browse = Button(frame2, height=2, text="Browse File",
                             command = browseFiles)
browse.grid(row=0,column=1)
check_deck = Button(frame2, height=2, text="Check Decklist",
                             command = log_check_deck_commons)
check_deck.grid(row=0,column=2)
frame3 = Frame(window)
frame3.pack()
log_text = Text(frame3, bg="white", width = 80,
                  relief="ridge", borderwidth=2,height = 20,
                  font=("Helvetica", 12), state='disabled')
log_text.config(spacing2=10) 
log_text.pack(padx=10, pady=10)
window.mainloop()
