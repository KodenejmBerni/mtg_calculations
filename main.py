import matplotlib.pyplot as plt
import numpy as np

from utils import get_probability

if __name__ == '__main__':
    x = np.arange(1, 20)
    y = []
    for elem in x:
        probability = get_probability(
            deck_size=99,
            hand_size=7 + 1,
            rel_cards_deck=elem,
            rel_cards_hand=3,
        )
        y.append(round(probability * 100, 2))

    plt.scatter(x, y)
    plt.xlabel('[-]')
    plt.ylabel('[%]', rotation=0)
    plt.show()
