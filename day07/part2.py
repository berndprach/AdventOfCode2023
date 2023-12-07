from part1 import read_input, CARD_INDEX, parse_input, get_sorted_counts


def get_hand_strength_with_joker(hand: str) -> list[int]:
    if hand == "JJJJJ":
        return [5, 5, 5, 5, 5, -1, -1, -1, -1, -1]

    joker_free_hand = hand.replace("J", "")
    best_joker = max(joker_free_hand,
                     key=lambda card: joker_free_hand.count(card))
    joker_hand = hand.replace("J", best_joker)

    sorted_counts = get_sorted_counts(joker_hand)
    card_indices = [-1 if card == "J" else CARD_INDEX[card]
                    for card in hand]
    return sorted_counts + card_indices


def solve(lines: list[str]) -> int:
    hands_with_bids = parse_input(lines)
    sorted_hands_with_bids = sorted(
        hands_with_bids, key=lambda x: get_hand_strength_with_joker(x[0])
    )

    solution = 0
    for rank_, (hand, bid) in enumerate(sorted_hands_with_bids):
        rank = rank_ + 1
        solution += rank * bid
    return solution


def main():
    lines = read_input()
    solution = solve(lines)
    print(f"{solution = }")


if __name__ == "__main__":
    main()
