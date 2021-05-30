import matplotlib.pyplot as plt
import numpy as np

from utils import get_probability

if __name__ == '__main__':
    for i in range(0, 5):
        x = np.arange(0, 20)
        y = []
        for elem in x:
            probability = get_probability(
                deck_size=60,
                hand_size=7+4,
                rel_cards_deck=elem,
                rel_cards_hand=i,
            )
            y.append(round(probability * 100, 2))
        plt.scatter(x, y, s=10)
    plt.xlabel('[-]')
    plt.ylabel('[%]', rotation=0)
    plt.show()
