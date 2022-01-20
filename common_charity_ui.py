from deck_check import *
from tkinter import *
from tkinter import filedialog, ttk
import tkinter.font as tkFont
glob_filename = ""
rarity_archetypes_to_members = {}
RARITY_LIST = ["Common", "Rare", "Super Rare", "Ultra Rare", "Secret Rare",
              "Ultimate Rare"]
NUM_ARCHETYPE_CARDS = list(range(5,21))
def browseFiles():
    global glob_filename
    filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("Ydk files",
                                                        "*.ydk*"),
                                                       ))
      
    path_label.configure(text=filename)
    glob_filename = filename
def log_update_card_list():
    log_text.config(state='normal')
    get_card_list()
    log_text.insert('end',"Card list updated.\n\n")
    log_text.see('end')
    log_text.config(state='disabled')

def log_update_rarity_list():
    log_text.config(state='normal')
    create_rarity_list_files(rarity_dropdown.get())
    log_text.insert('end',"{} card list updated.\n\n".format(rarity_dropdown.get()))
    log_text.see('end')
    log_text.config(state='disabled')

def log_check_deck_for_rarity():
    log_text.config(state='normal')
    #log_text.configure(font=("Helvetica", 12, "bold"))
    if glob_filename == "":
        result = "ERROR: The filename is empty. Please enter a choose a file\n"
    else:
        deckJson = check_deck_for_rarity(glob_filename, rarity_dropdown.get())
        
        if deckJson["isOfRarity"]:
            result = "The deck is legal for {}-only format.\n".format(rarity_dropdown.get())
        else:
            result = "The deck is not legal for common charity.\n"
            log_text.insert('end',result)
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
    log_text.insert('end',result+"\n")
    #log_text.configure(font=("Helvetica", 12))
    log_text.see('end')
    log_text.config(state='disabled')

def log_get_archetype_for_min_cards():
    global rarity_archetypes_to_members
    rarity_archetypes_to_members = get_archetypes_for_rarity(rarity_dropdown.get(),
                                               int(min_cards_dropdown.get()))
    archetype_dropdown.config(value=list(rarity_archetypes_to_members.keys()))
    archetype_dropdown.current(0)
    result = "The archetypes with at least {} {} cards are:\n".format(min_cards_dropdown.get(),
                                                   rarity_dropdown.get())
    for archetype, cards in rarity_archetypes_to_members.items():
        result+= "{}: {} cards\n".format(archetype, len(cards))
    log_text.config(state='normal')
    log_text.insert('end',result+"\n")
    log_text.see('end')
    log_text.config(state='disabled')

def log_get_archetype_members():
    if archetype_dropdown.get() == "":
        result = "Please get the archetypes for a specific rarity\n"
    else:
        result = "The members from the {} archetype:\n".format(archetype_dropdown.get())
        index = 1
        for card in rarity_archetypes_to_members[archetype_dropdown.get()]:
            result+="{}: {}\n".format(index, card)
            index+=1
    log_text.config(state='normal')
    log_text.insert('end',result+"\n")
    log_text.see('end')
    log_text.config(state='disabled')    
        
window = Tk()
window.title("Rarity Deck Build Tool")
cardRarity = StringVar(window)
cardRarity.set(RARITY_LIST[0])

#Title part
title = Label(text="Rarity Deck Build Tool")
title.config(font=("Courier", 44))
title.pack()

#Row 1: Update card list, rarity dropdown and rarity list
frame1 = Frame(window)
frame1.pack(expand=True)
update_card_list = Button(frame1, text="Update Card List",
                             command = log_update_card_list)
update_card_list.grid(row=0, column=0, padx=40, pady=10)
rarity_dropdown = ttk.Combobox(frame1, state="readonly", value=RARITY_LIST)
rarity_dropdown.current(0)
rarity_dropdown.grid(row=0, column=1, padx=40, pady=10)
update_common = Button(frame1, text="Update Rarity Card List",
                command = log_update_rarity_list)
update_common.grid(row=0, column=2, padx=40, pady=10)

# Row 2: file picker and button
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
                             command = log_check_deck_for_rarity)
check_deck.grid(row=0,column=2)

#Row 3: dropdown to get min cards for archetypes
frame_archetype = Frame(window)
frame_archetype.pack()
curr_archetype = StringVar(frame_archetype, "")
min_cards_label = Label(frame_archetype, text="Minimum cards for the archetype:")
min_cards_label.grid(row=0, column=0, padx=10, pady=10)
min_cards_dropdown = ttk.Combobox(frame_archetype, state="readonly", value=NUM_ARCHETYPE_CARDS)
min_cards_dropdown.current(5)
min_cards_dropdown.grid(row=0, column=1, padx=10, pady=10)
check_archetype_button = Button(frame_archetype, text="Get Archetypes",
                             command = log_get_archetype_for_min_cards)
check_archetype_button.grid(row=0, column=2, padx=10, pady=10)
archetype_label = Label(frame_archetype, text="Archetype:")
archetype_label.grid(row=0, column=3, padx=10, pady=10)
archetype_dropdown = ttk.Combobox(frame_archetype, state="readonly", value=[""])
archetype_dropdown.current(0)
archetype_dropdown.grid(row=0, column=4, padx=10, pady=10)
get_archetype_members_button = Button(frame_archetype, text="Get Archetype Members",
                             command = log_get_archetype_members)
get_archetype_members_button.grid(row=0, column=5, padx=10, pady=10)

#Row 4: log window
frame4 = Frame(window)
frame4.pack()
log_text = Text(frame4, bg="white", width = 80,
                  relief="ridge", borderwidth=2,height = 20,
                state='disabled', font=("Helvetica", 12))
log_text.pack(padx=10, pady=10)
window.mainloop()
