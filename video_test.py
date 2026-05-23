import tkinter as tk
import random
import winsound
from PIL import Image, ImageTk
from tkinter import *
from tkvideo import tkvideo

# ------------------ Load Words ------------------
def load_words():
    words = {}
    current_category = None
    category_order = ["fruits", "vegetables", "countries"]
    index = 0

    with open("words.txt", "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line:
                current_category = None
                continue

            if current_category is None:
                if index < len(category_order):
                    current_category = category_order[index]
                    words[current_category] = []
                    index += 1

            words[current_category].append(line.lower())

    return words


word_data = load_words()


# ------------------ Main App ------------------
class HangmanApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Hangman Game")
        self.root.geometry("600x400")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(
            root,
            width=600,
            height=400,
            highlightthickness=0
        )

        self.canvas.pack(fill="both", expand=True)

        self.current_word = ""
        self.guessed_letters = []
        self.attempts = 6
        self.score = 0

        self.show_welcome()

    # ------------------ Background ------------------
    def set_background(self, image_name):

        self.bg_image = Image.open(image_name)
        self.bg_image = self.bg_image.resize((600, 400))

        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        self.canvas.delete("all")

        self.canvas.create_image(
            0,
            0,
            image=self.bg_photo,
            anchor="nw"
        )

    # ------------------ Clear Widgets ------------------
    def clear_widgets(self):

        if hasattr(self, "video_label"):
           self.video_label.destroy()

        for widget in self.root.winfo_children():
           if widget != self.canvas:
              widget.destroy()

        self.canvas.delete("all")

    # ------------------ Welcome ------------------
    def show_welcome(self):

        self.clear_widgets()

        # Video Background
        self.video_label = Label(self.root)
        self.video_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.player = tkvideo(
            "first_1.mp4",
            self.video_label,
            loop=1,
            size=(600, 400)
        )

        self.player.play()

        winsound.PlaySound(
            "welcome.wav",
            winsound.SND_ASYNC | winsound.SND_LOOP
        )

        # Canvas Above Video
        self.canvas.place(x=0, y=0)
        self.canvas.config(highlightthickness=0) 
        self.canvas.create_text(
            300,
            120,
            text="MADE BY SHAILY DADRIWAL\n\nWelcome to Hangman",
            font=("Arial", 25, "bold"),
            fill="white",
            justify="center"
        )

        start_btn = tk.Button(
            self.root,
            text="Start Game",
            font=("Arial", 18),
            bg="green",
            fg="white",
            command=self.show_category
        )

        self.canvas.create_window(
            300,
            230,
            window=start_btn
        )

    # ------------------ Category ------------------
    def show_category(self):
         
        winsound.PlaySound(None, winsound.SND_PURGE)
 
        self.clear_widgets()

        self.set_background("second.jpg")

        self.canvas.create_text(
            300,
            80,
            text="Select Category",
            font=("Arial", 25, "bold"),
            fill="white"
        )

        y = 150

        for category in word_data.keys():

            btn = tk.Button(
                self.root,
                text=category.capitalize(),
                font=("Arial", 15),
                bg="#33b5ff",
                fg="white",
                width=15,
                command=lambda c=category: self.start_game(c)
            )

            self.canvas.create_window(300, y, window=btn)

            y += 50

    # ------------------ Start Game ------------------
    def start_game(self, category):

        self.current_word = random.choice(word_data[category])

        self.guessed_letters = []

        self.attempts = 6

        self.show_game()

    # ------------------ Game Screen ------------------
    def show_game(self):

        self.clear_widgets()

        self.set_background("third.jpg")

        self.word_text = self.canvas.create_text(
            300,
            70,
            text=self.display_word(),
            font=("Arial", 24),
            fill="white"
        )

        self.info_text = self.canvas.create_text(
            300,
            110,
            text=f"Attempts Left: {self.attempts}",
            font=("Arial", 18, "bold"),
            fill="purple"
        )

        self.buttons = {}

        x, y = 50, 180

        for i, letter in enumerate("abcdefghijklmnopqrstuvwxyz"):

            btn = tk.Button(
                self.root,
                text=letter.upper(),
                width=3,
                bg="#8c7ae6",
                fg="white",
                command=lambda l=letter: self.guess(l)
            )

            self.canvas.create_window(x, y, window=btn)

            self.buttons[letter] = btn

            x += 50

            if (i + 1) % 9 == 0:
                x = 50
                y += 40

    # ------------------ Display Word ------------------
    def display_word(self):

        return " ".join([
            l if l in self.guessed_letters else "_"
            for l in self.current_word
        ])

    # ------------------ Guess ------------------
    def guess(self, letter):

        if letter in self.guessed_letters:
            return

        self.guessed_letters.append(letter)

        self.buttons[letter].config(state="disabled")

        if letter not in self.current_word:

            self.attempts -= 1

            winsound.PlaySound(
                "no.wav",
                winsound.SND_ASYNC
            )

        else:

            winsound.PlaySound(
                "yes.wav",
                winsound.SND_ASYNC
            )

        self.canvas.itemconfig(
            self.word_text,
            text=self.display_word()
        )

        self.canvas.itemconfig(
            self.info_text,
            text=f"Attempts Left: {self.attempts}"
        )

        if all(l in self.guessed_letters for l in self.current_word):

            self.show_result(True)

        elif self.attempts <= 0:

            self.show_result(False)

    # ------------------ Result ------------------
    def show_result(self, win):

        self.clear_widgets()

        self.set_background("fourth.jpg")

        if win:

            self.score += 10

            winsound.PlaySound(
                "winner.wav",
                winsound.SND_ASYNC
            )

        else:

            winsound.PlaySound(
                "losser.wav",
                winsound.SND_ASYNC
            )

        result_text = "You Won!" if win else "You Lost!"

        color = "skyblue" if win else "red"

        self.canvas.create_text(
            300,
            100,
            text=result_text,
            font=("Arial", 24, "bold"),
            fill=color
        )

        self.canvas.create_text(
            300,
            150,
            text=f"Word was: {self.current_word}",
            font=("Arial", 20, "bold"),
            fill="white"
        )

        score_btn = tk.Button(
            self.root,
            text="Score",
            bg="#fbc531",
            command=self.show_score
        )

        self.canvas.create_window(
            300,
            220,
            window=score_btn
        )

        again_btn = tk.Button(
            self.root,
            text="Play Again",
            bg="green",
            fg="black",
            command=self.show_category
        )

        self.canvas.create_window(
            300,
            270,
            window=again_btn
        )

        quit_btn = tk.Button(
            self.root,
            text="Quit",
            bg="red",
            fg="white",
            command=self.root.destroy
        )

        self.canvas.create_window(
            300,
            320,
            window=quit_btn
        )

    # ------------------ Score ------------------
    def show_score(self):

        self.clear_widgets()

        self.set_background("fourth.jpg")

        self.canvas.create_text(
            300,
            150,
            text=f"Score: {self.score}",
            font=("Arial", 26, "bold"),
            fill="white"
        )

        again_btn = tk.Button(
            self.root,
            text="Play Again",
            command=self.show_category
        )

        self.canvas.create_window(
            300,
            230,
            window=again_btn
        )


# ------------------ Run ------------------
root = tk.Tk()

app = HangmanApp(root)

root.mainloop()