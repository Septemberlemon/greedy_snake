def attempt_push(new_head, dx, dy, rocks, snake, apples, woods, rows, cols):
    """
    当蛇头移动方向上的目标格 new_head 是石块时，将尝试推动该石块。
    检查该石块前方紧邻的格子是否满足推动条件：
      - 必须在棋盘内
      - 该格不能被wood、snake、rocks、apples、saw占据
      - 该格如果是thorn则占据之
    如果推动成功，则将该石块向同一方向移动一格，返回更新后的 rocks 集合（frozenset）。
    否则返回 None 表示推动失败。
    """
    target = (new_head[0] + dx, new_head[1] + dy)
    if not (0 <= target[0] < rows and 0 <= target[1] < cols):
        return None
    if target in snake or target in rocks or target in apples:
        return None
    if target in woods:
        return None
    new_rocks = set(rocks)
    new_rocks.remove(new_head)
    new_rocks.add(target)
    return frozenset(new_rocks)
