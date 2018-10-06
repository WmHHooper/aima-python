from collections import namedtuple
from games import (Game)
from queue import PriorityQueue
from copy import deepcopy

class GameState:
    def __init__(self, to_move, board, label=None, depth=8):
        self.to_move = to_move
        self.board = board
        self.label = label
        self.maxDepth = depth

    def __str__(self):
        if self.label == None:
            return super(GameState, self).__str__()
        return self.label

class FlagrantCopy(Game):
    """A flagrant copy of Connect4, from game.py
    It's simplified, so that moves and utility are calculated as needed
    Play Connect4 on an h x v board, with Max (first player) playing 'R'.
    A state has the player to move and a board, in the form of
    a dict of {(x, y): Player} entries, where Player is 'R' or 'B'."""

    def __init__(self, h=4, v=4, k=4):
        self.h = h
        self.v = v
        self.k = k
        self.initial = GameState(to_move='R', board={})

    def actions(self, state):
        try:
            return state.moves
        except:
            pass
        moves = []
        for x in range(1, self.v + 1):
            for y in range(self.h, 0, -1):
                if (y, x) not in state.board.keys():
                    moves.append((y, x))
                    break
        state.moves = moves
        return moves

    # defines the order of play
    def opponent(self, player):
        if player == 'R':
            return 'B'
        if player == 'B':
            return 'R'
        return None

    def result(self, state, move):
        if move not in self.actions(state):
            return state  # Illegal move has no effect
        board = state.board.copy()
        player = state.to_move
        board[move] = player
        next_mover = self.opponent(player)
        return GameState(to_move=next_mover, board=board)

    def utility(self, state, player):
        "Return the value to player; 1 for win, -1 for loss, 0 otherwise."
        try:
            return state.utility if player == 'R' else -state.utility
        except:
            pass
        board = state.board
        util = self.check_win(board, 'R')
        if util == 0:
            util = -self.check_win(board, 'B')
        state.utility = util
        return util if player == 'R' else -util

    # Did I win?
    def check_win(self, board, player):
        # check rows
        for y in range(1, self.v + 1):
            if self.k_in_row(board, (1,y), player, (1,0)):
                return 1
        # check columns
        for x in range(1, self.h + 1):
            if self.k_in_row(board, (x,1), player, (0,1)):
                return 1
        # check \ diagonal
        if self.k_in_row(board, (1,1), player, (1,1)):
            return 1
        # check / diagonal
        if self.k_in_row(board, (3,1), player, (-1,1)):
            return 1
        return 0

    # does player have K in a row? return 1 if so, 0 if not
    def k_in_row(self, board, start, player, direction):
        "Return true if there is a line through start on board for player."
        (delta_x, delta_y) = direction
        x, y = start
        n = 0  # n is number of moves in row
        while board.get((x, y)) == player:
            n += 1
            x, y = x + delta_x, y + delta_y
        x, y = start
        while board.get((x, y)) == player:
            n += 1
            x, y = x - delta_x, y - delta_y
        n -= 1  # Because we counted start itself twice
        return n >= self.k

    def terminal_test(self, state):
        "A state is terminal if it is won or there are no empty squares."
        return self.utility(state, 'R') != 0 or len(self.actions(state)) == 0

    def display(self, state):
        board = state.board
        for x in range(1, self.h + 1):
            for y in range(1, self.v + 1):
                print(board.get((x, y), '_'), end=' ')
            print()


myGame = FlagrantCopy()

won = GameState(
    to_move = 'B',
    board = {(1,1): 'R', (2,1): 'R', (3,1): 'R', (4,1): 'R',
             (2,2): 'B', (3,2): 'B', (4,2): 'B',
            },
    label = 'won'
)

winin1 = GameState(
    to_move = 'R',
    board = {(2,1): 'R', (3,1): 'R', (4,1): 'R',
             (2,2): 'B', (3,2): 'B', (4,2): 'B',
            },
    label = 'winin1'
)

losein1 = GameState(
    to_move = 'B',
    board = {(4,1): 'R', (3,1): 'R', (2,1): 'R', (4,3): 'R',
             (2,2): 'B', (3,2): 'B', (4,2): 'B',
            },
    label = 'losein1'
)

winin3 = GameState(
    to_move = 'R',
    board = {(4,1): 'R', (3,1): 'R',
             (3,2): 'B', (4,2): 'B',
            },
    label = 'winin3'
)

losein3 = GameState(
    to_move = 'B',
    board = {(4,1): 'R', (4,3): 'R',
             (3,2): 'B', (4,2): 'B',
            },
    label = 'losein3'
)

winin5 = GameState(
    to_move = 'R',
    board = {(4,1): 'R', (3,1): 'R',
             (4,2): 'B',
            },
    label = 'winin5'
)

lost = GameState(
    to_move = 'R',
    board = {(4,1): 'R', (3,1): 'R', (2,1): 'R', (4,3): 'R',
             (4,2): 'B', (3,2): 'B', (2,2): 'B', (1,2): 'B',
            },
    label = 'lost'
)
#
# class TemplateState:    # one way to define the state of a minimal game.
#
#     def __init__(self, player): # add parameters as needed.
#         self.to_move = player
#         self.label = str(id(self))   # change this to something easier to read
#         # add code and self.variables as needed.
#
#     def __str__(self):  # use this exact signature
#         return self.label
#
# # class TemplateAction:
# #     '''
# #     It is not necessary to define an action.
# #     Start with actions as simple as a label (e.g., 'Down')
# #     or a pair of coordinates (e.g., (1,2)).
# #
# #     Don't un-comment this until you already have a working game,
# #     and want to play smarter.
# #     '''
# #     def __lt__(self, other):    # use this exact signature
# #         # return True when self is a better move than other.
# #         return False
#
# class TemplateGame(Game):
#     '''
#     This is a minimal Game definition,
#     the shortest implementation I could run without errors.
#     '''
#
#     def __init__(self, initial):    # add parameters if needed.
#         self.initial = initial
#         # add code and self.variables if needed.
#
#     def actions(self, state):   # use this exact signature.
#         acts = []
#         # append all moves, which are legal in this state,
#         # to the list of acts.
#         return acts
#
#     def result(self, state, move):   # use this exact signature.
#         newState = deepcopy(state)
#         # use the move to modify the newState
#         return newState
#
#     def terminal_test(self, state):   # use this exact signature.
#         # return True only when the state of the game is over.
#         return True
#
#     def utility(self, state, player):   # use this exact signature.
#         ''' return:
#         >0 if the player is winning,
#         <0 if the player is losing,
#          0 if the state is a tie.
#         '''
#         return 0
#
#     def display(self, state):   # use this exact signature.
#         # pretty-print the game state, using ASCII art,
#         # to help a human player understand his options.
#         print(state)
#
# tg = TemplateGame(TemplateState('A'))   # this is the game we play interactively.

myGames = {
    myGame: [
        won,
        winin1, losein1, winin3, losein3, winin5,
        lost,
    ],

    # tg: [
    #     # these are the states we tabulate when we test AB(1), AB(2), etc.
    #     TemplateState('B'),
    #     TemplateState('C'),
    # ]
}
