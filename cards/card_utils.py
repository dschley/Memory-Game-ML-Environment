import random as rand
import numpy as np


def create_deck_of_nums(num_cards):
    return [Card(i) for i in range(1, (num_cards // 2) + 1) for _ in range(2)]


def shuffle_deck(deck):
    return rand.sample(deck, len(deck))


class Card:
    def __init__(self, value):
        self.value = value
        self.visible = False
        self.active = False

    def is_match(self, other):
        return self.value == other.value

    def flip(self):
        self.visible = not self.visible

    def reveal(self):
        self.flip()
        self.active = True

    def to_string(self, biggest_num_digits, show_hidden=False):
        if not show_hidden and not self.visible:
            braces = "[{}]" if not self.active else "({})"
            return braces.format("#" * biggest_num_digits)

        braces = "[{}{}]" if not self.active else "({}{})"
        return braces.format(self.value, " " * (biggest_num_digits - int(np.floor(np.log10(self.value))) - 1))

    def as_float(self):
        return float(self.value) if self.visible else 0.0

    def __copy__(self):
        card = Card(self.value)
        card.visible = self.visible
        card.active = self.active
        return card
