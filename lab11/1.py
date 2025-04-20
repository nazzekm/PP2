import psycopg2
import csv

conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="12345678",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        number VARCHAR(20) UNIQUE NOT NULL
    );
""")
conn.commit()

# поиск контактов 
create_function_sql = """
CREATE OR REPLACE FUNCTION search_contacts(pattern TEXT)
RETURNS TABLE(id INTEGER, name VARCHAR, number VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT c.id, c.name, c.number
    FROM contacts as c
    WHERE c.name ILIKE '%' || pattern || '%' OR c.number ILIKE '%' || pattern || '%';
END;
$$ LANGUAGE plpgsql;
"""

cur.execute(create_function_sql)
conn.commit()

# добавление или обновление
text_for_procedure = """
CREATE OR REPLACE PROCEDURE add_or_update_contact(p_name VARCHAR, p_number VARCHAR)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM contacts WHERE name = p_name) THEN
        UPDATE contacts
        SET number = p_number
        WHERE name = p_name;
    ELSIF EXISTS (SELECT 1 FROM contacts WHERE number = p_number) THEN
        UPDATE contacts
        SET name = p_name
        WHERE number = p_number;
    ELSE
        INSERT INTO contacts(name, number)
        VALUES (p_name, p_number);
    END IF;
END;
$$;
"""

cur.execute(text_for_procedure)
conn.commit()

# удаление данных
text_for_delete_procedure = """
CREATE OR REPLACE PROCEDURE delete_data(dna VARCHAR, dnum VARCHAR)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM contacts as c
    WHERE (dna IS NOT NULL AND c.name = dna)
        OR (dnum IS NOT NULL AND c.number = dnum);
END;
$$;
"""

cur.execute(text_for_delete_procedure)
conn.commit()

csv_file_path = "C:\\Users\\User\\Desktop\\code\\git-lessons\\lab10\\phonebook.csv"
 

with open(csv_file_path, 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  

    for row in reader:
        name = row[0]
        number = row[1]

        cur.execute("INSERT INTO contacts (name, number) VALUES (%s, %s);", (name, number))

conn.commit()

print("Данные успешно загружены в базу данных.")

pattern = input("Введите имя или часть номера: ")
cur.execute("SELECT * FROM search_contacts(%s);", (pattern,))
results = cur.fetchall()

if results:
    print("\nНайденные контакты:\n---------------------------")
    print("id\tname\tnumber\n---------------------------")
    for row in results:
        print(f"{row[0]}\t{row[1]}\t{row[2]}")
    print("---------------------------")
else:
    print("Совпадений не найдено.")

name = input("Введите имя для добавления или обновления: ")
number = input("Введите номер телефона: ")
cur.execute("CALL add_or_update_contact(%s, %s);", (name, number))
conn.commit()
print("Контакт добавлен или обновлен.")

name = input("Введите имя для удаления (или оставьте пустым): ")
number = input("Введите номер для удаления (или оставьте пустым): ")

name = name if name != "" else None
number = number if number != "" else None

if name is None and number is None:
    print("Нужно ввести хотя бы имя или номер.")
else:
    cur.execute("CALL delete_data(%s, %s);", (name, number))
    conn.commit()
    print("Контакт удалён, если он существовал.")

cur.close()
conn.close()
