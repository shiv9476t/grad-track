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
            
    def upsert_grad_scheme(self, grad_scheme):
        self.cursor.execute("""
        INSERT INTO grad_schemes (company, scheme_name, location, salary, status, start_date, url)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(url) DO UPDATE SET
        location = excluded.location,
        salary = excluded.salary,
        status = excluded.status""",
        (grad_scheme.company, grad_scheme.scheme_name, grad_scheme.location, grad_scheme.salary, grad_scheme.status, grad_scheme.start_date, grad_scheme.url))
        self.conn.commit()
            
    def get_schemes(self):
        self.cursor.execute("SELECT * FROM grad_schemes")
        return self.cursor.fetchall()
    
    def get_schemes_by_industry(self, industry):
        self.cursor.execute("SELECT * FROM grad_schemes WHERE industry LIKE ?",
                           (f"%{industry}%",))
        return self.cursor.fetchall()
    
    def add_industry_column(self):
        try:
            self.cursor.execute("ALTER TABLE grad_schemes ADD COLUMN industry TEXT")
            self.conn.commit()
        except:
            print("error")
            pass  # column already exists

    def update_industry(self, scheme_name, industry):
        self.cursor.execute("""
        UPDATE grad_schemes SET industry = ? WHERE scheme_name = ?""",
                           (industry, scheme_name))
        self.conn.commit()
    
    def get_scheme_names(self):
        self.cursor.execute("SELECT scheme_name FROM grad_schemes")
        return self.cursor.fetchall()
    
    def clear_industries(self):
        self.cursor.execute("UPDATE grad_schemes SET industry = NULL")
        self.conn.commit()
        
