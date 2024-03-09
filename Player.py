import numpy as np

class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = f'Player {player_number}:ai'

    def get_alpha_beta_move(self, board):
        alpha = float('-inf')
        beta = float('inf')
        best_move = None
        max_depth = 4

        for col in range(board.shape[1]):
            if board[0, col] == 0:
                temp_board = board.copy()
                row = self.get_next_empty_row(temp_board, col)
                temp_board[row, col] = self.player_number
                value = self.minimax(temp_board, alpha, beta, max_depth, False)

                if value > alpha:
                    alpha = value
                    best_move = col

        return best_move

    def minimax(self, board, alpha, beta, depth, is_maximizing_player):
        if depth == 0 or self.game_completed(board):
            return self.evaluation_value(board)

        if is_maximizing_player:
            value = float('-inf')
            for col in range(board.shape[1]):
                if board[0, col] == 0:
                    temp_board = board.copy()
                    row = self.get_next_empty_row(temp_board, col)
                    temp_board[row, col] = self.player_number
                    value = max(value, self.minimax(temp_board, alpha, beta, depth - 1, False))
                    alpha = max(alpha, value)
                    if alpha >= beta:
                        break
            return value
        else:
            value = float('inf')
            for col in range(board.shape[1]):
                if board[0, col] == 0:
                    temp_board = board.copy()
                    row = self.get_next_empty_row(temp_board, col)
                    temp_board[row, col] = 3 - self.player_number
                    value = min(value, self.minimax(temp_board, alpha, beta, depth - 1, True))
                    beta = min(beta, value)
                    if beta <= alpha:
                        break
            return value

    def get_expectimax_move(self, board):
        max_depth = 6
        _, best_move = self.expectimax(board, max_depth, True)
        return best_move

    def expectimax(self, board, depth, is_maximizing_player):
        if depth == 0 or self.game_completed(board):
            return self.evaluation_value(board), None

        if is_maximizing_player:
            max_value = float('-inf')
            best_move = None

            for col in range(board.shape[1]):
                if board[0, col] == 0:
                    temp_board = board.copy()
                    row = self.get_next_empty_row(temp_board, col)
                    temp_board[row, col] = self.player_number
                    value, _ = self.expectimax(temp_board, depth - 1, False)

                    if value > max_value:
                        max_value = value
                        best_move = col

            return max_value, best_move
        else:
            total_value = 0
            valid_moves = [col for col in range(board.shape[1]) if board[0, col] == 0]
            num_moves = len(valid_moves)

            for col in valid_moves:
                temp_board = board.copy()
                row = self.get_next_empty_row(temp_board, col)
                temp_board[row, col] = 3 - self.player_number  # Opponent's move
                value, _ = self.expectimax(temp_board, depth - 1, True)
                total_value += value

            average_value = total_value / num_moves
            return average_value, None

    def evaluation_value(self, board):
        # Heuristic Evaluation Function
        player_num = self.player_number
        opponent_num = 3 - player_num
        score = 0

        # Evaluate horizontal connections
        for row in range(board.shape[0]):
            for col in range(board.shape[1] - 3):
                window = board[row, col:col+4]
                score += self.evaluate_window(window, player_num, opponent_num)

        # Evaluate vertical connections
        for col in range(board.shape[1]):
            for row in range(board.shape[0] - 3):
                window = board[row:row+4, col]
                score += self.evaluate_window(window, player_num, opponent_num)

        # Evaluate diagonal connections (positive slope)
        for row in range(board.shape[0] - 3):
            for col in range(board.shape[1] - 3):
                window = [board[row+i, col+i] for i in range(4)]
                score += self.evaluate_window(window, player_num, opponent_num)

        # Evaluate diagonal connections (negative slope)
        for row in range(3, board.shape[0]):
            for col in range(board.shape[1] - 3):
                window = [board[row-i, col+i] for i in range(4)]
                score += self.evaluate_window(window, player_num, opponent_num)

        return score

    def evaluate_window(self, window, player_num, opponent_num):
        if np.count_nonzero(window == player_num) == 4:
            return 1000
        elif np.count_nonzero(window == player_num) == 3 and np.count_nonzero(window == 0) == 1:
            return 100
        elif np.count_nonzero(window == player_num) == 2 and np.count_nonzero(window == 0) == 2:
            return 10
        elif np.count_nonzero(window == opponent_num) == 3 and np.count_nonzero(window == 0) == 1:
            return -100
        elif np.count_nonzero(window == opponent_num) == 2 and np.count_nonzero(window == 0) == 2:
            return -10
        else:
            return 0

    def get_next_empty_row(self, board, col):
        for row in range(board.shape[0] - 1, -1, -1):
            if board[row, col] == 0:
                return row
        return None

    def game_completed(self, board):
        # Check for a win in rows
        for row in range(board.shape[0]):
            for col in range(board.shape[1] - 3):
                if board[row, col] == board[row, col + 1] == board[row, col + 2] == board[row, col + 3] != 0:
                    return True

        # Check for a win in columns
        for col in range(board.shape[1]):
            for row in range(board.shape[0] - 3):
                if board[row, col] == board[row + 1, col] == board[row + 2, col] == board[row + 3, col] != 0:
                    return True

        # Check for a win in diagonals (positive slope)
        for row in range(board.shape[0] - 3):
            for col in range(board.shape[1] - 3):
                if board[row, col] == board[row + 1, col + 1] == board[row + 2, col + 2] == board[row + 3, col + 3] != 0:
                    return True

        # Check for a win in diagonals (negative slope)
        for row in range(3, board.shape[0]):
            for col in range(board.shape[1] - 3):
                if board[row, col] == board[row - 1, col + 1] == board[row - 2, col + 2] == board[row - 3, col + 3] != 0:
                    return True

        # Check for a tie (board full)
        if np.count_nonzero(board == 0) == 0:
            return True

        return False

class RandomPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'random'
        self.player_string = f'Player {player_number}:random'

    def get_move(self, board):
        return np.random.choice([col for col in range(board.shape[1]) if board[0, col] == 0])

class HumanPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'human'
        self.player_string = f'Player {player_number}:human'

    def get_move(self, board):
        print("Human player's turn:")
        while True:
            try:
                move = int(input("Enter column number (0-6): "))
                if move < 0 or move > 6 or board[0, move] != 0:
                    raise ValueError
                break
            except ValueError:
                print("Invalid input! Please enter a valid column number.")
        return move
