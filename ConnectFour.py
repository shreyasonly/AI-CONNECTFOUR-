import numpy as np
import tkinter as tk
import multiprocessing as mp
from Player import AIPlayer, RandomPlayer, HumanPlayer

class Game:
    def __init__(self, player1, player2, time_limit=5):
        self.players = [player1, player2]
        self.colors = ['yellow', 'red']
        self.current_turn = 0
        self.board = np.zeros([6, 7]).astype(np.uint8)
        self.gui_board = []
        self.game_over = False
        self.ai_turn_limit = time_limit

        root = tk.Tk()
        root.title('Connect 4')
        self.player_string = tk.Label(root, text=player1.player_string)
        self.player_string.pack()
        self.c = tk.Canvas(root, width=700, height=600)
        self.c.pack()

        for row in range(0, 700, 100):
            column = []
            for col in range(0, 700, 100):
                column.append(self.c.create_oval(row, col, row + 100, col + 100, fill=''))
            self.gui_board.append(column)

        tk.Button(root, text='Next Move', command=self.make_move).pack()

        root.mainloop()

    def make_move(self):
        if not self.game_over:
            current_player = self.players[self.current_turn]

            if current_player.type == 'ai':
                move_func = current_player.get_expectimax_move if self.players[int(not self.current_turn)].type == 'random' else current_player.get_alpha_beta_move
                try:
                    recv_end, send_end = mp.Pipe(False)
                    p = mp.Process(target=self.turn_worker, args=(self.board, send_end, move_func))
                    p.start()
                    if p.join(self.ai_turn_limit) is None and p.is_alive():
                        p.terminate()
                        raise Exception('Player Exceeded time limit')
                except Exception as e:
                    uh_oh = 'Uh oh.... something is wrong with Player {}'
                    print(uh_oh.format(current_player.player_number))
                    print(e)
                    raise Exception('Game Over')

                move = recv_end.recv()
            else:
                move = current_player.get_move(self.board)

            if move is not None:
                self.update_board(int(move), current_player.player_number)

            if self.game_completed(current_player.player_number):
                self.game_over = True
                self.player_string.configure(text=self.players[self.current_turn].player_string + ' wins!')
            else:
                self.current_turn = int(not self.current_turn)
                self.player_string.configure(text=self.players[self.current_turn].player_string)

    def update_board(self, move, player_num):
        if 0 in self.board[:, move]:
            update_row = -1
            for row in range(1, self.board.shape[0]):
                update_row = -1
                if self.board[row, move] > 0 and self.board[row - 1, move] == 0:
                    update_row = row - 1
                elif row == self.board.shape[0] - 1 and self.board[row, move] == 0:
                    update_row = row

                if update_row >= 0:
                    self.board[update_row, move] = player_num
                    self.c.itemconfig(self.gui_board[move][update_row],
                                      fill=self.colors[self.current_turn])
                    break
        else:
            err = 'Invalid move by player {}. Column {}'.format(player_num, move)
            raise Exception(err)

    def game_completed(self, player_num):
        player_win_str = '{0}{0}{0}{0}'.format(player_num)
        board = self.board
        to_str = lambda a: ''.join(a.astype(str))

        def check_horizontal(b):
            for row in b:
                if player_win_str in to_str(row):
                    return True
            return False

        def check_vertical(b):
            return check_horizontal(b.T)

        def check_diagonal(b):
            for op in [None, np.fliplr]:
                op_board = op(b) if op else b

                root_diag = np.diagonal(op_board, offset=0)
                if player_win_str in ''.join(map(str, root_diag)):
                    return True

                for i in range(1, b.shape[1] - 3):
                    for offset in [i, -i]:
                        diag = np.diagonal(op_board, offset=offset)
                        if player_win_str in ''.join(map(str, diag)):
                            return True

            return False

        return (check_horizontal(board) or
                check_vertical(board) or
                check_diagonal(board))

    @staticmethod
    def turn_worker(board, send_end, move_func):
        send_end.send(move_func(board))

if __name__ == "__main__":
    player1_type = input("Enter player 1 type (ai, random, human): ")
    player2_type = input("Enter player 2 type (ai, random, human): ")

    player1 = None
    player2 = None

    if player1_type == 'ai':
        player1 = AIPlayer(1)
    elif player1_type == 'random':
        player1 = RandomPlayer(1)
    elif player1_type == 'human':
        player1 = HumanPlayer(1)

    if player2_type == 'ai':
        player2 = AIPlayer(2)
    elif player2_type == 'random':
        player2 = RandomPlayer(2)
    elif player2_type == 'human':
        player2 = HumanPlayer(2)

    game = Game(player1, player2)
