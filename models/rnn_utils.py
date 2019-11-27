import tensorflow as tf


class RNN:
    def __init__(self, state_size):
        self.state_size = state_size

        self.num_pairs = (state_size ** 2) / 2

        # make a network that takes in the entire state and flattens it,
        # maybe one hot encode each card value,
        # maybe also include currently active card as part of the input,
        # read into a few lstm layers,
        # output as vector of same size as flattened state with confidence of taking each action

        # game is a win if completed under max moves
