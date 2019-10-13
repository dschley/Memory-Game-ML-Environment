from board.board_utils import Board


class Game:
    def __init__(self, board_length=4, max_turns=64):
        self.board_length = board_length
        self.board = Board(self.board_length)

        self.num_turns = 0
        self.max_turns = max_turns

        self.score = 0

    def board_state(self):
        return self.board.state

    def board_state_f(self):
        return self.board.get_state_f()

    def step(self, x, y, human_player):
        """
        Check if move is valid on current board_utils.py state.
        If it is valid, return new board_utils.py state, and reward (tentative).
        If it is not valid, return None

        :param human_player: True if the player is human and would like to see complex data on the cards.
            False if player is computer and cards are represented by floats.
        :param x: x coordinate of card selected.
        :param y: y coordinate of card selected.
        """

        if self.board.is_valid_move(x, y):
            self.num_turns += 1
            is_match, next_state = self.board.reveal(x, y, human_player)

            if is_match is not None and is_match:
                self.score += 1
                print("Match Found!")
            return is_match, next_state, self.is_done()

        return None, None, None

    def is_done(self):
        return self.score == (self.board_length ** 2) // 2

    def print_game(self):
        print("Turn: {}, Score: {}".format(self.num_turns, self.score))
        self.board.print_board(self.board_state())
        print("{} turns remaining!\n".format(self.max_turns - self.num_turns))

    def print_interim_state(self, is_match, board):
        print()
        if is_match:
            print("Successful match!")
        else:
            print("Whomp whomp :(")

        self.board.print_board(board)
        print()


def play_from_console(game):
    game.print_game()

    while game.num_turns < game.max_turns and not game.is_done():
        print("Select a coordinate from 0,0 to {0},{0}".format(game.board_length - 1))

        x = prompt_for_int_input("Enter a number for the x coordinate")
        y = prompt_for_int_input("Enter a number for the y coordinate")

        is_match, next_state, is_done = game.step(x, y, True)

        if is_match is not None:
            game.print_interim_state(is_match, next_state)

        game.print_game()

    if game.is_done():
        print("Congratulations! You completed the game in {} moves!".format(game.num_turns))
    else:
        print("Sorry, you exceeded {} moves!".format(game.max_turns))


def prompt_for_int_input(initial_prompt):
    i = input(initial_prompt)

    while True:
        try:
            i = int(i)
            break
        except ValueError:
            print("{} is not a valid number.".format(i))
            i = input("Please enter a valid number.")

    return i


if __name__ == '__main__':
    play_from_console(Game(2))
