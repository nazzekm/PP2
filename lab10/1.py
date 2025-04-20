import psycopg2
import csv

conn = psycopg2.connect(
    dbname="PhoneBook",  
    user="postgres",     
    password="12345678",   
    host="localhost",    
    port="5432"          
)
conn.set_client_encoding('UTF8')  # кодировка

# создание курсора 
cur = conn.cursor()

def create_table():
    cur.execute("""
        CREATE TABLE IF NOT EXISTS PhoneBook(
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(50),
            last_name VARCHAR(50),
            phone_number VARCHAR(15) UNIQUE
        );
    """)
    conn.commit()

# вставка данных
def insert_from_csv():
    try:
        with open(r"C:\Users\User\Desktop\code\git-lessons\lab10\phonebook.csv", newline='', encoding='utf-8') as csv_file:
            r = csv.reader(csv_file)
            for row in r:
                if len(row) != 3:
                    continue  
                cur.execute("""
                    INSERT INTO PhoneBook (first_name, last_name, phone_number)
                    VALUES (%s, %s, %s);
                """, (row[0], row[1], row[2]))
            conn.commit()
        print("Данные успешно загружены из CSV файла.")
    except Exception as e:
        print(f"Ошибка при загрузке данных: {e}")

# вставка данных вручную
def insert_from_console():
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    phone_number = input("Enter phone number: ")
    cur.execute("""
        INSERT INTO PhoneBook (first_name, last_name, phone_number)
        VALUES (%s, %s, %s);
    """, (first_name, last_name, phone_number))
    conn.commit()

# обновление данных
def update_contact():
    user_id = input("Enter user ID to update: ")
    new_first_name = input("Enter new first name: ")
    new_phone_number = input("Enter new phone number: ")
    cur.execute("""
        UPDATE PhoneBook
        SET first_name = %s, phone_number = %s
        WHERE id = %s;
    """, (new_first_name, new_phone_number, user_id))
    conn.commit()

# удаление данных
def delete_contact():
    print("1. Delete by name\n2. Delete by phone number")
    choice = int(input())
    if choice == 1:
        name = input("Enter name to delete: ")
        cur.execute("""
            DELETE FROM PhoneBook
            WHERE first_name = %s;
        """, (name,))
    elif choice == 2:
        phone_number = input("Enter phone number to delete: ")
        cur.execute("""
            DELETE FROM PhoneBook
            WHERE phone_number = %s;
        """, (phone_number,))
    conn.commit()

# поиск контактов
def search_contacts():
    print("1. Search by name\n2. Search by phone number\n3. Show all")
    choice = int(input())
    if choice == 1:
        name = input("Enter name to search: ")
        cur.execute("""
            SELECT * FROM PhoneBook
            WHERE first_name = %s;
        """, (name,))
    elif choice == 2:
        phone_number = input("Enter phone number to search: ")
        cur.execute("""
            SELECT * FROM PhoneBook
            WHERE phone_number = %s;
        """, (phone_number,))
    elif choice == 3:
        cur.execute("SELECT * FROM PhoneBook;")
    rows = cur.fetchall()
    for row in rows:
        print(row)

def main():
    create_table()
    while True:
        print("\nChoose an option:")
        print("1. Insert data (from CSV or console)")
        print("2. Delete contact")
        print("3. Update contact")
        print("4. Search contacts")
        print("5. Quit")
        option = int(input())
        
        if option == 1:
            print("1. Insert from CSV\n2. Insert from console")
            method = int(input())
            if method == 1:
                insert_from_csv()
            elif method == 2:
                insert_from_console()
        
        elif option == 2:
            delete_contact()
        
        elif option == 3:
            update_contact()
        
        elif option == 4:
            search_contacts()
        
        elif option == 5:
            break

    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
