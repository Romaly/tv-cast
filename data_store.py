import sqlite3

DB_NAME = 'movies_db.db'


def init():
    with sqlite3.connect(DB_NAME) as sql_conn:
        sql_request = """CREATE TABLE IF NOT EXISTS movies_link (
            id integer PRIMARY KEY AUTOINCREMENT,
            provider text NOT NULL,
            title text NOT NULL,
            movie_page_url text NOT NULL,
            image_url text NOT NULL,
            duration text NOT NULL,
            rating text NOT NULL,
            year text NOT NULL,
            country text NOT NULL,
            genre text NOT NULL,
            additional_info text NOT NULL,
            description text NOT NULL,
            UNIQUE(provider, title, year)
        );"""
        sql_conn.execute(sql_request)


def insert(provider, title, movie_page_url, image_url, duration, rating, year, country, genre, additional_info, description):
    with sqlite3.connect(DB_NAME) as sql_conn:
        try:
            sql_request = """INSERT INTO movies_link(provider, title, movie_page_url, image_url, duration, rating, year, country, genre, additional_info, description) VALUES(?,?,?,?,?,?,?,?,?,?,?)"""
            sql_conn.execute(sql_request, [provider, title, movie_page_url, image_url,
                                           duration, rating, year, country, str(genre), additional_info, description])
            sql_conn.commit()
        except Exception as e:
            print(e)


def find_by_title(title, count, page):
    with sqlite3.connect(DB_NAME) as sql_conn:
        try:
            sql_request = """SELECT COUNT(*) FROM movies_link WHERE title like '%'||?||'%'"""
            sql_cursor = sql_conn.execute(sql_request, [title])
            total = sql_cursor.fetchall()[0][0]
            print('total: ', total)

            sql_request = """SELECT * FROM movies_link WHERE title like '%'||?||'%' ORDER BY title LIMIT ? OFFSET ? """
            sql_cursor = sql_conn.execute(
                sql_request, [title, count, page * count - count])
            return {
                'count': count,
                'page': page,
                'total': total,
                'data': sql_cursor.fetchall()
            }
        except Exception as e:
            print(e)
