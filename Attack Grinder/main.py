import pyautogui as g
import time as t
import win32gui
import win32process
import psutil
import os

g.PAUSE = 0.5

logo = """
████████╗ █████╗ ██████╗  ██████╗ ███████╗████████╗    ██╗      ██████╗  ██████╗██╗  ██╗███████╗██████╗ 
╚══██╔══╝██╔══██╗██╔══██╗██╔════╝ ██╔════╝╚══██╔══╝    ██║     ██╔═══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗
   ██║   ███████║██████╔╝██║  ███╗█████╗     ██║       ██║     ██║   ██║██║     █████╔╝ █████╗  ██║  ██║
   ██║   ██╔══██║██╔══██╗██║   ██║██╔══╝     ██║       ██║     ██║   ██║██║     ██╔═██╗ ██╔══╝  ██║  ██║
   ██║   ██║  ██║██║  ██║╚██████╔╝███████╗   ██║       ███████╗╚██████╔╝╚██████╗██║  ██╗███████╗██████╔╝
   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝       ╚══════╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝╚══════╝╚═════╝                                                                                                    
"""

# Global Variables
id_count = 0
exe_name = ''

cooldowns = {
    'Serial Fire Bombs': 13,
    'Inferno Wave': 19,
    'Chain Lightning': 7,
    'Swift Healing': 13
}

counters = {key: 0 for key in cooldowns}

# Utility Functions
def get_current_time():
    return t.strftime("%H:%M:%S", t.localtime())

def increment_id_count():
    global id_count
    id_count += 1
    return id_count

def get_active_window_exe():
    hwnd = win32gui.GetForegroundWindow()  # Get active window handle
    _, pid = win32process.GetWindowThreadProcessId(hwnd)  # Get process ID
    
    for process in psutil.process_iter(attrs=['pid', 'name', 'exe']):
        if process.info['pid'] == pid:
            return process.info['name']  # Return the executable name
    
    return None

def press_key(button):
    g.press(button)

def is_skill_ready(skill):
    return counters[skill] == 0

def strike(button, skill):
    if target_acquired('cancelTarget.png', (486, 83, 20, 20), 0.5):
        if is_skill_ready(skill):
            print(f"{increment_id_count():<5} {get_current_time():<10} {'strike(' + skill + ')'}")
            press_key(button)
            counters[skill] = 1  # Start cooldown

def skill_counter(skill):
    if counters[skill] > 0:  # Only update if it's on cooldown
        # print(f"{increment_id_count():<5} {get_current_time():<10} {skill + ': ' + str(counters[skill]) + ' / ' + str(cooldowns[skill])}")
        counters[skill] = (counters[skill] + 1) % cooldowns[skill]

def update_all_skill_counters():
    for skill in cooldowns:
        skill_counter(skill)

def turn_screen():
    print(f"{increment_id_count():<5} {get_current_time():<10} {'Turn Screen function not working'}")

def target_acquired(image, region, confidence):
    try:
        located = g.locateOnScreen(image, region=region, confidence=confidence)
        if located:
            return True
    except Exception:
        return;
    return False

def main():
    global exe_name
    print(f"{'#':<5} {'Time':<10} {'Function'}")
    
    while True:
        exe_name = get_active_window_exe()

        if exe_name == 'TL.exe':
        # if exe_name == 'Code.exe':
            press_key('tab')
            press_key('e')

            if target_acquired('cancelTarget.png', (486, 83, 20, 20), 0.5):
                print(f"{increment_id_count():<5} {get_current_time():<10} {'targetAcquired(true)'}")
                
                # Don't for get that this has to search image exists to move onto the next target - not done
                while target_acquired('cancelTarget.png', (486, 83, 20, 20), 0.5):
                    strike('4'  , 'Chain Lightning')
                    strike('1', 'Serial Fire Bombs')
                    strike('2', 'Inferno Wave')
                    strike('9', 'Swift Healing')
                    update_all_skill_counters()
                    t.sleep(1)
  
            else:
                print(f"{increment_id_count():<5} {get_current_time():<10} {'targetAcquired(false)'}")
                turn_screen()
                update_all_skill_counters()
                t.sleep(1)
        else:
            print(f"{increment_id_count():<5} {get_current_time():<10} {'Game window currently not active'}")
            update_all_skill_counters()
            t.sleep(1)

if __name__ == "__main__":
    os.system('cls')
    print(logo)
    # Start the script after a short delay
    t.sleep(3)
    main()