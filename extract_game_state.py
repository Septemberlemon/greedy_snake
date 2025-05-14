import json

from utils import contains_similar_color


with open("config.json") as f:
    config = json.load(f)
    cell2color = config["cell2color"]
    cell2num = config["cell2num"]


def extract_game_state(image):
    rows = 14
    cols = 25
    image = image[255:255 + rows * 75, 343:343 + cols * 75]
    state_matrix = [[] for _ in range(rows)]
    snake = []
    for i in range(rows):
        for j in range(cols):
            cell = "empty"
            indices = [25, 37, 50]
            pixels = []
            for idx in indices:
                for idx2 in indices:
                    pixels.append(image[i * 75 + idx, j * 75 + idx2])
            if list(pixels[4]) in cell2color.values():
                cell = [cell for cell, color in cell2color.items() if color == list(pixels[4])][0]
            elif (pixels[7] == (148, 115, 100)).all():
                cell = "saw"
            elif contains_similar_color(image[i * 75 + 5: i * 75 + 70, j * 75 + 5: j * 75 + 70],
                                        cell2color["snake_lip_color"]):
                cell = "snake_head"
                snake = [(i, j)] + snake
            elif any(int(spot[1]) > int(spot[0]) + int(spot[2]) and spot[1] > 100 for spot in pixels):
                cell = "snake_body"
                snake.append((i, j))
            elif sum(int(_) for _ in pixels[4]) < 200:
                if image[i * 75 + 25: i * 75 + 50, j * 75 + 25: j * 75 + 50].sum() < 70000:
                    cell = "victory_pos"
                elif [i, j] != [10, 21]:
                    cell = "thorn"
            else:
                cell = "empty"

            state_matrix[i].append(cell2num[cell])

            if cell not in ["snake_head", "snake_body", "empty"]:
                print(cell[0], end="\t")
            elif cell == "empty":
                print(".", end="\t")
            else:
                print(cell[6], end="\t")
        print()

    # 重构蛇的身体路径：从 snake_head 开始，寻找所有相邻的 snake_body 构成连通链条
    def segments_connected(segment_1, segment_2):
        x = int(segment_1[0] == segment_2[0])
        for i in range(min(segment_1[x], segment_2[x]) * 75 + 65, max(segment_1[x], segment_2[x]) * 75 + 10):
            if image[*[segment_1[1 - x] * 75 + 37, i][::2 * x - 1]].sum() < 100:
                return False
        return True

    new_snake = snake[:1]
    current = snake[0]
    snake.remove(current)
    # 定义四个方向，依次检测上下左右
    neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while True:
        found_next = False
        for dx, dy in neighbors:
            neighbor = (current[0] + dx, current[1] + dy)
            if neighbor in snake:
                if segments_connected(current, neighbor):
                    new_snake.append(neighbor)
                    snake.remove(neighbor)
                    current = neighbor
                    found_next = True
                    break
        if not found_next:
            break
    print(f"snake:{new_snake}")
    return state_matrix, new_snake
