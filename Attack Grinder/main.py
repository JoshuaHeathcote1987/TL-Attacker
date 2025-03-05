import pyautogui as g
import time as t
import win32gui
import win32process
import psutil
import os
import logo
from command import Command

# Global Variables
region = (487, 84, 17, 17)
id_count = 0
exe_name = ''
flip_flop = False

# Define attack skills with cooldowns and button mappings
command_list = {
    'swift_healing': Command(13, '9', 0.5, 2),
    'serial_fire_bombs': Command(12, '1', 2, 1),
    'chain_lightning': Command(7, '4', 0.5, 1),
    'inferno_wave': Command(17, '2', 0.5, 1),
}

counters = {key: 0 for key in command_list}

# Utility Functions
def get_current_time():
    return t.strftime("%H:%M:%S", t.localtime())

def increment_id_count():
    global id_count
    id_count += 1
    return id_count

def get_active_window_exe():
    hwnd = win32gui.GetForegroundWindow()
    _, pid = win32process.GetWindowThreadProcessId(hwnd)
    for process in psutil.process_iter(attrs=['pid', 'name', 'exe']):
        if process.info['pid'] == pid:
            return process.info['name']
    return None

def press_key(button, duration, amount):
    for _ in range(amount):
        g.keyDown(button)
        t.sleep(duration)
        g.keyUp(button)

def is_skill_ready(skill_name):
    return counters[skill_name] == 0

def strike(skill_name, skill):
    if target_acquired('cancelTarget.png', region, 0.5) and is_skill_ready(skill_name):
        print(f"{increment_id_count():<5} {get_current_time():<10} strike({skill_name})")
        press_key(skill.button, skill.duration, skill.amount)
        counters[skill_name] = 1

def skill_counter(skill_name, skill):
    if counters[skill_name] > 0:
        print(f"{increment_id_count():<5} {get_current_time():<10} strike({skill_name}) Countdown({counters[skill_name]})")
        counters[skill_name] = (counters[skill_name] + 1) % skill.cooldown

def update_all_skill_counters():
    for skill_name, skill in command_list.items():
        skill_counter(skill_name, skill)

def turn_screen():
    print(f"{increment_id_count():<5} {get_current_time():<10} Turn Screen")
    press_key('left', 0.5, 1)

def target_acquired(image, region, confidence):
    try:
        return g.locateOnScreen(image, region=region, confidence=confidence) is not None
    except Exception:
        return False
    
def init_attack():
    press_key('tab', 0, 1)
    press_key('e', 0, 1)

# Main Loop
def main():
    global exe_name
    print(f"{'#':<5} {'Time':<10} {'Function'}")
    while True:
        exe_name = get_active_window_exe()
        if exe_name == 'TL.exe':
            init_attack()
            if target_acquired('cancelTarget.png', region, 0.5):
                print(f"{increment_id_count():<5} {get_current_time():<10} Target Acquired")
                while target_acquired('cancelTarget.png', region, 0.5):
                    for skill_name, skill in command_list.items():
                        strike(skill_name, skill)
                    update_all_skill_counters()
                    t.sleep(1)
            else:
                print(f"{increment_id_count():<5} {get_current_time():<10} No Target Found")
                turn_screen()
        else:
            print(f"{increment_id_count():<5} {get_current_time():<10} Game Window Not Active")
        update_all_skill_counters()
        t.sleep(1)

if __name__ == '__main__':
    os.system('cls')
    t.sleep(3)
    main()
