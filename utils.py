from math import comb, perm


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

    irrel_cards_deck = deck_size - rel_cards_deck
    irrel_cards_hand = hand_size - rel_cards_hand

    combinations = comb(hand_size, rel_cards_hand)
    rel_order = perm(rel_cards_deck, rel_cards_hand)
    irrel_order = perm(irrel_cards_deck, irrel_cards_hand)
    omega_order = perm(deck_size, hand_size)

    probability = combinations * rel_order * irrel_order / omega_order
    return probability


def normalize_percentage(probability: float) -> float:
    return round(probability * 100, 2)
