import os, mysql.connector as mc
from dotenv import load_dotenv
load_dotenv()                          # pull env vars into os.environ

def get_conn():
    return mc.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", 3306)),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME"),
        auth_plugin="mysql_native_password",
        pool_name="genie_pool",
        pool_size=5,
    )

def run(query, params=(), fetchone=False, fetchall=False):
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute(query, params)
    data = None
    if fetchone:
        data = cur.fetchone()
    elif fetchall:
        data = cur.fetchall()
    conn.commit()
    cur.close(); conn.close()
    return data
