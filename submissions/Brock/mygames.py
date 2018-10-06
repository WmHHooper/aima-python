from collections import namedtuple
from games import (Game)
from queue import PriorityQueue
from copy import deepcopy



# class GameState:
#     def __init__(self, to_move, board, label=None, depth=8):
#         self.to_move = to_move
#         self.board = board
#         self.label = label
#         self.maxDepth = depth
#
#     def __str__(self):
#         if self.label == None:
#             return super(GameState, self).__str__()
#         return self.label
class Board:
    def __init__(self, length, a_spots, b_spots, a_pool, b_pool):
        self.length = length
        self.a_spots = a_spots
        self.b_spots = b_spots
        self.a_pool = a_pool
        self.b_pool = b_pool

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

class Mancala(Game):
    """A flagrant copy of TicTacToe, from game.py
    It's simplified, so that moves and utility are calculated as needed
    Play TicTacToe on an h x v board, with Max (first player) playing 'X'.
    A state has the player to move and a board, in the form of
    a dict of {(x, y): Player} entries, where Player is 'X' or 'O'."""

    def __init__(self):
        self.initial = GameState(to_move='A', board={})
        self.extraMoveA = False
        self.extraMoveB = False

    def actions(self, state):
        try:
            return state.moves
        except:
            pass
        "Legal moves are any pieces available on your side of the board not yet taken."
        moves = []
        if state.to_move == 'A':
            for a in range (0, state.board.length):
                if state.board.a_spots[a] > 0:
                    moves.append(a)
        if state.to_move == 'B':
            for b in range (0, state.board.length):
                if state.board.b_spots[b] > 0:
                    moves.append(b)
        state.moves = moves
        return moves


    # defines the order of play
    def opponent(self, player):
        if player == 'A' and self.extraMoveA == False:
            return 'B'
        if player == 'A' and self.extraMoveA == True:
            self.extraMoveA = False
            return 'A'
        if player == 'B' and self.extraMoveB == False:
            return 'A'
        if player == 'B' and self.extraMoveB == True:
            self.extraMoveB = False
            return 'B'
        return None

    def result(self, state, move):
        if move not in self.actions(state):
            return state  # Illegal move has no effect
        board = deepcopy(state.board)
        player = state.to_move
        if player == 'A':
            amount = 0
            amount = board.a_spots[move]
            board.a_spots[move] = 0
            for a in range (move+1, board.length):
                if amount != 0:
                    board.a_spots[a] = board.a_spots[a] + 1
                    amount = amount - 1
            if amount == 1:
                self.extraMoveA = True
                board.a_pool = board.a_pool + 1
                amount = 0
            for b in range(0, board.length):
                if amount != 0:
                    board.b_spots[b] = board.b_spots[b] + 1
                    amount = amount - 1
        if player == 'B':
            amount = 0
            amount = board.b_spots[move]
            board.b_spots[move] = 0
            for b in range(move+1, board.length):
                if amount != 0:
                    board.b_spots[b] = board.b_spots[b] + 1
                amount = amount - 1
            if amount == 1:
                self.extraMoveB = True
                board.b_pool = board.b_pool + 1
                amount = 0
            for a in range(0, board.length):
                if amount != 0:
                    board.a_spots[a] = board.a_spots[a] + 1
                amount = amount - 1
        next_mover = self.opponent(player)
        return GameState(to_move=next_mover, board=board)

    def utility(self, state, player):
        "Return the value to player; 1 for win, -1 for loss, 0 otherwise."
        try:
            return state.utility if player == 'A' else -state.utility
        except:
            pass
        board = state.board
        onA = 0
        for a in range (0, board.length):
            onA += board.a_spots[a]
        onB = 0
        for b in range(0, board.length):
            onB += board.b_spots[b]
        util = (board.a_pool+onA) - (board.b_pool+onB)
        return util

    def terminal_test(self, state):
        "A state is terminal if there are no more pieces to move for a player."
        if len(self.actions(state)) == 0:
            onA = 0
            for a in range(0, state.board.length):
                onA += state.board.a_spots[a]
            onB = 0
            for b in range(0, state.board.length):
                onB += state.board.b_spots[b]
            state.board.a_pool += onA
            state.board.b_pool += onB
            return True

    def display(self, state):
        board = state.board
        print(' ',end=' ')
        for b in range(0, board.length):
            print(board.b_spots[(board.length-1)-b],end=' ')
        print()
        print(board.b_pool,end=' ')
        for x in range(0, board.length):
            print(' ',end=' ')
        print(board.a_pool)
        print(' ',end=' ')
        for a in range(0, board.length):
            print(board.a_spots[a],end=' ')
        print()


