# Masowa wysyłka plików do Discorda ze swojego konta
# pip install pyautogui
# pip install msvcrt
# pip install termcolor
import os
import subprocess
import pyautogui
import time
import msvcrt
from termcolor import cprint


def files_to_discord():
    cprint("╚═══ Multimedia Magic – Audio Visual Heaven ═══╝",
           'white', attrs=['bold'])
    print("")
    print("Wysyłanie plików do Discorda...")
    print("Ścieżka do folderu z plikami: " +
          os.path.dirname(os.path.abspath(__file__)))
    print("* Otwórz okno Discorda i kliknij na kanał, do którego chcesz wysłać plik")
    print("* Następnie naciśnij dowolny klawisz, aby kontynuować...")
    msvcrt.getch()
    directory = os.path.dirname(os.path.abspath(__file__))

    subprocess.Popen(f'explorer "{directory}"')
    print('\n* Ustawienie sortowania w explorerze na "Nazwa" i "Rosnąco", Grubuj Według na "Brak"')
    print("* Następnie naciśnij dowolny klawisz, aby kontynuować...")
    print("Będziesz miał 5 sekund na wrócenie do explorera:")
    msvcrt.getch()
    for i in range(5, 0, -1):
        print(str(i) + "...")
        time.sleep(1)

    for filename in os.listdir(directory):
        if not filename.endswith('.py'):
            pyautogui.press('down')
            pyautogui.hotkey('ctrl', 'c')
            print(filename + " - Skopiowano do schowka!")
            subprocess.Popen(
                r'C:\Users\mateu\AppData\Local\Discord\Update.exe --processStart Discord.exe')
            if filename == os.listdir(directory)[0]:
                time.sleep(3)
            else:
                time.sleep(1)
            pyautogui.press('tab')
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(.2)
            pyautogui.press('enter')
            pyautogui.hotkey('alt', 'tab')
    pyautogui.hotkey('ctrl', 'w')
    print("Wysłano wszystkie pliki do Discorda!")


files_to_discord()
