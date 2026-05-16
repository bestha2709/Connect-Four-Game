import tkinter as tk
import random

ROWS = 6
COLS = 7
CELL_SIZE = 80

class ConnectFour:
    def __init__(self, root):
        self.root = root
        self.root.title("Connect Four")
        self.show_menu()

    # ---------------- MENU ----------------
    def show_menu(self):
        self.clear_screen()

        self.menu_frame = tk.Frame(self.root)
        self.menu_frame.pack()

        tk.Label(self.menu_frame, text="Connect Four", font=("Arial", 24)).pack(pady=20)

        tk.Button(self.menu_frame, text="Play with Friend", width=20,
                  command=self.start_pvp).pack(pady=10)

        tk.Button(self.menu_frame, text="Play with AI", width=20,
                  command=self.start_ai).pack(pady=10)

    # ---------------- START GAME ----------------
    def start_pvp(self):
        self.mode = "pvp"
        self.start_game()

    def start_ai(self):
        self.mode = "ai"
        self.start_game()

    def start_game(self):
        self.clear_screen()

        # Top buttons
        top_frame = tk.Frame(self.root)
        top_frame.pack()

        tk.Button(top_frame, text="Undo", command=self.undo_move).pack(side="left", padx=10)
        tk.Button(top_frame, text="Back to Menu", command=self.show_menu).pack(side="left", padx=10)

        # Canvas
        self.canvas = tk.Canvas(self.root, width=COLS*CELL_SIZE,
                                height=ROWS*CELL_SIZE, bg="blue")
        self.canvas.pack()

        self.board = [[None for _ in range(COLS)] for _ in range(ROWS)]
        self.current_player = "red"
        self.history = []  # store moves

        self.canvas.bind("<Button-1>", self.handle_click)
        self.draw_board()

    # ---------------- DRAW ----------------
    def draw_board(self):
        self.canvas.delete("all")

        for r in range(ROWS):
            for c in range(COLS):
                x1 = c * CELL_SIZE
                y1 = r * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE

                self.canvas.create_rectangle(x1, y1, x2, y2, fill="blue")

                color = self.board[r][c] if self.board[r][c] else "white"

                self.canvas.create_oval(x1+10, y1+10, x2-10, y2-10, fill=color)

    # ---------------- CLICK ----------------
    def handle_click(self, event):
        if self.mode == "ai" and self.current_player == "yellow":
            return

        col = int(event.x // CELL_SIZE)

        if col < 0 or col >= COLS:
            return

        row = self.get_row(col)
        if row is None:
            return

        self.place_piece(row, col, self.current_player)

        if self.check_winner(row, col):
            self.draw_board()
            self.canvas.unbind("<Button-1>")
            self.show_winner()
            return

        self.switch_player()
        self.draw_board()

        if self.mode == "ai" and self.current_player == "yellow":
            self.root.after(500, self.ai_move)

    # ---------------- PLACE ----------------
    def place_piece(self, row, col, player):
        self.board[row][col] = player
        self.history.append((row, col, player))

    # ---------------- AI ----------------
    def ai_move(self):
        available = [c for c in range(COLS) if self.get_row(c) is not None]
        if not available:
            return

        col = random.choice(available)
        row = self.get_row(col)

        self.place_piece(row, col, "yellow")

        if self.check_winner(row, col):
            self.draw_board()
            self.show_winner()
            self.canvas.unbind("<Button-1>")
            return

        self.switch_player()
        self.draw_board()

    # ---------------- UNDO ----------------
    def undo_move(self):
        if not self.history:
            return

        # In AI mode → undo 2 moves (player + AI)
        if self.mode == "ai" and len(self.history) >= 2:
            for _ in range(2):
                row, col, _ = self.history.pop()
                self.board[row][col] = None
        else:
            row, col, _ = self.history.pop()
            self.board[row][col] = None

        self.current_player = "red" if self.current_player == "yellow" else "yellow"
        self.draw_board()

    # ---------------- HELPERS ----------------
    def get_row(self, col):
        for r in range(ROWS-1, -1, -1):
            if self.board[r][col] is None:
                return r
        return None

    def switch_player(self):
        self.current_player = "yellow" if self.current_player == "red" else "red"

    def check_winner(self, row, col):
        color = self.board[row][col]

        def count(dx, dy):
            r, c = row + dy, col + dx
            cnt = 0
            while 0 <= r < ROWS and 0 <= c < COLS and self.board[r][c] == color:
                cnt += 1
                r += dy
                c += dx
            return cnt

        directions = [(1,0),(0,1),(1,1),(1,-1)]

        for dx, dy in directions:
            if 1 + count(dx, dy) + count(-dx, -dy) >= 4:
                return True
        return False

    def show_winner(self):
        winner = "Red" if self.current_player == "red" else "Yellow"

        self.canvas.create_text(
            COLS*CELL_SIZE//2,
            ROWS*CELL_SIZE//2,
            text=f"{winner} Wins!",
            fill="white",
            font=("Arial", 30, "bold")
        )

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()


# ---------------- RUN ----------------
root = tk.Tk()
game = ConnectFour(root)
root.mainloop()