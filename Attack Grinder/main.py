import pyautogui as g
import time as t
import win32gui
import win32process
import psutil

# Global Variables
id_count = 0
exe_name = ''

cooldowns = {
    'Serial Fire Bombs': 12,
    'Inferno Wave': 18,
    'Chain Lightning': 6,
    'Swift Healing': 12
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

def strike(button, skill):
    if counters[skill] == 0:
        press_key(button)
    
    counters[skill] = (counters[skill] + 1) % cooldowns[skill]

def turn_screen():
    print("Not currently working")

def target_acquired(image, region, confidence):
    try:
        located = g.locateOnScreen(image, region=region, confidence=confidence)
        if located:
            print(f"{increment_id_count():<5} {get_current_time():<10} {'targetAcquired(true)'}")
            return True
    except Exception:
        print(f"{increment_id_count():<5} {get_current_time():<10} {'targetAcquired(false)'}")
        print(f"{increment_id_count():<5} {get_current_time():<10} {'Turn Screen function not working'}")
    
    return False

def main():
    global exe_name
    print(f"{'#':<5} {'Time':<10} {'Function'}")
    
    while True:
        exe_name = get_active_window_exe()
        
        if exe_name == 'TL.exe':
            press_key('tab')
            press_key('e')
            
            # There is a problem in that when a target is not selected the cooldown are prevented from counting down.
            if target_acquired('cancelTarget.png', (463, 48, 48, 50), 0.5):     
                for _ in range(16):
                    strike('1', 'Serial Fire Bombs')
                    strike('2', 'Inferno Wave')
                    strike('4', 'Chain Lightning')
                    strike('9', 'Swift Healing')
                    t.sleep(1)
        else:
            print(f"{increment_id_count():<5} {get_current_time():<10} {'Game window currently not active'}")
            t.sleep(0.1)

if __name__ == "__main__":
    # Start the script after a short delay
    t.sleep(3)
    main()