from tkinter import *
from tkinter import filedialog
from main_logic import check_deck_for_rarity
class DeckFeature:
    def __init__(self, window, rarity, log):
        self.glob_filename=""
        self.rarity_dropdown = rarity
        self.log_text = log
        frame_deck_title = Frame(window)
        frame_deck_title.pack(fill=BOTH, expand=YES)
        deck_label = Label(frame_deck_title, text="Deck Verification Features",
                                font= ("Courier", 25))
        deck_label.pack(side=LEFT,padx=20)
        frame_archetype_button = Button(frame_deck_title, text="Show/Hide",
                        command = lambda: self.show_hide_button(frame2,
                                                           frame_deck_title))
        frame_archetype_button.pack(side=RIGHT, padx=20)
        frame2 = Frame(window)
        path_label = Label(frame2, bg="white", width = 50,
                           relief="ridge", borderwidth=2,height = 2,
                           font=("Helvetica", 11))
        path_label.grid(row=0,column=0)
        browse = Button(frame2, height=2, text="Browse File",
                                     command = lambda: self.browseFiles(path_label))
        browse.grid(row=0,column=1)
        check_deck = Button(frame2, height=2, text="Check Decklist",
                                     command = self.log_check_deck_for_rarity)
        check_deck.grid(row=0,column=2)

    def show_hide_button(self, frame, prev_frame):
        if frame.winfo_ismapped():
            frame.pack_forget()
        else:
            frame.pack(after=prev_frame,padx=10, pady=10)
    
    def browseFiles(self, path_label):
            filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("Ydk files",
                                                        "*.ydk*"),
                                                       ))
      
            path_label.configure(text=filename)
            self.glob_filename = filename
    
    def log_check_deck_for_rarity(self):
        self.log_text.config(state='normal')
        #log_text.configure(font=("Helvetica", 12, "bold"))
        if self.glob_filename == "":
            result = "ERROR: The filename is empty. Please enter a choose a file\n"
        else:
            deckJson = check_deck_for_rarity(self.glob_filename, self.rarity_dropdown.get())
            
            if deckJson["isOfRarity"]:
                result = "The deck is legal for {}-only format.\n".format(self.rarity_dropdown.get())
            else:
                result = "The deck is not legal for common charity.\n"
                self.log_text.insert('end',result)
                result = ""
                #log_text.configure(font=("Helvetica", 12))
                if "unavailableCards" in deckJson.keys():
                    result += "WARNING: The deck has card ids that are not in the database.\n"
                if "unavailableCards" in deckJson.keys():
                    result += "The card ids that are not available are:\n"
                    for card_id in deckJson["unavailableCards"]:
                        result+=card_id+"\n"
                if "notCardsOfRarity" in deckJson.keys():
                    result+="The illegal cards in the deck are:\n"
                    for card in deckJson["notCardsOfRarity"]:
                        result+=card+"\n"
        self.log_text.insert('end',result+"\n")
        #log_text.configure(font=("Helvetica", 12))
        self.log_text.see('end')
        self.log_text.config(state='disabled')
