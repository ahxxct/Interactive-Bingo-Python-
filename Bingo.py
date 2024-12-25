import tkinter as tk
from tkinter import messagebox
import random



def create_board(size):
    """Creates a game board of given size with unique random numbers."""
    numbers = list(range(1, size * size + 1))
    random.shuffle(numbers)
    return [numbers[i:i+size] for i in range(0, len(numbers), size)]

def mark_board(board, number):
    """Marks the given number on the board by replacing it with 'X'."""
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == number:
                board[i][j] = 'X'
                return True
    return False

def count_bingos(board):
    """Counts the number of completed rows, columns, and diagonals."""
    size = len(board)
    count = 0

    # Check rows
    for row in board:
        if all(cell == 'X' for cell in row):
            count += 1

    # Check columns
    for col in range(size):
        if all(board[row][col] == 'X' for row in range(size)):
            count += 1

    # Check diagonals
    if all(board[i][i] == 'X' for i in range(size)):
        count += 1
    if all(board[i][size - i - 1] == 'X' for i in range(size)):
        count += 1

    return count

def get_computer_move(board, valid_numbers, level):
    """Determines the computer's move based on the difficulty level."""
    size = len(board)

    if level == "easy":
        # Random move
        return random.choice(list(valid_numbers))

    elif level == "medium":
        # Try to complete a row, column, or diagonal
        for i in range(size):
            row = [board[i][j] for j in range(size)]
            if row.count('X') == size - 1:
                for num in row:
                    if num in valid_numbers:
                        return num

            col = [board[j][i] for j in range(size)]
            if col.count('X') == size - 1:
                for num in col:
                    if num in valid_numbers:
                        return num

        main_diag = [board[i][i] for i in range(size)]
        if main_diag.count('X') == size - 1:
            for num in main_diag:
                if num in valid_numbers:
                    return num

        anti_diag = [board[i][size - i - 1] for i in range(size)]
        if anti_diag.count('X') == size - 1:
            for num in anti_diag:
                if num in valid_numbers:
                    return num

        # Otherwise, random move
        return random.choice(list(valid_numbers))

    elif level == "hard":
        # Try to block the user from winning
        for i in range(size):
            row = [board[i][j] for j in range(size)]
            if row.count('X') == size - 1:
                for num in row:
                    if num in valid_numbers:
                        return num

            col = [board[j][i] for j in range(size)]
            if col.count('X') == size - 1:
                for num in col:
                    if num in valid_numbers:
                        return num

        main_diag = [board[i][i] for i in range(size)]
        if main_diag.count('X') == size - 1:
            for num in main_diag:
                if num in valid_numbers:
                    return num

        anti_diag = [board[i][size - i - 1] for i in range(size)]
        if anti_diag.count('X') == size - 1:
            for num in anti_diag:
                if num in valid_numbers:
                    return num

        # Otherwise, make a random move
        return random.choice(list(valid_numbers))

def update_gui_board(frame, board):
    """Updates the GUI board with the current state of the game board."""
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            widget = frame.grid_slaves(row=i, column=j)[0]
            if cell == 'X':
                widget.config(text='X', fg='red')  # Set 'X' color to red
            else:
                widget.config(text=str(cell), fg='black')

def save_game_to_file(player_name, user_board, comp_board, valid_numbers, user_bingos, comp_bingos, computer_level):
    """Saves the current game state to a text file."""
    with open(f"{player_name}_save.txt", "w") as file:
        file.write(f"{len(user_board)}\n")  # Save board size
        for row in user_board:
            file.write(" ".join(map(lambda x: str(x) if x != 'X' else 'X', row)) + "\n")
        file.write("#\n")
        for row in comp_board:
            file.write(" ".join(map(lambda x: str(x) if x != 'X' else 'X', row)) + "\n")
        file.write("#\n")
        file.write(" ".join(map(str, valid_numbers)) + "\n")
        file.write(f"{user_bingos[0]}\n")
        file.write(f"{comp_bingos[0]}\n")
        file.write(f"{computer_level}\n")

