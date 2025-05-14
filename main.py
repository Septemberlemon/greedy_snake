from capture_window import capture_window
from extract_game_state import extract_game_state
from A_star import find_solution
from run_solution import run_solution
from process_level_transition import process_level_transition


proc_name = "msedge.exe"

while True:
    image = capture_window(proc_name)  # 截取游戏画面
    state = extract_game_state(image)  # 根据游戏画面提取游戏状态
    solution, snake_final_length = find_solution(state)  # 根据游戏状态找出游戏的解法和最终时刻蛇的长度
    print(solution)
    run_solution(solution)  # 执行解法
    process_level_transition(proc_name, snake_final_length)  # 执行关卡间的一些过渡操作，需要蛇的最终长度决定等待时间
