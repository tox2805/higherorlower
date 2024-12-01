import tkinter as tk
from tkinter import messagebox
import random
import os
from PIL import Image, ImageTk
from tkinter.font import Font


class HigherLowerGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Higher or Lower Card Game")
        self.root.geometry("800x600")
        self.root.configure(bg="#1A1A1A")

        self.deck = self.create_deck()
        self.current_card = None
        self.next_card = None
        self.card_images = {}
        self.timeline_images = []
        self.score = 0
        self.streak = 0

        # Shuffle the deck
        random.shuffle(self.deck)

        # Load cardback image
        self.cardback_image = self.get_card_image("cardback")

        self.create_banner()

        # Displaying Hawkeye logo
        logo_path = os.path.join("cards", "logo.png")
        original_logo = Image.open(logo_path)
        scaled_width = 100 
        aspect_ratio = original_logo.height / original_logo.width
        scaled_height = int(scaled_width * aspect_ratio)
        self.logo_image = ImageTk.PhotoImage(original_logo.resize((scaled_width, scaled_height)))

        self.logo_label = tk.Label(
            self.root,
            image=self.logo_image,
            bg="#1A1A1A"
        )
        self.logo_label.pack(pady=5)

        # Setting up frames and labels for buttons
        self.center_frame = tk.Frame(root, bg="#1A1A1A")
        self.center_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.current_label = tk.Label(self.center_frame, text="Current Card", font=("Arial", 14), bg="#1A1A1A", fg="white")
        self.current_label.grid(row=0, column=0, pady=5, padx=20)

        self.next_label = tk.Label(self.center_frame, text="Next Card", font=("Arial", 14), bg="#1A1A1A", fg="white")
        self.next_label.grid(row=0, column=2, pady=5, padx=20)

        self.current_card_label = tk.Label(self.center_frame, bg="#1A1A1A")
        self.current_card_label.grid(row=1, column=0, padx=10, pady=10)

        self.next_card_label = tk.Label(self.center_frame, bg="#1A1A1A")
        self.next_card_label.grid(row=1, column=2, padx=10, pady=10)

        # Defing guess buttons
        self.button_frame = tk.Frame(self.center_frame, bg="#1A1A1A")
        self.button_frame.grid(row=2, column=0, columnspan=3, pady=10)

        self.higher_button = tk.Button(
            self.button_frame,
            text="Higher",
            font=("Arial", 14, "bold"),
            bg="#FF6600",
            fg="white",
            activebackground="#FF3300",
            activeforeground="white",
            command=lambda: self.make_guess("higher"),
        )
        self.higher_button.pack(side=tk.LEFT, padx=10)

        self.lower_button = tk.Button(
            self.button_frame,
            text="Lower",
            font=("Arial", 14, "bold"),
            bg="#FF6600",
            fg="white",
            activebackground="#FF3300",
            activeforeground="white",
            command=lambda: self.make_guess("lower"),
        )
        self.lower_button.pack(side=tk.LEFT, padx=10)

        # Score Tracker
        self.score_label = tk.Label(self.center_frame, text="Score: 0", font=("Arial", 14), bg="#1A1A1A", fg="white")
        self.score_label.grid(row=3, column=0, columnspan=3, pady=5)

        # Timeline Frame
        self.timeline_frame = tk.Frame(root, width=800, height=120, bg="#1A1A1A")
        self.timeline_frame.pack(side=tk.BOTTOM, pady=10)


        # Preallocate space for timeline images
        self.timeline_card_labels = [
            tk.Label(self.timeline_frame, bg="#1A1A1A") for _ in range(7)
        ]
        for label in self.timeline_card_labels:
            label.pack(side=tk.LEFT, padx=5)

        self.start_new_game()

    def create_banner(self):
        """Creates a banner with rounded edges"""
        banner_canvas = tk.Canvas(self.root, width=800, height=60, bg="#1A1A1A", highlightthickness=0)
        banner_canvas.pack(side=tk.TOP, pady=10)

        # I used an external tool to calculate the maths here for the rounded corners instead of importing a library (less dependancies)
        x1, y1, x2, y2 = 50, 5, 750, 55
        radius = 20
        banner_canvas.create_arc(x1, y1, x1 + 2 * radius, y1 + 2 * radius, start=90, extent=90, fill="#FF5733", outline="")
        banner_canvas.create_arc(x2 - 2 * radius, y1, x2, y1 + 2 * radius, start=0, extent=90, fill="#FF5733", outline="")
        banner_canvas.create_arc(x1, y2 - 2 * radius, x1 + 2 * radius, y2, start=180, extent=90, fill="#FF5733", outline="")
        banner_canvas.create_arc(x2 - 2 * radius, y2 - 2 * radius, x2, y2, start=270, extent=90, fill="#FF5733", outline="")

        banner_canvas.create_rectangle(x1 + radius, y1, x2 - radius, y2, fill="#FF5733", outline="")
        banner_canvas.create_rectangle(x1, y1 + radius, x2, y2 - radius, fill="#FF5733", outline="")

        banner_font = Font(family="Arial", size=16, weight="bold")
        banner_canvas.create_text(400, 30, text="Guess five cards in a row to win!", font=banner_font, fill="white")


    def create_deck(self):
        """Creates a standard 52-card deck."""
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        ranks = [
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",
            "Jack",
            "Queen",
            "King",
            "Ace",
        ]
        return [f"{rank}_of_{suit}" for suit in suits for rank in ranks]

    def get_card_image(self, card_name, half_size=False):
        """Load the image for the given card name."""
        image_path = os.path.join("cards", f"{card_name}.png")
        pil_image = Image.open(image_path)
        if half_size:
            resized_image = pil_image.resize((75, 100))
        else:
            resized_image = pil_image.resize((150, 200))
        image = ImageTk.PhotoImage(resized_image)

        # Cache the image for future use
        cache_key = card_name + ("_half" if half_size else "")
        self.card_images[cache_key] = image

        return image

    def start_new_game(self):
        """Starts a new game."""
        self.score = 0
        self.streak = 0
        self.deck = self.create_deck()
        random.shuffle(self.deck)
        self.timeline_images = []

        for label in self.timeline_card_labels:
            label.config(image="")

        self.update_score()

        # Show the first two cards
        self.current_card = self.deck.pop()
        self.next_card = self.deck.pop()
        self.update_gui()

    def update_gui(self, reveal_next_card=False):
        """Updates the GUI with the current card and next card."""
        self.current_card_label.config(image=self.get_card_image(self.current_card))
        if reveal_next_card:
            self.next_card_label.config(image=self.get_card_image(self.next_card))
        else:
            self.next_card_label.config(image=self.cardback_image)

    def update_score(self):
        """Updates the score display."""
        self.score_label.config(text=f"Score: {self.score}")

    def update_timeline(self):
        """Updates the timeline display."""
        for i, card_image in enumerate(self.timeline_images):
            self.timeline_card_labels[i].config(image=card_image)

    def make_guess(self, guess):
        """Handles the player's guess."""
        self.update_gui(reveal_next_card=True)

        # Determine rank order
        rank_order = {
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5,
            "6": 6,
            "7": 7,
            "8": 8,
            "9": 9,
            "10": 10,
            "Jack": 11,
            "Queen": 12,
            "King": 13,
            "Ace": 14,
        }

        current_rank = self.current_card.split("_of_")[0]
        next_rank = self.next_card.split("_of_")[0]

        is_higher = rank_order[next_rank] > rank_order[current_rank]

        if (guess == "higher" and is_higher) or (guess == "lower" and not is_higher):
            self.score += 1
            self.streak += 1
            self.timeline_images.append(self.get_card_image(self.next_card, half_size=True))

            if len(self.timeline_images) == 5:
                self.show_win_popup()
                return

            self.update_timeline()
            self.update_score()

            messagebox.showinfo("Correct!", f"Your guess was correct! Score: {self.score}")
        else:
            # Reset score, timeline, and streak
            self.score = 0
            self.streak = 0
            self.timeline_images = []
            self.update_timeline()
            self.update_score()

            messagebox.showerror("Wrong!", f"Your guess was wrong. Final Score: {self.score}")
            self.start_new_game()
            return

        self.root.after(100, self.prepare_next_round)

    def show_win_popup(self):
        """Displays a custom popup window when the player wins."""
        win_popup = tk.Toplevel(self.root)
        win_popup.title("Congratulations!")
        win_popup.geometry("400x200")
        win_popup.configure(bg="#FCF092")

        win_popup.transient(self.root)
        win_popup.grab_set()
        win_popup.update_idletasks()
        x = (self.root.winfo_screenwidth() - win_popup.winfo_reqwidth()) // 2
        y = (self.root.winfo_screenheight() - win_popup.winfo_reqheight()) // 2
        win_popup.geometry(f"+{x}+{y}")

        congrats_label = tk.Label(
            win_popup, 
            text="You Won!", 
            font=("Arial", 24, "bold"), 
            fg="#4CAF50",
            bg="#FCF092"
        )
        congrats_label.pack(pady=20)

        restart_button = tk.Button(
            win_popup,
            text="Play Again",
            font=("Arial", 14),
            command=lambda: [self.start_new_game(), win_popup.destroy()],
            bg="#4CAF50",
            fg="white",
            relief="raised",
            padx=10,
            pady=5,
        )
        restart_button.pack(pady=10)

        exit_button = tk.Button(
            win_popup,
            text="Exit",
            font=("Arial", 14),
            command=self.root.destroy,
            bg="red",
            fg="white",
            relief="raised",
            padx=10,
            pady=5,
        )
        exit_button.pack(pady=10)

    def prepare_next_round(self):
        """Updates the display and moves to the next card after the popup."""
        self.current_card = self.next_card
        if self.deck:
            self.next_card = self.deck.pop()
        else:
            messagebox.showinfo("Game Over", "You've gone through the entire deck!")
            self.start_new_game()
            return

        self.update_gui(reveal_next_card=False)

if __name__ == "__main__":
    root = tk.Tk()
    game = HigherLowerGame(root)
    root.mainloop()
