import psycopg2
import csv

conn = psycopg2.connect(
    host="localhost", dbname="lab10", user="postgres",
    password="12345678", port="5432"
)

cur = conn.cursor()

def insert_or_update_user(name, surname, phone):
    cur.execute("CALL insert_or_update_user(%s, %s, %s)", (name, surname, phone))
    conn.commit()
    print("User inserted or updated successfully.")

# несколько пользователей с проверкой телефона
def insert_multiple_users(names, surnames, phones):
    cur.execute("CALL insert_multiple_users(%s, %s, %s)", (names, surnames, phones))
    conn.commit()
    print("Multiple users inserted successfully.")
    
# несколько пользователей 
def insert_multiple_console():
    names = input("Enter names separated by commas: ").split(',')
    surnames = input("Enter surnames separated by commas: ").split(',')
    phones = input("Enter phone numbers separated by commas: ").split(',')

    if len(names) != len(surnames) or len(names) != len(phones):
        print("The number of names, surnames, and phone numbers must be the same!")
        return

    # отдельно
    for i in range(len(names)):
        insert_or_update_user(names[i].strip(), surnames[i].strip(), phones[i].strip())

# один пользователь
def insert_or_update_user(name, surname, phone):
    cur.execute("CALL insert_or_update_user(%s, %s, %s)", (name, surname, phone))
    conn.commit()
    print(f"User {name} {surname} inserted or updated successfully.")



# вставка вручную
def insert_console():
    name = input("Name: ")
    surname = input("Surname: ")
    phone = input("Phone: ")
    
    insert_or_update_user(name, surname, phone)


def insert_csv():
    path = input("Enter CSV file path: ")
    with open(path, 'r') as f:
        reader = csv.reader(f)
        next(reader)  
        for row in reader:
            insert_or_update_user(row[0], row[1], row[2])

# обновление
def update_column(column):
    old_value = input(f"Enter current {column}: ")
    new_value = input(f"Enter new {column}: ")
    cur.execute(f"UPDATE phonebook SET {column} = %s WHERE {column} = %s", (new_value, old_value))
    conn.commit()
    print(f"{column} updated successfully.")

# удаление
def delete_user():
    field = input("Delete by (name/phone): ").lower()
    
    if field not in ["name", "phone"]:
        print("Invalid input. Choose 'name' or 'phone'.")
        return

    value = input(f"Enter {field} to delete: ")
    cur.execute(f"DELETE FROM phonebook WHERE {field} = %s", (value,))
    conn.commit()
    print("User deleted if match was found.")

# запрос данных по колонке
def query_by_column(column):
    value = input(f"Enter {column}: ")
    cur.execute(f"SELECT * FROM phonebook WHERE {column} = %s", (value,))
    rows = cur.fetchall()
    for row in rows:
        print(row)

# вывод
def show_all():
    cur.execute("SELECT * FROM phonebook")
    rows = cur.fetchall()
    for row in rows:
        print(row)

# поиск по шаблону
def search_by_pattern():
    pattern = input("Enter pattern: ")
    cur.execute("SELECT * FROM phonebook WHERE name ILIKE %s OR surname ILIKE %s OR phone ILIKE %s",
                (f'%{pattern}%', f'%{pattern}%', f'%{pattern}%'))
    rows = cur.fetchall()
    for row in rows:
        print(row)

def menu():
    while True:
        print("""
        === MENU ===
        [i] Insert (console or csv)
        [u] Update
        [d] Delete
        [q] Query
        [s] Show all
        [p] Pattern search
        [m] Insert multiple users manually
        [f] Finish
        """)
        cmd = input("Choose command: ").lower()

        if cmd == "i":
            opt = input('Type "csv" to upload file or "con" to enter manually: ')
            if opt == "con": insert_console()
            elif opt == "csv": insert_csv()

        elif cmd == "m":
            insert_multiple_console()

        elif cmd == "u":
            col = input("Which column to update (name/surname/phone): ")
            if col in ["name", "surname", "phone"]:
                update_column(col)

        elif cmd == "d":
            delete_user()

        elif cmd == "q":
            col = input("Search by (name/phone): ")
            if col in ["name", "phone"]:
                query_by_column(col)

        elif cmd == "s":
            show_all()

        elif cmd == "p":
            search_by_pattern()

        elif cmd == "f":
            break


menu()

cur.close()
conn.close()
