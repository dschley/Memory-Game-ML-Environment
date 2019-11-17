import tensorflow as tf
from models.actor_critic_utils import ActorCriticNetwork


class Agent:
    def __init__(self, state_size, action_size):
        """
        Agent that will play the memory game.

        Needs to know the state size,
        have knowledge of its past moves/states,
        ability to select (and recognize playable moves?) next move on NxN board.

        :param state_size: N for the size of the NxN board.
        :param action_size: N^2 for the number of possible moves it could select.
        OR not needed and just uses state size to determine max range in selection of coordinates.
        """
        self.network = ActorCriticNetwork(state_size, action_size)

    def act(self, state):
        pass

    def step(self, state, action, reward, next_state, done):
        pass


