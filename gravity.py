def apply_gravity(snake, rocks, apples, woods, saws, thorns, rows, victory_pos):
    """
    同时模拟蛇和石块的下落，直到稳定为止。
    - 蛇：若所有蛇体下方都不在 (apples ∪ woods u rocks) 中，则整体下落一格（出界则返回 None 表示游戏失败）。
    - 石块：对于每个石块，若其下方不在支撑集合中，则下落一格。
      对石块，下方支撑集合为：apples ∪ woods ∪ snake ∪ (当前石块位置) ∪ saws
      注意：thorns 不支持石块。

    返回更新后的 (snake, rocks)；若蛇因下落出界则返回 (None, None)。
    """
    changed = True
    rocks = set(rocks)
    while changed:
        changed = False
        # 蛇的下落
        if all((x + 1 <= rows and ((x + 1, y) not in apples and (x + 1, y) not in woods and (x + 1, y) not in rocks)
                and (x + 1, y) != victory_pos) for (x, y) in snake):
            candidate_snake = tuple((x + 1, y) for (x, y) in snake)
            if any(x + 1 > rows for (x, y) in candidate_snake) or any(
                    (x, y) in (saws | thorns) for (x, y) in candidate_snake):
                return None, None  # 蛇触底，游戏失败
            snake = candidate_snake
            changed = True

        # 石块的下落
        old_rocks = set(rocks)
        new_rocks = set()
        for (x, y) in rocks:
            if x == rows - 1:
                continue
            below = (x + 1, y)
            if below in apples or below in woods or below in snake or below in old_rocks or below in saws:
                new_rocks.add((x, y))
            else:
                new_rocks.add((x + 1, y))
                changed = True
        rocks = new_rocks
    return snake, frozenset(rocks)