def load_game_from_file(player_name):
    """Loads the game state from a text file."""
    try:
        with open(f"{player_name}_save.txt", "r") as file:
            lines = file.readlines()
            if not lines:  # Check if the file is empty
                return None
    except FileNotFoundError:
        return None

    size = int(lines[0].strip())
    user_board = []
    comp_board = []
    valid_numbers = set()
    user_bingos = [0]
    comp_bingos = [0]
    computer_level = "easy"

    idx = 1
    while lines[idx].strip() != "#":
        user_board.append(list(map(lambda x: int(x) if x != 'X' else 'X', lines[idx].strip().split())))
        idx += 1
    idx += 1

    while lines[idx].strip() != "#":
        comp_board.append(list(map(lambda x: int(x) if x != 'X' else 'X', lines[idx].strip().split())))
        idx += 1
    idx += 1

    valid_numbers = set(map(int, lines[idx].strip().split()))
    idx += 1

    user_bingos[0] = int(lines[idx].strip())
    idx += 1

    comp_bingos[0] = int(lines[idx].strip())
    idx += 1

    computer_level = lines[idx].strip()

    return size, user_board, comp_board, valid_numbers, user_bingos, comp_bingos, computer_level

def delete_saved_game(player_name):
    """Resets the saved game file for the given player name by overwriting it."""
    try:
        with open(f"{player_name}_save.txt", "w") as file:
            file.write("")  # Write an empty string to reset the file
    except FileNotFoundError:
        pass

def handle_escape(root, player_name, user_board, comp_board, valid_numbers, user_bingos, comp_bingos, computer_level):
    """Handles the ESC key to save, exit, or continue the game."""
    response = messagebox.askyesnocancel("Pause Game", "Do you want to save and exit the game? Yes to save, No to exit, Cancel to continue.")
    if response is None:
        return  # Continue the game
    elif response:
        save_game_to_file(player_name, user_board, comp_board, valid_numbers, user_bingos, comp_bingos, computer_level)
        root.destroy()
    else:
        root.destroy()

def declare_winner(user_bingos, comp_bingos, root, player_name):
    """Displays the winner and terminates the game."""
    if user_bingos >= 5:
        delete_saved_game(player_name)  # Delete the saved game after wining
        messagebox.showinfo("Game Over", f"Congratulations! {player_name} is the winner!")
    elif comp_bingos >= 5:
        messagebox.showinfo("Game Over", "Computer is the winner!")
    root.destroy()

def user_turn(number, user_board, comp_board, valid_numbers, user_score_label, comp_score_label, gui_user_board, gui_comp_board, user_bingos, comp_bingos, root, player_name, computer_level):
    """Handles the user's turn."""
    if number not in valid_numbers:
        messagebox.showerror("Invalid Input", "Please enter a valid number!")
        return

    valid_numbers.remove(number)
    mark_board(user_board, number)
    mark_board(comp_board, number)

    update_gui_board(gui_user_board, user_board)
    update_gui_board(gui_comp_board, comp_board)

    user_bingos[0] = count_bingos(user_board)
    comp_bingos[0] = count_bingos(comp_board)

    user_score_label.config(text=f"Your Score: {' '.join('BINGO'[:user_bingos[0]])}")
    comp_score_label.config(text=f"Computer's Score: {' '.join('BINGO'[:comp_bingos[0]])}")

    if user_bingos[0] >= 5 or comp_bingos[0] >= 5:
        declare_winner(user_bingos[0], comp_bingos[0], root, player_name)
        return

    # Computer's turn
    comp_number = get_computer_move(comp_board, valid_numbers, computer_level)
    valid_numbers.remove(comp_number)
    messagebox.showinfo("Computer's Turn", f"Computer chose: {comp_number}")
    mark_board(user_board, comp_number)
    mark_board(comp_board, comp_number)

    update_gui_board(gui_user_board, user_board)
    update_gui_board(gui_comp_board, comp_board)

    user_bingos[0] = count_bingos(user_board)
    comp_bingos[0] = count_bingos(comp_board)

    user_score_label.config(text=f"Your Score: {' '.join('BINGO'[:user_bingos[0]])}")
    comp_score_label.config(text=f"Computer's Score: {' '.join('BINGO'[:comp_bingos[0]])}")

    if user_bingos[0] >= 5 or comp_bingos[0] >= 5:
        declare_winner(user_bingos[0], comp_bingos[0], root, player_name)
        return

