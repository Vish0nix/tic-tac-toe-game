import tkinter as tk
from tkinter import messagebox
import random

WIN_COMBOS = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6),
]


class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe Battle")
        self.root.configure(bg="#1e1e2f")
        self.root.resizable(False, False)

        self.human = "X"
        self.computer = "O"
        self.board = [""] * 9
        self.game_over = False
        self.computer_turn = False      # blocks clicks while computer "thinks"
        self.pending_job = None         # handle for the scheduled computer move

        tk.Label(
            root, text="⚔ TIC-TAC-TOE BATTLE ⚔",
            font=("Arial", 20, "bold"), bg="#1e1e2f", fg="#00e5ff"
        ).grid(row=0, column=0, columnspan=3, pady=15)

        self.buttons = []
        for i in range(9):
            btn = tk.Button(
                root, text="", font=("Arial", 28, "bold"),
                width=5, height=2, bg="#2d2d44", fg="white",
                activebackground="#454568", relief="flat",
                command=lambda idx=i: self.make_move(idx),
            )
            btn.grid(row=(i // 3) + 1, column=i % 3, padx=4, pady=4)
            self.buttons.append(btn)

        self.status = tk.Label(
            root, text="Your turn! You are X",
            font=("Arial", 13, "bold"), bg="#1e1e2f", fg="#ffffff"
        )
        self.status.grid(row=4, column=0, columnspan=3, pady=12)

        tk.Button(
            root, text="🔄 Restart Battle", font=("Arial", 12, "bold"),
            bg="#00b894", fg="white", command=self.restart_game
        ).grid(row=5, column=0, columnspan=3, sticky="ew", padx=10, pady=(0, 15))

    # ---------- helpers ----------
    def place(self, index, player, color):
        self.board[index] = player
        self.buttons[index].config(
            text=player, fg=color, disabledforeground=color, state="disabled"
        )

    def check_winner(self, board, player):
        return any(all(board[i] == player for i in combo) for combo in WIN_COMBOS)

    # ---------- game flow ----------
    def make_move(self, index):
        if self.game_over or self.computer_turn or self.board[index] != "":
            return

        self.place(index, self.human, "#00e5ff")

        if self.check_winner(self.board, self.human):
            self.finish_game("You win! 🏆")
            return
        if "" not in self.board:
            self.finish_game("It's a draw! 🤝")
            return

        self.computer_turn = True
        self.status.config(text="Computer is thinking...")
        self.pending_job = self.root.after(400, self.computer_move)

    def computer_move(self):
        self.pending_job = None
        if self.game_over:
            return

        available_moves = [i for i, cell in enumerate(self.board) if cell == ""]
        if not available_moves:
            self.finish_game("It's a draw! 🤝")
            return

        best_score = float("-inf")
        best_moves = []
        for i in available_moves:
            self.board[i] = self.computer
            score = self.minimax(self.board, 0, False)
            self.board[i] = ""
            if score > best_score:
                best_score, best_moves = score, [i]
            elif score == best_score:
                best_moves.append(i)

        if not best_moves:
            self.finish_game("It's a draw! 🤝")
            return

        self.place(random.choice(best_moves), self.computer, "#ff7675")
        self.computer_turn = False

        if self.check_winner(self.board, self.computer):
            self.finish_game("Computer wins! 🤖")
        elif "" not in self.board:
            self.finish_game("It's a draw! 🤝")
        else:
            self.status.config(text="Your turn! You are X")

    def minimax(self, board, depth, is_maximizing):
        if self.check_winner(board, self.computer):
            return 10 - depth
        if self.check_winner(board, self.human):
            return depth - 10
        if "" not in board:
            return 0

        if is_maximizing:
            best = float("-inf")
            for i in range(9):
                if board[i] == "":
                    board[i] = self.computer
                    best = max(best, self.minimax(board, depth + 1, False))
                    board[i] = ""
            return best

        best = float("inf")
        for i in range(9):
            if board[i] == "":
                board[i] = self.human
                best = min(best, self.minimax(board, depth + 1, True))
                board[i] = ""
        return best

    def finish_game(self, message):
        self.game_over = True
        self.computer_turn = False
        self.pending_job = None
        self.status.config(text=message)
        for btn in self.buttons:
            btn.config(state="disabled")
        messagebox.showinfo("Battle Over", message)

    def restart_game(self):
        if self.pending_job is not None:        # cancel any queued computer move
            self.root.after_cancel(self.pending_job)
            self.pending_job = None

        self.board = [""] * 9
        self.game_over = False
        self.computer_turn = False

        for btn in self.buttons:
            btn.config(text="", state="normal", bg="#2d2d44", fg="white")

        self.status.config(text="Your turn! You are X")


if __name__ == "__main__":
    root = tk.Tk()
    TicTacToe(root)
    root.mainloop()