# class FlagrantCopy(Game):
#     """A flagrant copy of TicTacToe, from game.py
#     It's simplified, so that moves and utility are calculated as needed
#     Play TicTacToe on an h x v board, with Max (first player) playing 'X'.
#     A state has the player to move and a board, in the form of
#     a dict of {(x, y): Player} entries, where Player is 'X' or 'O'."""
#
#     def __init__(self, h=3, v=3, k=3):
#         self.h = h
#         self.v = v
#         self.k = k
#         self.initial = GameState(to_move='X', board={})
#
#     def actions(self, state):
#         try:
#             return state.moves
#         except:
#             pass
#         "Legal moves are any square not yet taken."
#         moves = []
#         for x in range(1, self.h + 1):
#             for y in range(1, self.v + 1):
#                 if (x,y) not in state.board.keys():
#                     moves.append((x,y))
#         state.moves = moves
#         return moves
#
#     # defines the order of play
#     def opponent(self, player):
#         if player == 'X':
#             return 'O'
#         if player == 'O':
#             return 'X'
#         return None
#
#     def result(self, state, move):
#         if move not in self.actions(state):
#             return state  # Illegal move has no effect
#         board = state.board.copy()
#         player = state.to_move
#         board[move] = player
#         next_mover = self.opponent(player)
#         return GameState(to_move=next_mover, board=board)
#
#     def utility(self, state, player):
#         "Return the value to player; 1 for win, -1 for loss, 0 otherwise."
#         try:
#             return state.utility if player == 'X' else -state.utility
#         except:
#             pass
#         board = state.board
#         util = self.check_win(board, 'X')
#         if util == 0:
#             util = -self.check_win(board, 'O')
#         state.utility = util
#         return util if player == 'X' else -util
#
#     # Did I win?
#     def check_win(self, board, player):
#         # check rows
#         for y in range(1, self.v + 1):
#             if self.k_in_row(board, (1,y), player, (1,0)):
#                 return 1
#         # check columns
#         for x in range(1, self.h + 1):
#             if self.k_in_row(board, (x,1), player, (0,1)):
#                 return 1
#         # check \ diagonal
#         if self.k_in_row(board, (1,1), player, (1,1)):
#             return 1
#         # check / diagonal
#         if self.k_in_row(board, (3,1), player, (-1,1)):
#             return 1
#         return 0
#
#     # does player have K in a row? return 1 if so, 0 if not
#     def k_in_row(self, board, start, player, direction):
#         "Return true if there is a line through start on board for player."
#         (delta_x, delta_y) = direction
#         x, y = start
#         n = 0  # n is number of moves in row
#         while board.get((x, y)) == player:
#             n += 1
#             x, y = x + delta_x, y + delta_y
#         x, y = start
#         while board.get((x, y)) == player:
#             n += 1
#             x, y = x - delta_x, y - delta_y
#         n -= 1  # Because we counted start itself twice
#         return n >= self.k
#
#     def terminal_test(self, state):
#         "A state is terminal if it is won or there are no empty squares."
#         return self.utility(state, 'X') != 0 or len(self.actions(state)) == 0
#
#     def display(self, state):
#         board = state.board
#         for x in range(1, self.h + 1):
#             for y in range(1, self.v + 1):
#                 print(board.get((x, y), '.'), end=' ')
#             print()


