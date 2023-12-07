
CARD_ORDER = "AKQJT98765432"
CARD_INDEX = {card: index for index, card in enumerate(reversed(CARD_ORDER))}


def get_sorted_counts(hand: str) -> list[int]:
    # E.g. "AAKAK" -> [3, 3, 3, 2, 2]
    counts = []
    for card in hand:
        counts.append(hand.count(card))
    return sorted(counts, reverse=True)


def get_hand_strength(hand: str) -> list[int]:
    sorted_counts = get_sorted_counts(hand)
    card_indices = [CARD_INDEX[card] for card in hand]
    return sorted_counts + card_indices


def read_input() -> list[str]:
    with open("input.txt") as f:
        lines = f.read().splitlines()
    return lines


def parse_input(lines: list[str]) -> list[tuple[str, int]]:
    # "32T3K 765"
    hands_with_bids = []
    for line in lines:
        hand, bid_str = line.split(" ")
        bid = int(bid_str)
        hands_with_bids.append((hand, bid))
    return hands_with_bids


def solve(lines: list[str]) -> int:
    hands_with_bids = parse_input(lines)
    sorted_hands_with_bids = sorted(
        hands_with_bids, key=lambda x: get_hand_strength(x[0])
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
