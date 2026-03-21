import os
import shutil

def move_and_rename():
    source_folder = os.path.join("projects", "python_practice", "test_dir")
    archive_folder = os.path.join("projects", "archive")
    
    os.makedirs(archive_folder, exist_ok=True)

    file_to_move = "file1.txt"
    src_path = os.path.join(source_folder, file_to_move)
    dst_path = os.path.join(archive_folder, file_to_move)

    if os.path.exists(src_path):
        shutil.move(src_path, dst_path)
        print(f"Файл {file_to_move} перемещен в {archive_folder}")

        new_name_path = os.path.join(archive_folder, "archived_file1.txt")
        os.rename(dst_path, new_name_path)
        print(f"Файл переименован в: archived_file1.txt")
    else:
        print("Файл для перемещения не найден!")

    print(f"\nТекущая рабочая директория: {os.getcwd()}")

if __name__ == "__main__":
    move_and_rename()