myGame = Mancala()
play = GameState(
    to_move = 'A',
    board = Board(3,[1,1,1],[1,1,1],0,0),
    label = 'play'
)
won = GameState(
    to_move = 'A',
    board = Board(3,[0,0,0],[0,0,0],4,2),
    label = 'won'
)
lost = GameState(
    to_move = 'A',
    board = Board(3,[0,0,0],[0,0,0],2,4),
    label = 'lost'
)
tied = GameState(
    to_move = 'A',
    board = Board(3,[0,0,0],[0,0,0],3,3),
    label = 'tied'
)
winin1 = GameState(
    to_move = 'A',
    board = Board(3,[0,0,1],[0,0,0],3,2),
    label = 'winin1'
)

# won = GameState(
#     to_move = 'O',
#     board = {(1,1): 'X', (1,2): 'X', (1,3): 'X',
#              (2,1): 'O', (2,2): 'O',
#             },
#     label = 'won'
# )
#
# winin1 = GameState(
#     to_move = 'X',
#     board = {(1,1): 'X', (1,2): 'X',
#              (2,1): 'O', (2,2): 'O',
#             },
#     label = 'winin1'
# )
#
# losein1 = GameState(
#     to_move = 'O',
#     board = {(1,1): 'X', (1,2): 'X',
#              (2,1): 'O', (2,2): 'O',
#              (3,1): 'X',
#             },
#     label = 'losein1'
# )
#
# winin3 = GameState(
#     to_move = 'X',
#     board = {(1,1): 'X', (1,2): 'O',
#              (2,1): 'X',
#              (3,1): 'O',
#             },
#     label = 'winin3'
# )
#
# losein3 = GameState(
#     to_move = 'O',
#     board = {(1,1): 'X',
#              (2,1): 'X',
#              (3,1): 'O', (1,2): 'X', (1,2): 'O',
#             },
#     label = 'losein3'
# )
#
# winin5 = GameState(
#     to_move = 'X',
#     board = {(1,1): 'X', (1,2): 'O',
#              (2,1): 'X',
#             },
#     label = 'winin5'
# )
#
# lost = GameState(
#     to_move = 'X',
#     board = {(1,1): 'X', (1,2): 'X',
#              (2,1): 'O', (2,2): 'O', (2,3): 'O',
#              (3,1): 'X'
#             },
#     label = 'lost'
# )

class TemplateState:    # one way to define the state of a minimal game.

    def __init__(self, player): # add parameters as needed.
        self.to_move = player
        self.label = str(id(self))   # change this to something easier to read
        # add code and self.variables as needed.

    def __str__(self):  # use this exact signature
        return self.label

# class TemplateAction:
#     '''
#     It is not necessary to define an action.
#     Start with actions as simple as a label (e.g., 'Down')
#     or a pair of coordinates (e.g., (1,2)).
#
#     Don't un-comment this until you already have a working game,
#     and want to play smarter.
#     '''
#     def __lt__(self, other):    # use this exact signature
#         # return True when self is a better move than other.
#         return False

class TemplateGame(Game):
    '''
    This is a minimal Game definition,
    the shortest implementation I could run without errors.
    '''

    def __init__(self, initial):    # add parameters if needed.
        self.initial = initial
        # add code and self.variables if needed.

    def actions(self, state):   # use this exact signature.
        acts = []
        # append all moves, which are legal in this state,
        # to the list of acts.
        return acts

    def result(self, state, move):   # use this exact signature.
        newState = deepcopy(state)
        # use the move to modify the newState
        return newState

    def terminal_test(self, state):   # use this exact signature.
        # return True only when the state of the game is over.
        return True

    def utility(self, state, player):   # use this exact signature.
        ''' return:
        >0 if the player is winning,
        <0 if the player is losing,
         0 if the state is a tie.
        '''
        return 0

    def display(self, state):   # use this exact signature.
        # pretty-print the game state, using ASCII art,
        # to help a human player understand his options.
        print(state)

tg = TemplateGame(TemplateState('A'))   # this is the game we play interactively.

myGames = {
    myGame: [
        play, won, lost, tied, winin1
        # won,
        # winin1, losein1, winin3, losein3, winin5,
        # lost,
    ],

    tg: [
        # these are the states we tabulate when we test AB(1), AB(2), etc.
        TemplateState('B'),
        TemplateState('C'),
    ]
}
