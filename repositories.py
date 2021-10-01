import sqlite3


class CategoryRepository:
    def get_list_all_category_with_id(self):
        with sqlite3.connect('database.db') as connection:
            cursor = connection.cursor()
            cursor.execute('''SELECT 
                    id,
                    name
                FROM 
                    category
                ORDER BY id ASC;
            ''')
            return cursor.fetchall()

    def save_new_category(self, name):
        with sqlite3.connect('database.db') as connection:
            cursor = connection.cursor()
            cursor.execute(
                'INSERT INTO category(`name`) '
                'VALUES(?)', (
                    (name,)
                ))
            connection.commit()


class EntryRepository:
    def save(self, title, author, category_id, year_of_release, number_of_pages):
        with sqlite3.connect('database.db') as connection:
            cursor = connection.cursor()
            cursor.execute(
                'INSERT INTO entry(`title`, `author`, `category_id`, `year_of_release`, `number_of_pages`) '
                'VALUES(?, ?, ?, ?, ?)', (
                    title,
                    author,
                    category_id,
                    year_of_release,
                    number_of_pages
                ))
            connection.commit()

    def save_new_read_page(self, book_id, new_last_read_page):
        with sqlite3.connect('database.db') as connection:
            cursor = connection.cursor()
            cursor.execute('''
                UPDATE 
                    entry
                SET 
                    last_read_page = ?,
                    last_day_of_reading = CURRENT_TIMESTAMP
                WHERE 
                    id = ?;
                ''', (new_last_read_page, book_id))

            return cursor.fetchone()

    def get_book_id_with_pages(self):
        with sqlite3.connect('database.db') as connection:
            cursor = connection.cursor()
            cursor.execute(
                '''SELECT 
                    id,
                    STRFTIME('%d/%m/%Y-%H:%M', last_day_of_reading), 
                    last_read_page,
                    number_of_pages
                FROM 
                    entry;''')

            return cursor.fetchall()

    def delete(self, id):
        with sqlite3.connect('database.db') as connection:
            cursor = connection.cursor()
            cursor.execute(
                'DELETE FROM entry WHERE id=?', (
                    (id,)
                ))
            connection.commit()

    def get_book_id(self, id):
        with sqlite3.connect('database.db') as connection:
            cursor = connection.cursor()
            cursor.execute(
                'SELECT `id` FROM entry WHERE `id`=?', (
                    (id,)
                ))

            return cursor.fetchall()

    def get_list_all_books(self):
        with sqlite3.connect('database.db') as connection:
            cursor = connection.cursor()
            cursor.execute('''SELECT 
                    entry.id,
                    entry.title,
                    entry.author,
                    category.name,
                    entry.year_of_release,
                    STRFTIME('%d/%m/%Y - %H:%M', entry.last_day_of_reading), 
                    entry.last_read_page,
                    entry.number_of_pages,
                    entry.status TEXT 
                FROM 
                    entry 
                LEFT JOIN category ON entry.category_id = category.id 
                ORDER BY title ASC;
            ''')
            return cursor.fetchall()

    def save_lend_book(self, id, status):
        with sqlite3.connect('database.db') as connection:
            cursor = connection.cursor()
            cursor.execute('''
                UPDATE 
                    entry
                SET 
                    status = ?
                WHERE 
                    id = ?;
                ''', (status, id))

            return cursor.fetchone()

    def get_back_lend_book(self, id, status):
        with sqlite3.connect('database.db') as connection:
            cursor = connection.cursor()
            cursor.execute('''
                UPDATE 
                    entry
                SET 
                    status = ?
                WHERE 
                    id = ?;
                ''', (status, id))

            return cursor.fetchone()

    def report_books(self):
        with sqlite3.connect('database.db') as connection:
            cursor = connection.cursor()
            cursor.execute(
                '''SELECT 
                    id,
                    status 
                FROM 
                    entry;''')

            return cursor.fetchall()