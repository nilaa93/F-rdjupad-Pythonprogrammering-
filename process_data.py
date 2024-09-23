import requests
import pyodbc

def fetch_data_from_api():
    try:
        response = requests.get('https://jsonplaceholder.typicode.com/todos/1')
        if response.status_code == 200:
            data = response.json()
            print('Data från API har hämtats:')
            return data
        else:
            print(f'Fel vid API-anrop: {response.status_code}')
            return None
    except Exception as e:
        log_error(f'Fel vid hämtning av data från API: {e}')
        return None

def process_data(data):
    try:
        title = data['title'].strip().lower()  # Ta bort mellanslag och gör till gemener
        completed = int(data['completed'])  # Omvandla till int (1 eller 0)

        if validate_data(title, completed):
            print("Data har bearbetats!")
            return title, completed
        else:
            return None
    except Exception as e:
        log_error(f"Fel vid bearbetning av data: {e}")
        return None
    
def validate_data(title, completed):
    if not isinstance(title, str) or not title:
        log_error("Ogiltig titel!")
        return False
    if completed not in (0, 1):
        log_error("Ogiltigt värde för completed!")
        return False
    return True

def check_duplicate(title):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM todos WHERE title = ?', (title,))
    exists = cursor.fetchone()[0] > 0
    conn.close()
    return exists

def log_error(error_message):
    with open('error_log.txt', 'a') as log_file:
        log_file.write(error_message + '\n')

def create_connection():
    conn = pyodbc.connect(
        'Driver={SQL Server};'
        'Server=RAQI;'
        'Database=raqis_database;'
        'Trusted_Connection=yes;'
    )
    return conn

def create_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='todos' AND xtype='U')
        BEGIN
            CREATE TABLE todos (
                id INT IDENTITY(1,1) PRIMARY KEY,
                title NVARCHAR(255),
                completed BIT
            )
        END
    ''')
    conn.commit()

def update_database(processed_data):
    title, completed_value = processed_data
    if check_duplicate(title):
        log_error(f"Dubblett hittad för titeln: {title}")
        return  # Avbryt om dubblett finns

    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO todos (title, completed) VALUES (?, ?)', (title, completed_value))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    conn = create_connection()
    create_table(conn)
    conn.close()
    
    data = fetch_data_from_api()
    if data is not None:
        processed_data = process_data(data)
        if processed_data is not None:
            update_database(processed_data)
