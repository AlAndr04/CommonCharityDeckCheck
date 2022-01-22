from tkinter import *
from tkinter import ttk
from main_logic import search_cards_by_spec
class CardSearchFeature:
    def __init__(self, window, rarity, log):
        card_type = ["","Monster","Spell","Trap"]
        self.card_subtype = {"Monster":["","Normal","Effect","Ritual",
                                        "Fusion","Synchro","Xyz","Link"],
                             "Spell":["","Normal","Quick-Play","Continuous",
                                      "Field","Ritual"],
                             "Trap":["","Normal","Continuous","Counter"]}
        self.monster_type = ["","Aqua","Beast","Beast-Warrior","Creator God","Cyberse","Dinosaur",
                             "Creator-God","Cyberse","Dinosaur","Divine-Beast","Dragon","Fairy",
                             "Fiend","Fish","Insect","Machine","Plant","Psychic","Pyro", "Reptile",
                             "Rock","Sea Serpent","Spellcaster","Thunder","Warrior","Winged Beast",
                             "Wyrm","Zombie"]
        self.attributes = ["","DARK","DIVINE","EARTH","FIRE","LIGHT","WATER","WIND"]
        self.monster_sub_type = ["","Toon","Gemini","Union","Spirit","Tuner","Flip"]
        self.rarity_dropdown = rarity
        self.log_text = log
        frame_search_title = Frame(window)
        frame_search_title.pack(fill=BOTH, expand=YES)
        search_label = Label(frame_search_title, text="Card Search",
                                font= ("Courier", 25))
        search_label.pack(side=LEFT,padx=20)
        frame_search_button = Button(frame_search_title, text="Show/Hide",
                        command = lambda: self.show_hide_button(frame_search,
                                                           frame_search_title))
        frame_search_button.pack(side=RIGHT, padx=20)
        frame_search = Frame(window)
        card_name_label = Label(frame_search, text="Card Name")
        card_name_label.grid(row=0, column=0, padx=2)
        self.card_name_entry = Entry(frame_search)
        self.card_name_entry.grid(row=1, column=0, padx=10)
        card_effect_label = Label(frame_search, text="Card Effect")
        card_effect_label.grid(row=2, column=0, padx=2)
        self.card_effect_entry = Entry(frame_search)
        self.card_effect_entry.grid(row=3, column=0, padx=10)
        card_type_label = Label(frame_search, text="Card Type")
        card_type_label.grid(row=0, column=1, padx=2)
        self.card_type_dropdown = ttk.Combobox(frame_search, state="readonly", value=card_type)
        self.card_type_dropdown.grid(row=1, column=1, padx=10)
        self.card_type_dropdown.bind("<<ComboboxSelected>>", self.update_dropdowns)
        card_sub_type_label = Label(frame_search, text="Card Sub-Type")
        card_sub_type_label.grid(row=2, column=1, padx=2)
        self.card_sub_type_dropdown = ttk.Combobox(frame_search, state="disabled", value=[""])
        self.card_sub_type_dropdown.grid(row=3, column=1, padx=10)
        monster_type_label = Label(frame_search, text="Monster Type")
        monster_type_label.grid(row=0, column=2, padx=2)
        self.monster_type_dropdown = ttk.Combobox(frame_search, state="disabled", value=[""])
        self.monster_type_dropdown.grid(row=1, column=2, padx=10)
        monster_sub_type_label = Label(frame_search, text="Monster Sub-Type")
        monster_sub_type_label.grid(row=2, column=2, padx=2)
        self.monster_sub_type_dropdown = ttk.Combobox(frame_search, state="disabled", value=[""])
        self.monster_sub_type_dropdown.grid(row=3, column=2, padx=10)
        attribute_label = Label(frame_search, text="Attribute")
        attribute_label.grid(row=0, column=3, padx=2)
        self.attribute_dropdown = ttk.Combobox(frame_search, state="disabled", value=[""])
        self.attribute_dropdown.grid(row=1, column=3, padx=10)
        level_label = Label(frame_search, text="Level/Rank/Rating")
        level_label.grid(row=2, column=3, padx=2)
        self.level_entry = Entry(frame_search, state="disabled")
        self.level_entry.grid(row=3, column=3, padx=10)
        atk_label = Label(frame_search, text="ATK")
        atk_label.grid(row=0, column=4, padx=2)
        self.atk_entry = Entry(frame_search, state="disabled")
        self.atk_entry.grid(row=1, column=4, padx=10)
        def_label = Label(frame_search, text="DEF")
        def_label.grid(row=2, column=4, padx=2)
        self.def_entry = Entry(frame_search, state="disabled")
        self.def_entry.grid(row=3, column=4, padx=10)
        self.is_penlum = IntVar()
        self.penlum = Checkbutton(frame_search, state="disabled",
                                  variable=self.is_penlum, text="Pendulum")
        self.penlum.grid(row=4, column=2, padx=10)
        get_cards_button = Button(frame_search, text="Get Cards",
                                     command = self.log_get_cards)
        get_cards_button.grid(row=4, column=3, padx=10)

    def show_hide_button(self, frame, prev_frame):
        if frame.winfo_ismapped():
            frame.pack_forget()
        else:
            frame.pack(after=prev_frame, padx=10, pady=10)
    def update_dropdowns(self, e):
        self.card_sub_type_dropdown.config(
            value=self.card_subtype[self.card_type_dropdown.get()],
            state="readonly")
        if self.card_type_dropdown.get() == "Monster":
            self.monster_type_dropdown.config(
                value=self.monster_type,
                state="readonly")
            self.monster_sub_type_dropdown.config(
                value=self.monster_sub_type,
                state="readonly")
            self.attribute_dropdown.config(
                value=self.attributes,
                state="readonly")
            self.level_entry.config(
                state="normal")
            self.atk_entry.config(
                state="normal")
            self.def_entry.config(
                state="normal")
            self.penlum.config(
                state="normal")
        else:
            self.monster_type_dropdown.config(
                value=[""],
                state="disabled")
            self.monster_sub_type_dropdown.config(
                value=[""],
                state="disabled")
            self.attribute_dropdown.config(
                value=[""],
                state="disabled")
            self.level_entry.config(
                state="disabled")
            self.atk_entry.config(
                state="disabled")
            self.def_entry.config(
                state="disabled")
            self.penlum.config(
                state="disabled")
    def log_get_cards(self):
        spec = {"name":self.card_name_entry.get(),
                "effect":self.card_effect_entry.get(),
                "type":self.card_type_dropdown.get(),
                "sub_type":self.card_sub_type_dropdown.get(),
                "monster_type":self.monster_type_dropdown.get(),
                "monster_sub_type": self.monster_sub_type_dropdown.get(),
                "attribute": self.attribute_dropdown.get(),
                "level": self.level_entry.get(),
                "is_penlum":self.is_penlum.get()==1,
                "ATK": self.atk_entry.get(),
                "DEF": self.def_entry.get()}
        print(spec)
        cards_match = search_cards_by_spec(self.rarity_dropdown.get(), spec)
        
        result = "The {} cards that match the given descriptions are:\n".format(
            self.rarity_dropdown.get())
        for card in cards_match:
            result+= "{}\n".format(card)
        self.log_text.config(state='normal')
        self.log_text.insert('end',result+"\n")
        self.log_text.see('end')
        self.log_text.config(state='disabled')
