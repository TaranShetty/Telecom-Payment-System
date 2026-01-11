import sqlite3

def get_db():
 conn = sqlite3.connect("telecom.db")
 conn.row_factory = sqlite3.Row
 return conn

def init_db():
    conn = get_db()
    c = conn.cursor()

    c.execute("""
              CREATE TABLE IF NOT EXISTS vendors(
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT,
              billing_cycle TEXT,
              rate REAL
              )
              """)
    c.execute("""
              CREATE TABLE IF NOT EXISTS invoices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                location TEXT,
                last_payment_date TEXT,
                pending_units INTEGER,
                rate REAL,
                pending_amount REAL
              )
              """)
              
    c.execute("""
              CREATE TABLE IF NOT EXISTS payments(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                vendor_name TEXT,
                amount REAL,
                date TEXT
              )
              """)
    conn.commit()
    conn.close()
              
if __name__ == "__main__":
    init_db()