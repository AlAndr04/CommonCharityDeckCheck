from tkinter import *
from tkinter import ttk
from main_logic import get_archetypes_for_rarity
class ArchetypeFeature:
    def __init__(self, window, rarity, log):
        self.num_archetypes_to_members={}
        self.num_archetype_cards = list(range(5,21))
        self.rarity_dropdown = rarity
        self.log_text = log
        frame_archetype_title = Frame(window)
        frame_archetype_title.pack(fill=BOTH, expand=YES)
        archetype_label = Label(frame_archetype_title, text="Archetype Features",
                                font= ("Courier", 25))
        archetype_label.pack(side=LEFT,padx=20)
        frame_archetype_button = Button(frame_archetype_title, text="Show/Hide",
                        command = lambda: self.show_hide_button(frame_archetype,
                                                           frame_archetype_title))
        frame_archetype_button.pack(side=RIGHT, padx=20)
        frame_archetype = Frame(window)
        min_cards_label = Label(frame_archetype, text="Minimum cards for the archetype:")
        min_cards_label.grid(row=0, column=0, padx=2)
        min_cards_dropdown = ttk.Combobox(frame_archetype, state="readonly", value=self.num_archetype_cards)
        min_cards_dropdown.current(5)
        min_cards_dropdown.grid(row=0, column=1)
        check_archetype_button = Button(frame_archetype, text="Get Archetypes",
                                     command = lambda: self.log_get_archetype_for_min_cards(min_cards_dropdown))
        check_archetype_button.grid(row=0, column=2, padx=10)
        archetype_label = Label(frame_archetype, text="Archetype:")
        archetype_label.grid(row=0, column=3, padx=2)
        self.archetype_dropdown = ttk.Combobox(frame_archetype, state="readonly", value=[""])
        self.archetype_dropdown.current(0)
        self.archetype_dropdown.grid(row=0, column=4)
        get_archetype_members_button = Button(frame_archetype, text="Get Archetype Members",
                                     command = self.log_get_archetype_members)
        get_archetype_members_button.grid(row=0, column=5, padx=10)

    def show_hide_button(self, frame, prev_frame):
        if frame.winfo_ismapped():
            frame.pack_forget()
        else:
            frame.pack(after=prev_frame, padx=10, pady=10)
    
    def log_get_archetype_for_min_cards(self, min_cards_dropdown):
        global rarity_archetypes_to_members
        rarity_archetypes_to_members = get_archetypes_for_rarity(self.rarity_dropdown.get(),
                                                   int(min_cards_dropdown.get()))
        self.archetype_dropdown.config(value=list(rarity_archetypes_to_members.keys()))
        self.archetype_dropdown.current(0)
        result = "The archetypes with at least {} {} cards are:\n".format(min_cards_dropdown.get(),
                                                       self.rarity_dropdown.get())
        for archetype, cards in rarity_archetypes_to_members.items():
            result+= "{}: {} cards\n".format(archetype, len(cards))
        self.log_text.config(state='normal')
        self.log_text.insert('end',result+"\n")
        self.log_text.see('end')
        self.log_text.config(state='disabled')

    def log_get_archetype_members(self):
        if self.archetype_dropdown.get() == "":
            result = "Please get the archetypes for a specific rarity\n"
        else:
            result = "The members of the {} archetype in {} rarity:\n".format(self.archetype_dropdown.get(),
                                                                     self.rarity_dropdown.get())
            index = 1
            for card in rarity_archetypes_to_members[self.archetype_dropdown.get()]:
                result+="{}: {}\n".format(index, card)
                index+=1
        self.log_text.config(state='normal')
        self.log_text.insert('end',result+"\n")
        self.log_text.see('end')
        self.log_text.config(state='disabled')  
