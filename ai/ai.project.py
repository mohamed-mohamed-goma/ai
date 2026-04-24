import tkinter as tk
from tkinter import messagebox
import random



class NumberPickingGame:
    def __init__(self):
        self.reset()

    def reset(self):
        self.numbers = list(range(1,10 ))
        self.available = self.numbers.copy()
        self.human_choices = []
        self.ai_choices = []
        self.move_count = 0

    def check_win(self, choices):
        return len(choices) == 3 and sum(choices) == 15

    def ai_move(self):
      
        for n in self.available:
            if self.check_win((self.ai_choices + [n])[-3:]):
                return n

        
        for n in self.available:
            if self.check_win((self.human_choices + [n])[-3:]):
                return n

    
        return random.choice(self.available)

    def make_move(self, player, num):
        self.available.remove(num)
        self.move_count += 1

        if player == "Human":
            self.human_choices.append(num)
            if len(self.human_choices) > 3:
                removed = self.human_choices.pop(0)
                self.available.append(removed)
        else:
            self.ai_choices.append(num)
            if len(self.ai_choices) > 3:
                removed = self.ai_choices.pop(0)
                self.available.append(removed)




class NumberPickingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Number Picking Game")

        self.game = NumberPickingGame()
        self.buttons = {}

      
        self.human_score = 0
        self.ai_score = 0

        self.create_interface()

    def create_interface(self):
        tk.Label(self.root, text="Pick numbers (ONLY 3 active - Sum 15 wins)",
                 font=("Arial", 14)).grid(row=0, column=0, columnspan=3, pady=10)

   
        for i, num in enumerate(range(1, 10)):
            btn = tk.Button(self.root, text=str(num), font=("Arial", 18),
                            width=5, height=2,
                            command=lambda n=num: self.player_choice(n))
            btn.grid(row=(i // 3) + 1, column=i % 3, padx=5, pady=5)
            self.buttons[num] = btn

        self.status_label = tk.Label(self.root, text="Your turn",
                                     font=("Arial", 12), fg="blue")
        self.status_label.grid(row=5, column=0, columnspan=3)

      
        self.score_label = tk.Label(self.root,
                                   text="You: 0  |  AI: 0",
                                   font=("Arial", 12))
        self.score_label.grid(row=6, column=0, columnspan=3, pady=5)

       
        tk.Button(self.root, text="Restart Match",
                  command=self.restart_match,
                  bg="lightgreen").grid(row=7, column=0, columnspan=3, pady=10)


    def update_buttons(self):
        for num, btn in self.buttons.items():
            if num in self.game.available:
                btn.config(state="normal", bg="SystemButtonFace")
            elif num in self.game.human_choices:
                btn.config(state="disabled", bg="lightblue")
            elif num in self.game.ai_choices:
                btn.config(state="disabled", bg="lightcoral")

    def disable_buttons(self):
        for num in self.game.available:
            self.buttons[num].config(state="disabled")

    def enable_buttons(self):
        for num in self.game.available:
            self.buttons[num].config(state="normal")

  

    def player_choice(self, number):
        if number not in self.game.available:
            return

        self.game.make_move("Human", number)
        self.update_buttons()

        if self.game.check_win(self.game.human_choices):
            self.end_round("You win this round! 🎉")
            return

        if self.game.move_count >= 12:
            self.end_round("Round Draw!")
            return

        self.disable_buttons()
        self.status_label.config(text="AI is thinking...")

        self.root.after(700, self.ai_turn)

    def ai_turn(self):
        ai_choice = self.game.ai_move()
        self.game.make_move("AI", ai_choice)
        self.update_buttons()

        if self.game.check_win(self.game.ai_choices):
            self.end_round("AI wins this round! 🤖")
            return

        if self.game.move_count >= 12:
            self.end_round("Round Draw!")
            return

        self.enable_buttons()
        self.status_label.config(text="Your turn")

 

    def end_round(self, message):
        self.disable_buttons()

        if "You win" in message:
            self.human_score += 1
        elif "AI wins" in message:
            self.ai_score += 1

        self.update_score()

     
        if self.human_score == 2:
            messagebox.showinfo("Match Over", "🏆 You won the match!")
            self.restart_match()
            return
        elif self.ai_score == 2:
            messagebox.showinfo("Match Over", "🤖 AI won the match!")
            self.restart_match()
            return

        messagebox.showinfo("Round Over", message)
        self.start_new_round()

    def start_new_round(self):
        self.game.reset()
        self.update_buttons()
        self.status_label.config(text="Your turn")

    def update_score(self):
        self.score_label.config(
            text=f"You: {self.human_score}  |  AI: {self.ai_score}"
        )


    def restart_match(self):
        if messagebox.askyesno("Restart", "Restart full match?"):
            self.human_score = 0
            self.ai_score = 0
            self.update_score()
            self.start_new_round()




if __name__ == "__main__":
    root = tk.Tk()
    app = NumberPickingGUI(root)
    root.mainloop()