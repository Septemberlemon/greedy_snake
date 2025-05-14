import json
from collections import deque

from push import attempt_push
from gravity import apply_gravity
from utils import timer


@timer()
def find_solution(initial_state):
    """
    利用 BFS 求解蛇游戏，使蛇头到达 victory_pos。
    初始网格中每个元素可能为：
      "empty", "apple", "wood", "saw", "thorn", "rock", "snake_head", "snake_body"
    其中：
      - apple, wood, saw, thorn 为固定位置（saw 和 thorn 均视为陷阱）
      - rock 为可推动并受重力影响的小石块
      - snake_head 和 snake_body 表示蛇的初始位置（蛇头在最前）
    返回移动序列（例如 ['up', 'right', ...]），无解则返回 None。
    """
    state_matrix, snake = initial_state
    rows = len(state_matrix)
    cols = len(state_matrix[0]) if rows > 0 else 0

    woods = set()
    saws = set()
    thorns = set()
    apples = set()
    rocks = set()
    victory_pos = None

    with open("config.json") as f:
        config = json.load(f)
        cell2num = config["cell2num"]
        move2num = config["move2num"]

    for i in range(rows):
        for j in range(cols):
            cell = state_matrix[i][j]
            pos = (i, j)
            if cell == cell2num['wood']:
                woods.add(pos)
            elif cell == cell2num['apple']:
                apples.add(pos)
            elif cell == cell2num['saw']:
                saws.add(pos)
            elif cell == cell2num['thorn']:
                thorns.add(pos)
            elif cell == cell2num['rock']:
                rocks.add(pos)
            elif cell == cell2num['victory_pos']:
                victory_pos = pos

    snake = tuple(snake)
    apples = frozenset(apples)
    rocks = frozenset(rocks)

    visited = set()
    queue = deque()
    init_state = (snake, apples, rocks, [])
    queue.append(init_state)
    visited.add((snake, apples, rocks))

    moves = {
        'up': (-1, 0),
        'down': (1, 0),
        'left': (0, -1),
        'right': (0, 1)
    }

    while queue:
        current_snake, current_apples, current_rocks, path = queue.popleft()
        current_head = current_snake[0]
        if current_head == victory_pos:
            return path, len(current_snake)

        for move, (dx, dy) in moves.items():
            new_head = (current_head[0] + dx, current_head[1] + dy)
            if not (0 <= new_head[0] < rows and 0 <= new_head[1] < cols):
                continue
            if new_head in woods or new_head in saws or new_head in thorns:
                continue
            if new_head in current_snake[1:]:
                continue

            new_rocks = current_rocks
            if new_head in current_rocks:
                pushed = attempt_push(new_head, dx, dy, current_rocks, current_snake, current_apples, woods, rows, cols)
                if pushed is None:
                    continue
                new_rocks = pushed

            if new_head in current_apples:
                if move == "up" and len(set(_[1] for _ in current_snake)) == 1:
                    continue
                else:
                    new_snake = (new_head,) + current_snake
                new_apples = set(current_apples)
                new_apples.remove(new_head)
                new_apples = frozenset(new_apples)
            else:
                new_snake = (new_head,) + current_snake[:-1]
                new_apples = current_apples

            if new_head == victory_pos and not (move == "up" and len(set(_[1] for _ in current_snake)) == 1):
                return path + [move2num[move]], len(new_snake)
            if new_head[0] + 1 > rows:
                continue
            gravity_snake, gravity_rocks = apply_gravity(new_snake, new_rocks, new_apples, woods, saws, thorns, rows,
                                                         victory_pos)
            if gravity_snake is None:
                continue

            state_key = (gravity_snake, new_apples, gravity_rocks)
            if state_key in visited:
                continue
            visited.add(state_key)
            new_path = path + [move2num[move]]
            if gravity_snake[0] == victory_pos:
                return new_path, len(gravity_snake)
            queue.append((gravity_snake, new_apples, gravity_rocks, new_path))
    return None, None
