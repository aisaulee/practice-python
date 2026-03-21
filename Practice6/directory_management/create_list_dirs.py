import os

def manage_directories():
    path = os.path.join("projects", "python_practice", "test_dir")
    os.makedirs(path, exist_ok=True)
    print(f"{path}")


    files = ["file1.txt", "file2.txt", "script.py"]
    for file_name in files:
        file_path = os.path.join(path, file_name)
        with open(file_path, 'w') as f:
            f.write("content") 

    print("\nСодержимое папки:")
    content = os.listdir(path)
    for item in content:
        full_item_path = os.path.join(path, item)
        if os.path.isfile(full_item_path):
            print(f"[ФАЙЛ] {item}")
        else:
            print(f"[ПАПКА] {item}")

if __name__ == "__main__":
    manage_directories()