import json
from pathlib import Path
import random
import tkinter as tk
from tkinter import messagebox

import pandas as pd

BACKGROUND_COLOR = "#B1DDC6"
BUTTON_COLOR = "#8EC3B0"

CUR_DIR = Path(__file__).parent  # directory containing this file
SETTINGS_PATH = CUR_DIR / "data" / "language.json"
TRANSLATION_INDICES_PATH = CUR_DIR / "data" / "subset_indices.json"

LANGUAGES = ("German", "French", "Spanish", "Italian")
LEVELS = (
    "Introductory",
    "Beginner 1",
    "Beginner 2",
    "Beginner 3",
    "Intermediate 1",
    "Intermediate 2",
    "Intermediate 3",
    "Comprehensive",
)

# defaults, may be overwritten by contents of data/language.json
SETTINGS = {
    "language": "German",
    "native": "English",
    "level": "Introductory",
}
if SETTINGS_PATH.exists():
    with SETTINGS_PATH.open() as f:
        SETTINGS = json.load(f)

# ---------------------------- SAVE SETTINGS ------------------------------- #
def save_settings():
    """save settings to file, and reselect a random order of questions"""
    global LANGUAGE_FOREIGN, LANGUAGE_NATIVE, TRANSLATION_INDICES, TRANSLATIONS, SETTINGS
    language_selected = radio_state_language.get()
    level_selected = radio_state_level.get()
    SETTINGS = {
        "language": language_selected,
        "native": "English",
        "level": level_selected,
    }
    LANGUAGE_FOREIGN, language_file, LANGUAGE_NATIVE = languages()
    TRANSLATIONS = pd.read_csv(CUR_DIR / "data" / language_file)
    TRANSLATION_INDICES = choose_translation_indices()
    choose_translation_indices()
    messagebox.showinfo(title="Save", message="Your changes have been saved.")
    clear_card()
    selection_window.destroy()


def set_language_level():
    """Create a menu for the user to select language and difficulty level"""
    global radio_state_language, radio_state_level, selection_window, flip_timer, SETTINGS
    window.after_cancel(flip_timer)

    language_selection = SETTINGS["language"]
    level_selection = SETTINGS["level"]

    selection_window = tk.Toplevel(window)
    selection_window.title("Set Language and Level")
    selection_window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)

    # add buttons for the user to select a language
    language_prompt = tk.Label(
        selection_window, bg=BACKGROUND_COLOR, text="Please select a language:", font=20
    )
    language_prompt.grid(row=0, column=0, padx=20, pady=20, sticky="w")
    radio_state_language = tk.StringVar()
    for ii, language in enumerate(LANGUAGES):
        lang_radiobutton = tk.Radiobutton(
            selection_window,
            bg=BACKGROUND_COLOR,
            text=language,
            font=20,
            value=language,
            variable=radio_state_language,
        )
        lang_radiobutton.grid(row=ii + 1, column=0, padx=20, sticky="w")
    radio_state_language.set(language_selection)
    # add buttons for the user to select the level
    level_prompt = tk.Label(
        selection_window, bg=BACKGROUND_COLOR, text="Please select a level:", font=20
    )
    level_prompt.grid(row=0, column=1, padx=20, pady=20, sticky="w")
    radio_state_level = tk.StringVar()
    for ii, level in enumerate(LEVELS):
        level_radiobutton = tk.Radiobutton(
            selection_window,
            bg=BACKGROUND_COLOR,
            text=level,
            font=20,
            value=level,
            variable=radio_state_level,
        )
        level_radiobutton.grid(row=ii + 1, column=1, padx=20, sticky="w")
    radio_state_level.set(level_selection)

    save_button = tk.Button(
        selection_window,
        text="Save",
        bg=BUTTON_COLOR,
        fg="white",
        font=("Ariel", 15),
        command=save_settings,
        highlightthickness=0,
    )
    save_button.grid(row=9, column=0, sticky="w", pady=20)

    cancel_button = tk.Button(
        selection_window,
        text="Cancel",
        bg=BUTTON_COLOR,
        fg="white",
        font=("Ariel", 15),
        command=selection_window.destroy,
        highlightthickness=0,
    )
    cancel_button.grid(row=9, column=2, sticky="e", pady=20)

    selection_window.focus()
    selection_window.mainloop()


def languages():
    """returns the foreign language, the file containing translations,
    and the native language"""
    global SETTINGS
    foreign_lang = SETTINGS["language"]
    file_choice = CUR_DIR / "data" / f"English-{foreign_lang}.csv"
    native_lang = SETTINGS["native"]
    return foreign_lang, file_choice, native_lang


def choose_translation_indices():
    """Return a randomly shuffled list of translation numbers based on the
    difficulty level.

    Also write this to file."""
    global TRANSLATION_INDICES, SETTINGS
    level = SETTINGS["level"]
    start = 0
    end = len(TRANSLATIONS)
    if level == "Beginner 1":
        end = 500
    elif level == "Beginner 2":
        start = 500
        end = 1000
    elif level == "Beginner 3":
        start = 1000
        end = 1500
    elif level == "Intermediate 1":
        start = 1500
        end = 2000
    elif level == "Intermediate 2":
        start = 2000
        end = 2500
    elif level == "Intermediate 3":
        start = 2500
    elif level == "Introductory":
        end = 250
    # choose a random order to iterate questions in
    TRANSLATION_INDICES = list(range(start, end))
    random.shuffle(TRANSLATION_INDICES)
    subset_indices_path = CUR_DIR / "data" / "subset_indices.json"
    with subset_indices_path.open("w") as f:
        json.dump(TRANSLATION_INDICES, f)


