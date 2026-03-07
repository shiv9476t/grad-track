import sqlite3

class JobDatabase:
    
    def __init__(self, db_name="jobs.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.create_jobs_table()
        
    def create_jobs_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs(
        job_id INTEGER PRIMARY KEY AUTOINCREMENT,
        company TEXT,
        title TEXT,
        location TEXT,
        salary TEXT,
        status TEXT,
        url TEXT UNIQUE)""")
        
        self.conn.commit()
        
    def close(self):
        self.conn.close()
        
    def save_job(self, job):
        try:
            self.cursor.execute("""
            INSERT INTO jobs (company, title, location, salary, status, url)
            VALUES (?, ?, ?, ?, ?) """,
            (job.company, job.title, job.location, job.salary, job.status, job.url))
            self.conn.commit()
        except sqlite3.IntegrityError:
            pass
            #print("Duplicate job skipped")