def play_game():
    """Main function to play the Bingo game with GUI."""
    root = tk.Tk()
    root.title("Bingo Game")

    # Player setup with input validation
    while True:
        player_name = input("Enter your name: ").strip()
        if player_name:
            break
        print("Invalid input, try again.")

    game_data = load_game_from_file(player_name)

    if game_data:
        while True:
            load_game = input("A saved game exists. Do you want to load it? (yes/no): ").strip().lower()
            if load_game in {"yes", "no"}:
                break
            print("Invalid input, try again.")

        if load_game == "yes":
            size, user_board, comp_board, valid_numbers, user_bingos, comp_bingos, computer_level = game_data
        else:
            while True:
                try:
                    size = int(input("Enter board size (e.g., 5 for 5x5): ").strip())
                    if size >= 3:
                        break
                    else:
                        print("Invalid input, try again.")
                except ValueError:
                    print("Invalid input, try again.")

            while True:
                computer_level = input("Choose computer difficulty (easy, medium, hard): ").strip().lower()
                if computer_level in {"easy", "medium", "hard"}:
                    break
                print("Invalid input, try again.")

            user_board = create_board(size)
            comp_board = create_board(size)
            valid_numbers = set(range(1, size * size + 1))
            user_bingos = [0]
            comp_bingos = [0]
    else:
        print(f"No saved game found for {player_name}. Starting a new game.")

        while True:
            try:
                size = int(input("Enter board size (e.g., 5 for 5x5): ").strip())
                if size >= 3:
                    break
                else:
                    print("Invalid input, try again.")
            except ValueError:
                print("Invalid input, try again.")

        while True:
            computer_level = input("Choose computer difficulty (easy, medium, hard): ").strip().lower()
            if computer_level in {"easy", "medium", "hard"}:
                break
            print("Invalid input, try again.")

        user_board = create_board(size)
        comp_board = create_board(size)
        valid_numbers = set(range(1, size * size + 1))
        user_bingos = [0]
        comp_bingos = [0]

    # GUI setup
    user_frame = tk.LabelFrame(root, text=f"{player_name}'s Board", padx=10, pady=10)
    user_frame.grid(row=0, column=0, padx=20, pady=20)

    comp_frame = tk.LabelFrame(root, text="Computer's Board", padx=10, pady=10)
    comp_frame.grid(row=0, column=1, padx=20, pady=20)

    gui_user_board = tk.Frame(user_frame)
    gui_user_board.pack()

    gui_comp_board = tk.Frame(comp_frame)
    gui_comp_board.pack()

    for i in range(size):
        for j in range(size):
            user_cell = tk.Label(gui_user_board, text=str(user_board[i][j]), width=5, height=2, relief="solid")
            user_cell.grid(row=i, column=j, padx=5, pady=5)

            comp_cell = tk.Label(gui_comp_board, text=str(comp_board[i][j]), width=5, height=2, relief="solid")
            comp_cell.grid(row=i, column=j, padx=5, pady=5)

    user_score_label = tk.Label(root, text="Your Score: ")
    user_score_label.grid(row=1, column=0, pady=10)

    comp_score_label = tk.Label(root, text="Computer's Score: ")
    comp_score_label.grid(row=1, column=1, pady=10)

    input_frame = tk.Frame(root)
    input_frame.grid(row=2, column=0, columnspan=2, pady=20)

    tk.Label(input_frame, text="Enter a number: ").grid(row=0, column=0)
    number_entry = tk.Entry(input_frame)
    number_entry.grid(row=0, column=1)

    tk.Button(input_frame, text="Submit", command=lambda: user_turn(
        int(number_entry.get()), user_board, comp_board, valid_numbers,
        user_score_label, comp_score_label, gui_user_board, gui_comp_board,
        user_bingos, comp_bingos, root, player_name, computer_level
    )).grid(row=0, column=2)

    root.bind("<Escape>", lambda e: handle_escape(
        root, player_name, user_board, comp_board, valid_numbers,
        user_bingos, comp_bingos, computer_level
    ))

    root.mainloop()


if __name__ == "__main__":
    play_game()
