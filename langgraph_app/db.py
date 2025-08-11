import pymysql
from pymysql import cursors

def get_connection():
    return pymysql.connect(
        host="localhost",
        port=3307,
        user="root",
        password="",
        database="smart_hub",
        cursorclass=pymysql.cursors.DictCursor
    )

def fetch_faq_answer(query_text):
    db = get_connection()
    with db.cursor() as cursor:
        cursor.execute("SELECT answer FROM faq WHERE question LIKE %s LIMIT 1", ("%" + query_text + "%",))
        result = cursor.fetchone()
    db.close()
    return result['answer'] if result else None

def log_ai_response(user_query, ai_response):
    db = get_connection()
    with db.cursor() as cursor:
        cursor.execute("INSERT INTO ai_logs (user_query, ai_response) VALUES (%s, %s)", (user_query, ai_response))
        db.commit()
    db.close()