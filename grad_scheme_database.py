import sqlite3

class GradSchemeDB:
    
    def __init__(self, db_name="gradtrack.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.conn.row_factory = sqlite3.Row #makes each row behave like a dictionary
        self.cursor = self.conn.cursor()
        self.create_grad_schemes_table()
        
    def create_grad_schemes_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS grad_schemes(
        grad_scheme_id INTEGER PRIMARY KEY AUTOINCREMENT,
        company TEXT,
        scheme_name TEXT,
        location TEXT,
        salary TEXT,
        status TEXT,
        start_date DATE,
        url TEXT UNIQUE)""")
        
        self.conn.commit()
        
    def close(self):
        self.conn.close()
        
    def save_grad_scheme(self, grad_scheme):
        try:
            self.cursor.execute("""
            INSERT INTO grad_schemes (company, scheme_name, location, salary, status, start_date, url)
            VALUES (?, ?, ?, ?, ?, ?, ?) """,
            (grad_scheme.company, grad_scheme.scheme_name, grad_scheme.location, grad_scheme.salary, grad_scheme.status, grad_scheme.start_date, grad_scheme.url))
            self.conn.commit()
        except sqlite3.IntegrityError:
            pass
            #print("Duplicate job skipped")
            
    def get_schemes(self):
        self.cursor.execute("SELECT * FROM grad_schemes")
        return self.cursor.fetchall()