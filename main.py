import matplotlib.pyplot as plt
import numpy as np

from utils import get_probability

if __name__ == '__main__':
    # passable = [0, 0, 0, 1, 1, 0]
    for i in range(0, 6):
        x = np.arange(0, 51)
        y = []
        for elem in x:
            probability = get_probability(
                deck_size=99,
                hand_size=7 + 7,
                rel_cards_deck=elem,
                rel_cards_hand=i,
            )
            # if passable[i]:
            y.append(round(probability * 100, 2))
            # else:
            #     y.append(round(probability ** 2 * 100, 2))
        plt.scatter(x, y, s=2)
    plt.xlabel('[-]')
    plt.ylabel('[%]', rotation=0)
    plt.show()
