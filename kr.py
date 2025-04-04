import sqlite3
def create_database():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            book_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            year INTEGER,
            available INTEGER DEFAULT 1
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS readers (
            reader_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT,
            book_id INTEGER,
            FOREIGN KEY (book_id) REFERENCES books (book_id)
        )
    ''')
    conn.commit()
    conn.close()

def add_book(title, author, year):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO books (title, author, year) VALUES (?, ?, ?)
    ''', (title, author, year))
    conn.commit()
    conn.close()

def add_reader(name, phone):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO readers (name, phone) VALUES (?, ?)
    ''', (name, phone))
    conn.commit()
    conn.close()

def give_book(reader_id, book_id):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('SELECT available FROM books WHERE book_id = ?', (book_id,))
    available = cursor.fetchone()
    if available and available[0] == 1:
        cursor.execute('''
            UPDATE books SET available = 0 WHERE book_id = ?
        ''', (book_id,))
        cursor.execute('''
            UPDATE readers SET book_id = ? WHERE reader_id = ?
        ''', (book_id, reader_id))
        conn.commit()
        print(f'Книга "{book_id}" выдана читателю "{reader_id}".')
    else:
        print(f'Книга "{book_id}" недоступна.')
    conn.close()

def return_book(book_id):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE books SET available = 1 WHERE book_id = ?
    ''', (book_id,))
    cursor.execute('''
        UPDATE readers SET book_id = NULL WHERE book_id = ?
    ''', (book_id,))
    conn.commit()
    print(f'Книга "{book_id}" возвращена в библиотеку.')
    conn.close()

def get_available_books():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books WHERE available = 1')
    available_books = cursor.fetchall()
    conn.close()
    return available_books

def get_reader_books(reader_id):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT b.* FROM books b
        JOIN readers r ON b.book_id = r.book_id
        WHERE r.reader_id = ?
    ''', (reader_id,))
    reader_books = cursor.fetchall()
    conn.close()
    return reader_books

def search_books(keyword):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM books WHERE title LIKE ? OR author LIKE ?
    ''', ('%' + keyword + '%', '%' + keyword + '%'))
    search_results = cursor.fetchall()
    conn.close()
    return search_results

if __name__ == "__main__":
    create_database()

    popular_books = [
        ("Война и мир", "Лев Толстой", 1869),
        ("Преступление и наказание", "Федор Достоевский", 1866),
        ("Анна Каренина", "Лев Толстой", 1877),
        ("Мастер и Маргарита", "Михаил Булгаков", 1967),
        ("1984", "Джордж Оруэлл", 1949),
        ("Убить пересмешника", "Харпер Ли", 1960)
    ]
    for title, author, year in popular_books:
        add_book(title, author, year)
    add_reader("Алексей", "123-456-7890")
    add_reader("Мария", "098-765-4321")
    give_book(1, 1)
    print("Доступные книги:", get_available_books())
    return_book(1)
    print("Доступные книги после возврата:", get_available_books())
