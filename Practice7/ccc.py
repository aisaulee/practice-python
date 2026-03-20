import psycopg2
import csv
from config import load_config

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

if __name__=='__main__':
    delete=input("Удалить контакт: ")
    delete_contact(delete)
