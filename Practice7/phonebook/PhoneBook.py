import psycopg2
import csv
from config import load_config

def insert_contacts(name, phone):
    """ПРИНИМАЕТ ИМЯ И НОМЕР ТЕЛЕФОНА И СОХРАНЯЕТ"""
    sql="INSERT INTO contacts(first_name, phone) VALUES(%s, %s) ON CONFLICT (phone) DO NOTHING;"
    config=load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (name, phone))
                conn.commit()
                print(f"Контакт {name} сохранен!")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def insert_contacts_csv(filenum):
    """ДАННЫЕ ИЗ ФАЙЛА"""
    sql="INSERT INTO contacts(first_name, phone) VALUES(%s, %s) ON CONFLICT (phone) DO NOTHING;"
    config=load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                with open(filenum, 'r') as f:
                    read=csv.reader(f)
                    for row in read:
                        cur.execute(sql, row)
                conn.commit()
                print(f"Контакт из файла {filenum} сохранен!")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)



def update_name(new_name, number):
    """ОБНОВЛЯЕТ ИМЯ """
    sql = "UPDATE contacts SET first_name= %s WHERE phone = %s;"
    config=load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (new_name, number))
                conn.commit()
                print(f"Контакт {new_name} обновлен!")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)  



def update_phone(new_phone, name):
    """ОБНОВЛЯЕТ НОМЕР """
    sql = "UPDATE contacts SET phone= %s WHERE first_name = %s;"
    config=load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (new_phone, name))
                conn.commit()
                print(f"Номер контакта {name} обновлен!")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error) 



def find_contact(search):

    """НАЙТИ КОНТАКТ"""
    sss=f"%{search}%"
    sql = "SELECT * FROM contacts WHERE first_name ILIKE %s OR phone ILIKE %s;"
    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (sss, sss))
                rows=cur.fetchall()
                if not rows:
                    print("контакт не найден!")
                else:
                    for row in rows:
                        print(f"ID: {row[0]}  Имя: {row[1]} Номер: {row[3]} ")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)



def delete_contact(contact):

    """УДАЛИТЬ КОНТАКТ"""
    sql = "DELETE FROM contacts WHERE first_name= %s OR phone = %s;"
    config=load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (contact, contact))
                conn.commit()
                print(f"Контакт {contact} удален!")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error) 






if __name__ == '__main__':
    print("1: сохранить контакты вручную " \
    "2: сохранить контакты из файла csv " \
    "3: изменить имю контакта " \
    "4: изменить номер контакта " \
    "5: найти контакт " \
    "6: удалить контакт")

    choice = input()
    if choice == '1':
        name=input("имя:")
        phone =input("номер:")
        insert_contacts(name, phone)

    elif choice == '2':
        insert_contacts_csv('people.csv')
    
    elif choice == '3':
        phone=input("введите номер контакта: ")
        newname=input("введите новое имя для контакта: ")
        update_name(newname, phone)

    elif choice == '4':
        name=input("Имя контакта: ")
        new_number=input("введите новый номер контакта: ")
        update_phone(new_number, name)
    
    elif choice == '5':
        find=input("Поиск:")
        find_contact(find)

    elif choice == '6':
        delete=input("Удалить контакт: ")
        delete_contact(delete)

    else:
        print("ошибка")