def foreign_card():
    """show the user a random card in the foreign language of the
    chosen language-level combo"""
    global CUR_TRANSLATION, flip_timer, TRANSLATION_INDICES, TRANSLATIONS, LANGUAGE_FOREIGN
    window.after_cancel(flip_timer)
    if not TRANSLATION_INDICES:
        messagebox.showinfo(
            title="Level Complete",
            message="Congratulations!  You have completed this level.  "
            "Reset or choose another level.",
        )
        return
    translation_idx = random.randrange(0, len(TRANSLATION_INDICES) - 1)
    # move the selected translation to the end of the indices
    # this way it will be removed if the user got it right
    # because word_known() always removes the last index
    # in TRANSLATION_INDICES
    TRANSLATION_INDICES[translation_idx], TRANSLATION_INDICES[-1] = (
        TRANSLATION_INDICES[-1],
        TRANSLATION_INDICES[translation_idx],
    )
    CUR_TRANSLATION = TRANSLATIONS.iloc[TRANSLATION_INDICES[-1]]
    foreign_word = CUR_TRANSLATION[LANGUAGE_FOREIGN]
    # print(f'{TRANSLATION_INDICES[translation_idx] = }, {len(TRANSLATION_INDICES) = }')
    canvas.itemconfig(card_word_text, text=foreign_word, fill="black")
    canvas.itemconfig(card_language_text, text=LANGUAGE_FOREIGN, fill="black")
    canvas.itemconfig(card_image, image=card_front_img)
    flip_timer = window.after(3000, func=native_card)


def native_card():
    """show the word in the native language"""
    native_word = CUR_TRANSLATION[LANGUAGE_NATIVE]
    canvas.itemconfig(card_word_text, text=native_word, fill="white")
    canvas.itemconfig(card_language_text, text=LANGUAGE_NATIVE, fill="white")
    canvas.itemconfig(card_image, image=card_back_img)


def clear_card():
    canvas.itemconfig(card_word_text, text="", fill="black")
    canvas.itemconfig(card_language_text, text="", fill="black")
    canvas.itemconfig(card_image, image=card_front_img)


def reverse_order():
    """swap foreign and native languages"""
    global LANGUAGE_FOREIGN, LANGUAGE_NATIVE, flip_timer
    window.after_cancel(flip_timer)
    LANGUAGE_FOREIGN, LANGUAGE_NATIVE = LANGUAGE_NATIVE, LANGUAGE_FOREIGN
    clear_card()


def word_known():
    """the user got the translation, so remove it from the list
    and show another card"""
    global TRANSLATION_INDICES
    if not TRANSLATION_INDICES:
        messagebox.showinfo(
            title="Level Complete",
            message="Congratulations!  You have completed this level.  "
            "Reset or choose another level.",
        )
        return
    TRANSLATION_INDICES.pop()
    foreign_card()


# ---------------------------- UI SETUP ------------------------------- #
window = tk.Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, lambda: None)  # pause for 3 seconds

canvas = tk.Canvas(width=800, height=526)
card_front_img = tk.PhotoImage(file=CUR_DIR / "images" / "card_front.png")
card_back_img = tk.PhotoImage(file=CUR_DIR / "images" / "card_back.png")
card_image = canvas.create_image(400, 263, image=card_front_img)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=1, column=0, columnspan=3)
card_language_text = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
card_word_text = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))

cross_image = tk.PhotoImage(file=CUR_DIR / "images" / "wrong.png")
unknown_button = tk.Button(
    image=cross_image, command=foreign_card, highlightthickness=0
)
unknown_button.grid(row=2, column=0)

check_image = tk.PhotoImage(file=CUR_DIR / "images" / "right.png")
known_button = tk.Button(image=check_image, command=word_known, highlightthickness=0)
known_button.grid(row=2, column=2)

choose_language_level = tk.Button(
    text="Set Language and Level",
    bg=BUTTON_COLOR,
    fg="white",
    font=("Ariel", 15),
    command=set_language_level,
    highlightthickness=0,
)
choose_language_level.grid(row=0, column=0, sticky="w", pady=20)

begin_button = tk.Button(
    text="Begin",
    bg=BUTTON_COLOR,
    fg="white",
    font=("Ariel", 15),
    command=foreign_card,
    highlightthickness=0,
)
begin_button.grid(row=0, column=1, sticky="w", pady=20)

reverse_button = tk.Button(
    text="Reverse",
    bg=BUTTON_COLOR,
    fg="white",
    font=("Ariel", 15),
    command=reverse_order,
    highlightthickness=0,
)
reverse_button.grid(row=0, column=1, sticky="e", pady=20)

reset_button = tk.Button(
    text="Reset Progress",
    bg=BUTTON_COLOR,
    fg="white",
    font=("Ariel", 15),
    command=choose_translation_indices,
    highlightthickness=0,
)
reset_button.grid(row=0, column=2, sticky="e", pady=20)


# -------------------------- INITIALIZE GLOBALS -----------------------#
word_index = 0
CUR_TRANSLATION = {}
LANGUAGE_FOREIGN, foreign_path, LANGUAGE_NATIVE = languages()

TRANSLATIONS = pd.read_csv(foreign_path)

if TRANSLATION_INDICES_PATH.exists():
    try:
        with TRANSLATION_INDICES_PATH.open() as f:
            TRANSLATION_INDICES = json.load(f)
    except:
        choose_translation_indices()
else:
    choose_translation_indices()


# -------------------------------- RUN THE PROGRAM -----------------------#
if __name__ == "__main__":
    try:
        window.mainloop()
    except Exception as ex:
        print(ex)
    finally:
        # when the user closes the form, save all settings to file
        with TRANSLATION_INDICES_PATH.open("w") as f:
            json.dump(TRANSLATION_INDICES, f)
        with SETTINGS_PATH.open("w") as f:
            json.dump(SETTINGS, f, indent=4)
