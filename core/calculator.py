from core.data import BONUS_TABLE, MAX_QUALITY_LEVEL


def quality_bonus(tier: int, quality: int) -> float:
    if tier not in BONUS_TABLE:
        raise ValueError(f"Invalid tier: {tier}")
    if quality < 1 or quality > MAX_QUALITY_LEVEL:
        raise ValueError(f"Invalid quality level: {quality}")
    return BONUS_TABLE[tier][quality]


def total_chance(count: int, tier: int, quality: int) -> float:
    if count < 0:
        raise ValueError(f"Count must be non-negative: {count}")
    bonus = quality_bonus(tier, quality)
    return min(count * bonus, 1.0)


def distribute(
    start_level: int,
    chance: float,
    output_per_min: float,
    max_unlocked_level: int = MAX_QUALITY_LEVEL,
) -> dict[int, tuple[float, float]]:
    if start_level < 1 or start_level > MAX_QUALITY_LEVEL:
        raise ValueError(f"Invalid start_level: {start_level}")
    if max_unlocked_level < 1 or max_unlocked_level > MAX_QUALITY_LEVEL:
        raise ValueError(f"Invalid max_unlocked_level: {max_unlocked_level}")
    if start_level > max_unlocked_level:
        raise ValueError(
            f"start_level ({start_level}) > max_unlocked_level ({max_unlocked_level})"
        )
    if chance < 0.0 or chance > 1.0:
        raise ValueError(f"Chance must be in [0, 1]: {chance}")

    result: dict[int, tuple[float, float]] = {}
    m = max_unlocked_level - start_level

    if m == 0:
        result[start_level] = (1.0, output_per_min)
        return result

    for level in range(start_level, max_unlocked_level + 1):
        if level == start_level:
            share = 1.0 - chance
        elif level < max_unlocked_level:
            k = level - start_level
            share = chance * 0.9 * (0.1 ** (k - 1))
        else:
            share = chance * (0.1 ** (m - 1))
        result[level] = (share, share * output_per_min)

    return result


def calculate_with_recycling(
    base_input: float,
    start_level: int,
    Q_prod: float,
    Q_rec: float,
    recycle_threshold: int,
    max_unlocked_level: int = MAX_QUALITY_LEVEL,
    max_iterations: int = 1000,
) -> dict[int, float]:
    if start_level < 1 or start_level > MAX_QUALITY_LEVEL:
        raise ValueError(f"Invalid start_level: {start_level}")
    if max_unlocked_level < 1 or max_unlocked_level > MAX_QUALITY_LEVEL:
        raise ValueError(f"Invalid max_unlocked_level: {max_unlocked_level}")
    if start_level > max_unlocked_level:
        raise ValueError(
            f"start_level ({start_level}) > max_unlocked_level ({max_unlocked_level})"
        )
    if recycle_threshold < 1 or recycle_threshold > max_unlocked_level:
        raise ValueError(
            f"recycle_threshold ({recycle_threshold}) out of range"
        )
    if Q_prod < 0.0 or Q_prod > 1.0 or Q_rec < 0.0 or Q_rec > 1.0:
        raise ValueError("Quality chances must be in [0, 1]")
    if base_input < 0:
        raise ValueError(f"base_input must be non-negative: {base_input}")

    queue: dict[int, float] = {start_level: base_input}
    final: dict[int, float] = {level: 0.0 for level in range(1, max_unlocked_level + 1)}

    epsilon = 1e-9 * max(base_input, 1.0)

    for _ in range(max_iterations):
        crafted: dict[int, float] = {}
        for lvl, amount in list(queue.items()):
            if amount < epsilon:
                continue
            dist = distribute(lvl, Q_prod, amount, max_unlocked_level)
            for out_lvl, (_, items) in dist.items():
                crafted[out_lvl] = crafted.get(out_lvl, 0.0) + items

        queue.clear()

        any_recycled = False
        for lvl in range(1, max_unlocked_level + 1):
            amount = crafted.get(lvl, 0.0)
            if lvl <= recycle_threshold:
                if amount > 0:
                    any_recycled = True
                    rec_dist = distribute(lvl, Q_rec, amount * 0.25, max_unlocked_level)
                    for out_lvl, (_, items) in rec_dist.items():
                        queue[out_lvl] = queue.get(out_lvl, 0.0) + items
            else:
                final[lvl] = final.get(lvl, 0.0) + amount

        if not any_recycled:
            break

    return final
