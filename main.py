import matplotlib.pyplot as plt
import numpy as np

from utils import get_probability, normalize_percentage


def lands():
    deck_size = 99
    hand_size = 7 + 4
    x = np.arange(0, 50)

    # Terrible scenarios
    y = []
    for elem in x:
        probability_0 = get_probability(
            deck_size=deck_size,
            hand_size=hand_size,
            rel_cards_deck=elem,
            rel_cards_hand=0,
        )
        probability_1 = get_probability(
            deck_size=deck_size,
            hand_size=hand_size,
            rel_cards_deck=elem,
            rel_cards_hand=1,
        )
        probability_5 = get_probability(
            deck_size=deck_size,
            hand_size=hand_size,
            rel_cards_deck=elem,
            rel_cards_hand=5,
        )
        probability_6 = get_probability(
            deck_size=deck_size,
            hand_size=hand_size,
            rel_cards_deck=elem,
            rel_cards_hand=6,
        )
        probability_7 = get_probability(
            deck_size=deck_size,
            hand_size=hand_size,
            rel_cards_deck=elem,
            rel_cards_hand=7,
        )
        probability = (probability_0 + probability_1 + probability_5 + probability_6 + probability_7) ** 3
        y.append(normalize_percentage(probability))
    plt.scatter(x, y, s=10)

    # Git good scenarios
    y = []
    for elem in x:
        probability_2 = get_probability(
            deck_size=deck_size,
            hand_size=hand_size,
            rel_cards_deck=elem,
            rel_cards_hand=2,
        )
        probability = probability_2
        y.append(normalize_percentage(probability))
    plt.scatter(x, y, s=10)

    y = []
    for elem in x:
        probability_3 = get_probability(
            deck_size=deck_size,
            hand_size=hand_size,
            rel_cards_deck=elem,
            rel_cards_hand=3,
        )
        probability = probability_3
        y.append(normalize_percentage(probability))
    plt.scatter(x, y, s=10)

    y = []
    for elem in x:
        probability_4 = get_probability(
            deck_size=deck_size,
            hand_size=hand_size,
            rel_cards_deck=elem,
            rel_cards_hand=4,
        )
        probability = probability_4
        y.append(normalize_percentage(probability))
    plt.scatter(x, y, s=10)

    plt.xlabel('[-]')
    plt.ylabel('[%]', rotation=0)
    plt.show()


def other_cards():
    deck_size = 99
    hand_size = 7 + 7
    x = np.arange(0, 10)

    for i in range(0, 6):
        y = []
        for elem in x:
            probability = get_probability(
                deck_size=deck_size,
                hand_size=hand_size,
                rel_cards_deck=elem,
                rel_cards_hand=i,
            )
            y.append(normalize_percentage(probability))
        plt.scatter(x, y, s=10)

    plt.xlabel('[-]')
    plt.ylabel('[%]', rotation=0)
    plt.show()


if __name__ == '__main__':
    # lands()
    other_cards()
