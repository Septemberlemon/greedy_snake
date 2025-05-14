import time
import psutil
import win32ui
import win32gui
import win32con
import win32process
import numpy as np
from PIL import Image
import cv2


def capture_window(proc_name):
    hwnd = get_hwnd_list(proc_name)[0]
    if win32gui.GetWindowPlacement(hwnd)[1] != win32con.SW_MAXIMIZE:
        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
    win32gui.SetForegroundWindow(hwnd)  # 使窗口获得焦点
    time.sleep(1)  # 等待窗口渲染

    _, _, width, height = win32gui.GetClientRect(hwnd)

    window_left, window_top = win32gui.ClientToScreen(hwnd, (0, 0))

    hwnd_desktop = win32gui.GetDesktopWindow()
    dc_handle_desktop = win32gui.GetWindowDC(hwnd_desktop)
    dc_desktop = win32ui.CreateDCFromHandle(dc_handle_desktop)
    compatible_dc = dc_desktop.CreateCompatibleDC()

    bitmap = win32ui.CreateBitmap()
    bitmap.CreateCompatibleBitmap(dc_desktop, width, height)
    compatible_dc.SelectObject(bitmap)

    compatible_dc.BitBlt((0, 0), (width, height), dc_desktop, (window_left, window_top), win32con.SRCCOPY)

    bmp_info = bitmap.GetInfo()
    bmp_str = bitmap.GetBitmapBits(True)
    img = Image.frombuffer(
        "RGB", (bmp_info["bmWidth"], bmp_info["bmHeight"]), bmp_str, "raw", "BGRX", 0, 1
    )

    img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)

    win32gui.DeleteObject(bitmap.GetHandle())
    compatible_dc.DeleteDC()
    dc_desktop.DeleteDC()
    win32gui.ReleaseDC(hwnd_desktop, dc_handle_desktop)

    return np.array(img)


def get_hwnd_list(proc_name):
    hwnd_list = []

    def enum_windows_callback(hwnd, extra):
        if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd):
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            if pid in extra["pids"]:
                hwnd_list.append(hwnd)

    # 获取目标进程名对应的pid
    target_pids = [proc.info["pid"] for proc in psutil.process_iter(attrs=["pid", "name"])
                   if proc.info["name"].lower() == proc_name.lower()]

    if not target_pids:
        print(f"未找到进程名为 {proc_name} 的进程。")
        return []

    # 枚举所有窗口句柄
    win32gui.EnumWindows(enum_windows_callback, {"pids": target_pids})
    return hwnd_list
