import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MultipleLocator

from utils import get_probability, normalize_percentage

if __name__ == '__main__':
    deck_size = 60
    hand_size = 7
    x = np.arange(0, 30)

    fig = plt.figure()
    fig.show()
    ax = fig.add_subplot()
    for i in range(0, 5):
        y = []
        for elem in x:
            probability = get_probability(
                deck_size=deck_size,
                hand_size=hand_size,
                rel_cards_deck=elem,
                rel_cards_hand=i,
            )
            y.append(normalize_percentage(probability))
        ax.scatter(x, y, s=10, )
        ax.plot(x, y)

    ax.xaxis.set_major_locator(MultipleLocator())
    ax.set_title(f'Deck: {deck_size}, Cards drawn: {hand_size}')
    ax.set_xlabel('[-]')
    ax.set_ylabel('[%]', rotation=0)
    ax.grid()
