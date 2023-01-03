import pandas
import json
import random
from tkinter import *
from tkinter import messagebox

BACKGROUND_COLOR = "#B1DDC6"
BUTTON_COLOR = "#8EC3B0"


# ---------------------------- SAVE SETTINGS ------------------------------- #
def save_settings():
    language_selected = radio_state_language.get()
    level_selected = radio_state_level.get()
    setting_dict = {"language": language_selected, "native": "English", "level": level_selected}
    with open("data/language.json", "w") as setting_file:
        json.dump(setting_dict, setting_file, indent=4)
    make_dataframe()
    clear_card()
    selection_window.destroy()


# ---------------------------- SET LANGUAGE AND LEVEL ------------------------------- #
def set_language_level():
    global radio_state_language, radio_state_level, selection_window, flip_timer
    window.after_cancel(flip_timer)

    with open("data/language.json", "r") as choice_file:
        choice_dict = json.load(choice_file)

    language_selection = choice_dict["language"]
    level_selection = choice_dict["level"]

    selection_window = Toplevel(window)
    selection_window.title("Set Language and Level")
    selection_window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)

    language_prompt = Label(selection_window, bg=BACKGROUND_COLOR, text="Please select a language:", font=20)
    language_prompt.grid(row=0, column=0, padx=20, pady=20, sticky="w")
    radio_state_language = StringVar()
    radiobutton_german = Radiobutton(selection_window, bg=BACKGROUND_COLOR, text="German", font=20, value="German",
                                     variable=radio_state_language)
    radiobutton_french = Radiobutton(selection_window, bg=BACKGROUND_COLOR, text="French", font=20, value="French",
                                     variable=radio_state_language)
    radiobutton_spanish = Radiobutton(selection_window, bg=BACKGROUND_COLOR, text="Spanish", font=20, value="Spanish",
                                      variable=radio_state_language)
    radiobutton_italian = Radiobutton(selection_window, bg=BACKGROUND_COLOR, text="Italian", font=20, value="Italian",
                                      variable=radio_state_language)
    radio_state_language.set(language_selection)
    radiobutton_german.grid(row=1, column=0, padx=20, sticky="w")
    radiobutton_french.grid(row=2, column=0, padx=20, sticky="w")
    radiobutton_spanish.grid(row=3, column=0, padx=20, sticky="w")
    radiobutton_italian.grid(row=4, column=0, padx=20, sticky="w")

    level_prompt = Label(selection_window, bg=BACKGROUND_COLOR, text="Please select a level:", font=20)
    level_prompt.grid(row=0, column=1, padx=20, pady=20, sticky="w")
    radio_state_level = StringVar()
    radiobutton_introductory = Radiobutton(selection_window, bg=BACKGROUND_COLOR, text="Introductory", font=20,
                                           value="Introductory", variable=radio_state_level)
    radiobutton_beginner_1 = Radiobutton(selection_window, bg=BACKGROUND_COLOR, text="Beginner 1", font=20,
                                         value="Beginner 1", variable=radio_state_level)
    radiobutton_beginner_2 = Radiobutton(selection_window, bg=BACKGROUND_COLOR, text="Beginner 2", font=20,
                                         value="Beginner 2", variable=radio_state_level)
    radiobutton_beginner_3 = Radiobutton(selection_window, bg=BACKGROUND_COLOR, text="Beginner 3", font=20,
                                         value="Beginner 3", variable=radio_state_level)
    radiobutton_intermediate_1 = Radiobutton(selection_window, bg=BACKGROUND_COLOR, text="Intermediate 1", font=20,
                                             value="Intermediate 1", variable=radio_state_level)
    radiobutton_intermediate_2 = Radiobutton(selection_window, bg=BACKGROUND_COLOR, text="Intermediate 2", font=20,
                                             value="Intermediate 2", variable=radio_state_level)
    radiobutton_intermediate_3 = Radiobutton(selection_window, bg=BACKGROUND_COLOR, text="Intermediate 3", font=20,
                                             value="Intermediate 3", variable=radio_state_level)
    radiobutton_comprehensive = Radiobutton(selection_window, bg=BACKGROUND_COLOR, text="Comprehensive", font=20,
                                            value="Comprehensive", variable=radio_state_level)
    radio_state_level.set(level_selection)
    radiobutton_introductory.grid(row=1, column=1, padx=20, sticky="w")
    radiobutton_beginner_1.grid(row=2, column=1, padx=20, sticky="w")
    radiobutton_beginner_2.grid(row=3, column=1, padx=20, sticky="w")
    radiobutton_beginner_3.grid(row=4, column=1, padx=20, sticky="w")
    radiobutton_intermediate_1.grid(row=5, column=1, padx=20, sticky="w")
    radiobutton_intermediate_2.grid(row=6, column=1, padx=20, sticky="w")
    radiobutton_intermediate_3.grid(row=7, column=1, padx=20, sticky="w")
    radiobutton_comprehensive.grid(row=8, column=1, padx=20, sticky="w")

    save_button = Button(selection_window, text="Save", bg=BUTTON_COLOR, fg="white", font=("Ariel", 15),
                         command=save_settings, highlightthickness=0)
    save_button.grid(row=9, column=0, sticky="w", pady=20)

    cancel_button = Button(selection_window, text="Cancel", bg=BUTTON_COLOR, fg="white", font=("Ariel", 15),
                           command=selection_window.destroy, highlightthickness=0)
    cancel_button.grid(row=9, column=2, sticky="e", pady=20)

    selection_window.focus()
    selection_window.mainloop()


