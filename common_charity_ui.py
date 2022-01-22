from main_logic import *
from tkinter import *
from tkinter import filedialog, ttk
from deck_check_feature import DeckFeature
from archetype_feature import ArchetypeFeature
from card_search_feature import CardSearchFeature
import tkinter.font as tkFont
glob_filename = ""
rarity_archetypes_to_members = {}
RARITY_LIST = ["Common", "Rare", "Super Rare", "Ultra Rare", "Secret Rare",
              "Ultimate Rare"]


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
frame4 = Frame(window)
log_text = Text(frame4, bg="white", width = 90,
                  relief="ridge", borderwidth=2,height = 20,
                state='disabled', font=("Helvetica", 12))
# Row 2: file picker and button

deck_feature = DeckFeature(window, rarity_dropdown, log_text)


archetype_feature = ArchetypeFeature(window, rarity_dropdown, log_text)
#Row 4: log window
card_search_feature = CardSearchFeature(window, rarity_dropdown, log_text)
frame4.pack()

log_text.pack(padx=10, pady=10)
window.mainloop()
