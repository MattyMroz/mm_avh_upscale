# pip install termcolor
import os
from termcolor import cprint


def rename_files_in_directory(directory_path):
    file_list = [file for file in os.listdir(directory_path)
                 if os.path.isfile(os.path.join(directory_path, file)) and not file.endswith('.py')]
    # getctime - czas utworzenia pliku
    # getmtime - czas ostatniej modyfikacji pliku
    # getatime - czas ostatniego dostępu do pliku
    # getsize - rozmiar pliku
    file_list.sort(key=lambda x: os.path.getmtime(
        os.path.join(directory_path, x)))
    for index, filename in enumerate(file_list):
        new_filename = f'{index + 1:04d}' + os.path.splitext(filename)[1]
        os.rename(os.path.join(directory_path, filename),
                  os.path.join(directory_path, new_filename))


def rename_files_in_directory_reverse(directory_path):
    file_list = [file for file in os.listdir(directory_path)
                 if os.path.isfile(os.path.join(directory_path, file)) and not file.endswith('.py')]
    file_list.sort(key=lambda x: os.path.getmtime(
        os.path.join(directory_path, x)), reverse=True)
    for index, filename in enumerate(file_list):
        new_filename = f'{index + 1:04d}' + os.path.splitext(filename)[1]
        os.rename(os.path.join(directory_path, filename),
                  os.path.join(directory_path, new_filename))


def main():
    cprint("╚═══ Multimedia Magic – Audio Visual Heaven ═══╝",
           'white', attrs=['bold'])
    print("")
    current_directory = os.getcwd()
    print("1. Numerowanie plików zgodnie z datą utworzenia w kolejności rosnącej")
    print("2. Numerowanie plików zgodnie z datą utworzenia w kolejności malejącej")
    choice = input("Wybierz numer: ")
    if choice == '1':
        rename_files_in_directory(current_directory)
    if choice == '2':
        rename_files_in_directory_reverse(current_directory)


if __name__ == "__main__":
    main()