# ---------------------------- LANGUAGES ------------------------------- #
def languages():
    with open("data/language.json", "r") as choice_file:
        choice_dict = json.load(choice_file)

    foreign_choice = choice_dict["language"]
    file_choice = "data/English-French.csv"

    if foreign_choice == "French":
        pass
    if foreign_choice == "German":
        file_choice = "data/English-German.csv"
    if foreign_choice == "Italian":
        file_choice = "data/English-Italian.csv"
    if foreign_choice == "Spanish":
        file_choice = "data/English-Spanish.csv"

    native_choice = choice_dict["native"]

    choice_info = [foreign_choice, file_choice, native_choice]

    return choice_info


# ---------------------------- LEVELS ------------------------------- #
def levels():
    with open("data/language.json", "r") as choice_file:
        choice_dict = json.load(choice_file)

    range_choice = choice_dict["level"]
    series_start = 0
    series_end = 2998

    if range_choice == "Beginner 1":
        series_end = 499
    if range_choice == "Beginner 2":
        series_start = 500
        series_end = 999
    if range_choice == "Beginner 3":
        series_start = 1000
        series_end = 1499
    if range_choice == "Intermediate 1":
        series_start = 1500
        series_end = 1999
    if range_choice == "Intermediate 2":
        series_start = 2000
        series_end = 2499
    if range_choice == "Intermediate 3":
        series_start = 2500
    if range_choice == "Introductory":
        series_end = 249
    if range_choice == "Comprehensive":
        pass

    random_range = [series_start, series_end]
    return random_range


# ---------------------------- DATAFRAME ------------------------------- #
def make_dataframe():
    global language_foreign, language_native, small_frame, data_list, flip_timer
    window.after_cancel(flip_timer)
    language_choice_reset = languages()
    language_foreign = language_choice_reset[0]
    language_file = language_choice_reset[1]
    language_native = language_choice_reset[2]

    level_choice = levels()
    starting = level_choice[0]
    ending = level_choice[1]

    large_frame = pandas.read_csv(language_file)
    small_frame_1 = large_frame[large_frame.index <= ending]
    small_frame_2 = small_frame_1[small_frame_1.index >= starting]
    small_frame_2.to_csv("data/subset.csv", index=False)

    small_frame = pandas.read_csv("data/subset.csv")
    data_list = small_frame.to_dict(orient="records")


