import json
from heapq import heappush, heappop

from push import attempt_push
from gravity import apply_gravity
from utils import timer


def dis(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def heuristic(head, goal, rest_apples):
    return dis(head, goal)
    # return 2 * dis(head, goal)
    # return 2 * dis(head, goal) + 10 * sum(dis(apple, head) for apple in rest_apples) + 20 * len(rest_apples)


@timer()
def find_solution(initial_state):
    state_matrix, snake = initial_state
    rows = len(state_matrix)
    cols = len(state_matrix[0]) if rows > 0 else 0

    woods, saws, thorns, apples, rocks = set(), set(), set(), set(), set()
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

    open_set = []
    g_scores = {(snake, apples, rocks): 0}
    start_h = heuristic(snake[0], victory_pos, apples)
    heappush(open_set, (start_h, 0, snake, apples, rocks, []))

    moves = {'up': (-1, 0), 'down': (1, 0), 'left': (0, -1), 'right': (0, 1)}

    while open_set:
        f, g, current_snake, current_apples, current_rocks, path = heappop(open_set)
        current_head = current_snake[0]
        if current_head == victory_pos:
            return path, len(current_snake)

        # 扩展邻居
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
            new_g = g + 1
            if new_g < g_scores.get(state_key, float('inf')):
                g_scores[state_key] = new_g
                h = heuristic(gravity_snake[0], victory_pos, new_apples)
                heappush(open_set, (new_g + h, new_g,
                                    gravity_snake, new_apples, gravity_rocks,
                                    path + [move2num[move]]))
    return None, None
