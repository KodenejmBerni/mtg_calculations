from math import comb, perm

import numpy as np


def get_probability(
        *,
        deck_size: int,
        hand_size: int,
        rel_cards_deck: int,
        rel_cards_hand: int,
) -> float:
    assert 0 <= deck_size
    assert 0 <= hand_size <= deck_size
    assert 0 <= rel_cards_deck <= deck_size
    assert 0 <= rel_cards_hand <= hand_size

    unrel_cards_deck = deck_size - rel_cards_deck
    unrel_cards_hand = hand_size - rel_cards_hand

    combinations = comb(hand_size, rel_cards_hand)
    rel_order = perm(rel_cards_deck, rel_cards_hand)
    unrel_order = perm(unrel_cards_deck, unrel_cards_hand)
    omega_order = perm(deck_size, hand_size)

    probability = combinations * rel_order * unrel_order / omega_order
    return probability


def polyfit_smooth_edges(x, y):
    assert len(x) == len(y)
    powers = np.arange(len(x) + 2).reshape(-1, 1)
    xp = x ** powers
    min_i = np.argmin(x)
    max_i = np.argmax(x)
    edges = powers * np.insert(xp[:-1, [min_i, max_i]], 0, [0, 0], 0)
    xp_full = np.concatenate([xp, edges], 1)
    y_full = np.append(y, [0, 0])
    c = y_full @ np.linalg.inv(xp_full)
    return c