# ---------------------------- FOREIGN CARD ------------------------------- #
def foreign_card():
    global little_dict, flip_timer
    window.after_cancel(flip_timer)
    try:
        little_dict = random.choice(data_list)
    except IndexError:
        messagebox.showinfo(title="Level Complete", message="Congratulations!  You have completed this level.  "
                                                            "Reset or choose another level.")
    else:
        foreign_word = little_dict[language_foreign]
        canvas.itemconfig(card_word_text, text=foreign_word, fill="black")
        canvas.itemconfig(card_language_text, text=language_foreign, fill="black")
        canvas.itemconfig(card_image, image=card_front_img)
        flip_timer = window.after(3000, func=native_card)


# ---------------------------- NATIVE CARD ------------------------------- #
def native_card():
    native_word = little_dict[language_native]
    canvas.itemconfig(card_word_text, text=native_word, fill="white")
    canvas.itemconfig(card_language_text, text=language_native, fill="white")
    canvas.itemconfig(card_image, image=card_back_img)


# ---------------------------- CLEAR CARD ------------------------------- #
def clear_card():
    canvas.itemconfig(card_word_text, text="", fill="black")
    canvas.itemconfig(card_language_text, text="", fill="black")
    canvas.itemconfig(card_image, image=card_front_img)


# ---------------------------- REVERSE ORDER ------------------------------- #
def reverse_order():
    global language_foreign, language_native, flip_timer
    window.after_cancel(flip_timer)
    place_holder = language_foreign
    language_foreign = language_native
    language_native = place_holder
    clear_card()


# ---------------------------- WORD KNOWN ------------------------------- #
def word_known():
    try:
        data_list.remove(little_dict)
    except ValueError:
        messagebox.showinfo(title="Level Complete", message="Congratulations!  You have completed this level.  "
                                                            "Reset or choose another level.")
    else:
        update_frame = pandas.DataFrame.from_dict(data_list)
        update_frame.to_csv("data/subset.csv", index=False)
        foreign_card()


# ---------------------------- WASTE TIME ------------------------------- #
def waste_time():
    pass


# ---------------------------- UI SETUP ------------------------------- #
language_choice = languages()
language_foreign = language_choice[0]
language_native = language_choice[2]

try:
    small_frame = pandas.read_csv("data/subset.csv")
except:
    make_dataframe()
    small_frame = pandas.read_csv("data/subset.csv")

data_list = small_frame.to_dict(orient="records")

window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, waste_time)

canvas = Canvas(width=800, height=526)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_image = canvas.create_image(400, 263, image=card_front_img)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=1, column=0, columnspan=3)
card_language_text = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
card_word_text = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))

cross_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=cross_image, command=foreign_card, highlightthickness=0)
unknown_button.grid(row=2, column=0)

check_image = PhotoImage(file="images/right.png")
known_button = Button(image=check_image, command=word_known, highlightthickness=0)
known_button.grid(row=2, column=2)

choose_language_level = Button(text="Set Language and Level", bg=BUTTON_COLOR, fg="white", font=("Ariel", 15),
                               command=set_language_level, highlightthickness=0)
choose_language_level.grid(row=0, column=0, sticky="w", pady=20)

begin_button = Button(text="Begin", bg=BUTTON_COLOR, fg="white", font=("Ariel", 15), command=foreign_card,
                      highlightthickness=0)
begin_button.grid(row=0, column=1, sticky="w", pady=20)

reverse_button = Button(text="Reverse", bg=BUTTON_COLOR, fg="white", font=("Ariel", 15), command=reverse_order,
                        highlightthickness=0)
reverse_button.grid(row=0, column=1, sticky="e", pady=20)

reset_button = Button(text="Reset Progress", bg=BUTTON_COLOR, fg="white", font=("Ariel", 15), command=make_dataframe,
                      highlightthickness=0)
reset_button.grid(row=0, column=2, sticky="e", pady=20)

word_index = 0
little_dict = {}


window.mainloop()
