import psycopg2
import csv

conn = psycopg2.connect(
    host="localhost", dbname="lab10", user="postgres",
    password="12345678", port="5432"
)

cur = conn.cursor()

# создание таблицы 
cur.execute("""
            CREATE TABLE IF NOT EXISTS phonebook (
            user_id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            surname VARCHAR(255) NOT NULL,
            phone VARCHAR(255) NOT NULL UNIQUE
            )
""")
conn.commit()

# вставка данных 
def insert_console():
    try:
        name = input("Name: ")
        surname = input("Surname: ")
        phone = input("Phone: ")

        # дублирование номера
        cur.execute("SELECT * FROM phonebook WHERE phone = %s", (phone,))
        if cur.fetchone():
            print("Phone number already exists in the database.")
            return

        # вставка
        cur.execute("INSERT INTO phonebook (name, surname, phone) VALUES (%s, %s, %s)", (name, surname, phone))
        conn.commit()
        print("Contact added successfully.")

    except Exception as e:
        conn.rollback()  # откатить 
        print(f"Error inserting data: {e}")

# вставка данных CSV
def insert_csv():
    try:
        path = input("Enter CSV file path: ")
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                if len(row) != 3: # корректность 
                    continue

                name, surname, phone = row

                # дублирование 
                cur.execute("SELECT * FROM phonebook WHERE phone = %s", (phone,))
                if cur.fetchone():
                    print(f"Phone number {phone} already exists. Skipping entry.")
                    continue

                # вставка 
                cur.execute("INSERT INTO phonebook (name, surname, phone) VALUES (%s, %s, %s)", (name, surname, phone))
            conn.commit()
            print("Data successfully uploaded from CSV.")
    except Exception as e:
        conn.rollback()  # откатить 
        print(f"Error uploading data from CSV: {e}")

# обновление данных
def update_column(column):
    try:
        old_value = input(f"Enter current {column}: ")
        new_value = input(f"Enter new {column}: ")

        # выполнение 
        cur.execute(f"UPDATE phonebook SET {column} = %s WHERE {column} = %s", (new_value, old_value))
        conn.commit()

        print(f"{column} updated successfully.")

        cur.execute(f"SELECT * FROM phonebook WHERE {column} = %s", (new_value,))
        rows = cur.fetchall()

        if rows:
            print("Updated contact details:")
            for row in rows:
                print(row) 
        else:
            print("No contact found with the updated information.")

    except Exception as e:
        conn.rollback()  
        print(f"Error updating data: {e}")


# удаление контакта
def delete_contact():
    try:
        print("Choose the parameter for deletion:")
        print("[1] Delete by Name")
        print("[2] Delete by Surname")
        print("[3] Delete by Phone Number")

        choice = input("Enter your choice (1/2/3): ")

        if choice == "1":
            name = input("Enter name to delete: ")
            cur.execute("DELETE FROM phonebook WHERE name = %s", (name,))
        elif choice == "2":
            surname = input("Enter surname to delete: ")
            cur.execute("DELETE FROM phonebook WHERE surname = %s", (surname,))
        elif choice == "3":
            phone = input("Enter phone to delete: ")
            cur.execute("DELETE FROM phonebook WHERE phone = %s", (phone,))
        else:
            print("Invalid choice. Please choose 1, 2, or 3.")
            return
        
        conn.commit()
        print("Contact deleted successfully.")
    
    except Exception as e:
        conn.rollback()  
        print(f"Error deleting contact: {e}")

# запрос
def query_by_column(column):
    try:
        value = input(f"Enter {column}: ")
        if column == "id": 
            column = "user_id"
        cur.execute(f"SELECT * FROM phonebook WHERE {column} = %s", (value,))
        rows = cur.fetchall()
        for row in rows:
            print(row)  
    except Exception as e:
        print(f"Error querying data: {e}")

# вывод 
def show_all():
    try:
        cur.execute("SELECT * FROM phonebook")
        rows = cur.fetchall()
        for row in rows:
            print(row)  
    except Exception as e:
        print(f"Error showing all data: {e}")

def menu():
    while True:
        print("""
        === MENU ===
        [i] Insert (console or csv)
        [u] Update
        [d] Delete
        [q] Query
        [s] Show all
        [f] Finish
        """)
        cmd = input("Choose command: ").lower()

        if cmd == "i":
            opt = input('Type "csv" to upload file or "con" to enter manually: ')
            if opt == "con": insert_console()
            elif opt == "csv": insert_csv()

        elif cmd == "u":
            col = input("Which column to update (name/surname/phone): ")
            if col in ["name", "surname", "phone"]:
                update_column(col)

        elif cmd == "d":
            delete_contact()

        elif cmd == "q":
            col = input("Search by (id/name/surname/phone): ")
            if col in ["id", "name", "surname", "phone"]:
                query_by_column(col)

        elif cmd == "s":
            show_all()

        elif cmd == "f":
            break

menu()

cur.close()
conn.close()
