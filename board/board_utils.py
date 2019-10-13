from cards.card_utils import create_deck_of_nums, shuffle_deck
import numpy as np


def init_board(board_length):
    deck = create_deck_of_nums(board_length ** 2)
    deck = shuffle_deck(deck)

    board = np.reshape(deck, (board_length, board_length))

    return board


class Board:
    def __init__(self, board_length):
        if board_length % 2 != 0:
            raise UnevenNumberOfCardsException("Board only supports even numbers of cards.")
        self.board_length = board_length
        self.state = init_board(self.board_length)
        self.biggest_num_digits = int(np.floor(np.log10((self.board_length ** 2) // 2))) + 1
        self.active_card = None

    def print_board(self, board):
        for r in range(self.board_length):
            print(("{}" * self.board_length)
                  .format(*[card.to_string(self.biggest_num_digits) for card in board[r]]))

    def is_valid_move(self, x, y):
        return 0 <= x < self.board_length and 0 <= y < self.board_length and not self.state[x, y].visible

    def reveal(self, x, y, human_player):
        self.state[x, y].reveal()
        new_state = self.deep_copy() if human_player else self.get_state_f()

        if self.active_card is not None:
            is_match = self.check_for_match(self.state[x, y])

            if not is_match:
                self.reset_actives(self.state[x, y])

            return is_match, new_state
        else:
            self.active_card = self.state[x, y]
            return None, new_state

    def check_for_match(self, card):
        if self.active_card.value == card.value:
            self.active_card.active = False
            self.active_card = None
            card.active = False
            return True

        return False

    def reset_actives(self, card):
        self.active_card.active = False
        self.active_card.flip()
        self.active_card = None
        card.active = False
        card.flip()

    def deep_copy(self):
        return np.array([[card.__copy__() for card in r] for r in self.state])

    def get_state_f(self):
        return np.array([[card.as_float() for card in r] for r in self.state])


class UnevenNumberOfCardsException(Exception):
    pass
