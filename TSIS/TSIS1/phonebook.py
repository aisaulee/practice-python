import psycopg2
from config import load_config
from connect import connect
import json

def execute_query(query, params=None, fetch=False):
    config = load_config()
    conn = connect(config)
    if conn is None:
        return None
    
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                if fetch:
                    return cur.fetchall()
                return True
            
    except Exception as e:
        print(f"Ошибка при выполнении запроса: {e}")
        return None
    finally:
        conn.close()

def add_new_contact():
    print("\n Добавление нового контакта")
    name = input("Введите имя:")
    email= input("Введите почту:")
    phone = input("Введите номер телефона:")

    config = load_config()
    conn = connect(config)

    try: 
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO contacts(first_name, email) VALUES (%s, %s) RETURNING id", 
                    (name, email)
                )

                contact_id = cur.fetchone()[0]

                cur.execute(
                    "INSERT INTO phones (contact_id, phone) VALUES (%s, %s)",
                    (contact_id, phone)
                )

                print(f"Контакт {name} успешно добавлен!")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        conn.close()

def search_contact():
    print("\n--- Поиск контакта ---")
    query = input("Введите имя или номер телефона для поиска: ")

    config = load_config()
    conn = connect(config)
    
    try:
        with conn.cursor() as cur:
           
            sql = """
                SELECT c.first_name, c.email, p.phone, g.name
                FROM contacts c
                JOIN phones p ON c.id = p.contact_id
                LEFT JOIN groups g ON c.group_id = g.id
                WHERE c.first_name ILIKE %s OR p.phone ILIKE %s
            """
         
            search_param = f"%{query}%"
            cur.execute(sql, (search_param, search_param))
            
            results = cur.fetchall()
            
            if not results:
                print("Ничего не найдено.")
            else:
                print(f"\nРезультаты поиска ({len(results)}):")
                for row in results:
                    print(f"👤 {row[0]} | 📧 {row[1] or 'Нет почты'} | 📞 {row[2]} | 📁 Группа: {row[3] or 'Общая'}")
    except Exception as e:
        print(f"Ошибка поиска: {e}")
    finally:
        conn.close()


def delete_contact():
    name = input("Введите точное имя контакта для удаления: ")
    
    config = load_config()
    conn = connect(config)
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM contacts WHERE first_name = %s", (name,))
                
                if cur.rowcount > 0:
                    print(f"✓ Контакт '{name}' и все его номера удалены.")
                else:
                    print("✗ Контакт не найден.")
    except Exception as e:
        print(f"Ошибка при удалении: {e}")
    finally:
        conn.close()

def view_all_contacts():
    limit = 10  
    offset = 0 
    
    config = load_config()
    conn = connect(config)
    
    while True:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT c.first_name, p.phone, g.name
                    FROM contacts c
                    JOIN phones p ON c.id = p.contact_id
                    LEFT JOIN groups g ON c.group_id = g.id
                    ORDER BY c.first_name
                    LIMIT %s OFFSET %s
                """, (limit, offset))
                
                rows = cur.fetchall()
                
                if not rows and offset == 0:
                    print("Книга пуста.")
                    break
                
                print(f"\n--- Страница {(offset // limit) + 1} ---")
                for r in rows:
                    print(f"👤 {r[0]:<15} | 📞 {r[1]:<15} | 📁 {r[2] or 'Общая'}")
                
                print("\n[n] - След. страница, [p] - Пред. страница, [q] - Выход в меню")
                choice = input("Выберите действие: ").lower()
                
                if choice == 'n':
                    if len(rows) == limit: offset += limit
                    else: print("Это последняя страница.")
                elif choice == 'p':
                    offset = max(0, offset - limit)
                elif choice == 'q':
                    break
        except Exception as e:
            print(f"Ошибка: {e}")
            break
    conn.close()

def update_contact_email():
    name = input("Введите имя контакта: ")
    new_email = input("Введите новый email: ")
    
    query = "UPDATE contacts SET email = %s WHERE first_name = %s"
    result = execute_query(query, (new_email, name))
    
    if result:
        print(f"✓ Email для {name} обновлен!")
    else:
        print("✗ Ошибка или контакт не найден.")

def change_contact_group():
    name = input("Имя контакта: ")
    group = input("Новая группа: ")
    
    config = load_config()
    conn = connect(config)
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("CALL move_to_group(%s, %s)", (name, group))
                print(f"✓ Контакт {name} перемещен в группу {group}")
    except Exception as e:
        print(f"✗ Ошибка: {e}")
    finally:
        conn.close()


def export_to_json():
    rows = execute_query("""
        SELECT c.first_name, c.email, p.phone, g.name 
        FROM contacts c 
        JOIN phones p ON c.id = p.contact_id 
        LEFT JOIN groups g ON c.group_id = g.id
    """, fetch=True)
    
    data = []
    for r in rows:
        data.append({"name": r[0], "email": r[1], "phone": r[2], "group": r[3]})
        
    with open("contacts.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print("✓ Данные экспортированы в contacts.json")


def import_from_json(filename="contacts.json"):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        config = load_config()
        conn = connect(config)
        with conn: 
            with conn.cursor() as cur:
                for entry in data:
                    cur.execute("SELECT id FROM phones WHERE phone = %s", (entry['phone'],))
                    if cur.fetchone():
                        print(f"⚠ Пропуск: {entry['phone']} уже существует.")
                        continue
                    
                    cur.execute(
                        "INSERT INTO contacts (first_name, email) VALUES (%s, %s) RETURNING id",
                        (entry['name'], entry['email'])
                    )
                    c_id = cur.fetchone()[0]
                    
                    cur.execute(
                        "INSERT INTO phones (contact_id, phone) VALUES (%s, %s)",
                        (c_id, entry['phone'])
                    )
        print("✓ Данные успешно импортированы.")
    except FileNotFoundError:
        print("✗ Файл не найден.")
    except Exception as e:
        print(f"✗ Ошибка: {e}")
    finally:
        conn.close()

def main():
    while True:
        print("\n" + "="*30)
        print("      PHONEBOOK v3.0")
        print("="*30)
        print("1. Показать все (пагинация)")
        print("2. Добавить контакт")
        print("3. Найти контакт")
        print("4. Удалить контакт")
        print("5. Обновить почту")
        print("6. Изменить группу (Procedures)")
        print("7. Экспорт в JSON")
        print("8. Импорт из JSON")
        print("0. Выход")
        
        choice = input("\nВыбор: ")

        
        if choice == '1': view_all_contacts()
        elif choice == '2': add_new_contact()
        elif choice == '3': search_contact()
        elif choice == '4': delete_contact()
        elif choice == '5': update_contact_email()
        elif choice == '6': change_contact_group()
        elif choice == '7': export_to_json()
        elif choice == '8': import_from_json()
        elif choice == '0': break
        else: print("Ошибка: введите число от 0 до 8")


if __name__ == "__main__":
    main()
