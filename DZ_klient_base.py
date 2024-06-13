import psycopg2


def create_db(conn):
  
  cur = conn.cursor()
  cur.execute("""CREATE TABLE IF NOT EXISTS Clients(
              id SERIAL PRIMARY KEY,
              first_name VARCHAR(15) NOT NULL,
              last_name VARCHAR(15) NOT NULL);
              """)
  cur.execute("""
              CREATE TABLE IF NOT EXISTS Phones (
              id SERIAL PRIMARY KEY,
              client_id INTEGER PRIMARY KEY REFERENCES Clients(id),
              phones INTEGER VARCHAR(11) NOT NULL);
              """)
  cur.execute("""
              CREATE TABLE IF NOT EXISTS Emails (
              id SERIAL PRIMARY KEY,
              client_id INTEGER PRIMARY KEY REFERENCES Clients(id),
              email VARCHAR(30) NOT NULL);
              """)
  conn.commit()
  pass

def add_client(conn, first_name, last_name):
  cur = conn.cursor()
  cur.execute("""
              INSERT INTO Clients(first_name, last_name) VALUES (%s, %s);
              """)
  conn.commit()
  print ("Клиент добавлен")
  pass

def add_phone(conn, client_id, phone):
  cur = conn.cursor()
  cur.execute("""
              INSERT INTO Phones(client_id, phones) VALUES (%s, %s);
              """)
  conn.commit()
  print ("Телефон добавлен")
  pass

def change_client(conn, client_id, first_name=None, last_name=None, email=None, phones=None):
  cur = conn.cursor()
  arg_list = {first_name:first_name, last_name:last_name, email:email, phones:phones}
  for key, value in arg_list.items():
    if value is not None:
      cur.execute("""
                  UPDATE Clients SET {} = %s WHERE id = %s;
                  """.format(key), (value, client_id))
  conn.commit()
  print ("Клиент изменен")
  pass

def delete_phone(conn, client_id, phone):
  cur = conn.cursor()
  cur.execute("""
              DELETE FROM Phones WHERE id = %s; 
              """)
  print (f"У клиента {client_id} телефон удален")

def delete_client(conn, client_id):
  cur = conn.cursor()
  cur.execute("""
              DELETE FROM Phones WHERE client_id = %s; 
              """)
  cur.execute("""
              DELETE FROM Emails WHERE client_id = %s; 
              """)
  cur.execute("""
              DELETE FROM Clients WHERE id = %s;
              """)
  conn.commmit()
  print ("Клиент удален")

def find_client(cur, first_name, last_name, email = None, phone = None):
  if first_name is not None:
    cur.execute("""
                SELECT * FROM Clients WHERE first_name = %s;
                """, (first_name,))
  if last_name is not None:
    cur.execute("""
                SELECT * FROM Clients WHERE last_name = %s;
                """, (last_name,))
  if email is not None:
    cur.execute("""
                SELECT * FROM Clients WHERE email = %s;
                """, (email,))
  if phone is not None:
    cur.execute("""
                SELECT * FROM Clients WHERE phone = %s;
                """, (phone,))
  print (cur.fetchall())


with psycopg2.connect(database="clients_db", user="postgres", password="postgres") as conn:
            
  if __name__ == '__main__':
              
    create_db(conn)
    add_client(conn, "Сергей", "Иванов")
    add_phone(conn, 5, "89435667895")
    change_client(conn, 5, "Сергей", "Иванов", "qpmzj@example.com", "89116784356")
    delete_phone(conn, 5, "89115784356")
    delete_client(conn, 5)
    find_client(conn, "Сергей", "Иванов", "qpmzj@example.com", "89116784356")