import sqlite3
import sys

def create_db():
    # 데이터베이스 생성
    conn = sqlite3.connect("database.db")
    # print("Opened database successfully")

    # 테이블 생성
    conn.execute('''
        CREATE TABLE IF NOT EXISTS KEYWORDS(
            KEYWORD TEXT PRIMARY KEY,
            LASTSEARCHED TEXT DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS RESULTS(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            KEYWORD TEXT,
            TITLE TEXT,
            COMPANY TEXT,
            LOCATION TEXT,
            TIME TEXT,
            LINK TEXT,
            FOREIGN KEY(KEYWORD) REFERENCES KEYWORDS
        );
    ''')
    # print("Created table successfully")

    conn.commit()
    conn.close()


def get_keywords():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT KEYWORD FROM KEYWORDS;")
    rows = cur.fetchall()
    cur.close()
    return [r[0] for r in rows]


def get_results(keyword):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM RESULTS WHERE KEYWORD = ?;", (keyword,))
    rows = cur.fetchall()
    res = []
    for r in rows:
        res.append({
            "title": r[2],
            "company": r[3],
            "location": r[4],
            "time": r[5],
            "link": r[6]
        })
    cur.close()
    return res


def add_result(keyword, jobs):
    try:
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO KEYWORDS(KEYWORD) VALUES(?);", (keyword,))
        for job in jobs:
            cur.execute('''
                    INSERT INTO RESULTS(
                        KEYWORD, 
                        TITLE,
                        COMPANY,
                        LOCATION,
                        TIME,
                        LINK
                    ) VALUES(?,?,?,?,?,?);
                ''', 
                (keyword, 
                job["title"], 
                job["company"], 
                job["location"],
                job["time"],
                job["link"])
            )
        conn.commit()
        # print("add_result success")
    except:
        conn.rollback()
        # print("add_result failed", sys.exc_info())
    finally:
        conn.close()


def delete_result(keyword):
    try:
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute("DELETE FROM KEYWORDS WHERE KEYWORD = ?;", (keyword,))
        cur.execute("DELETE FROM RESULTS WHERE KEYWORD = ?", (keyword,))
        conn.commit()
        # print("delete_result success")
    except:
        conn.rollback()
        # print("delete_result failed", sys.exc_info())
    finally:
        conn.close()