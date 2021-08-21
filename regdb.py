import sqlite3
import logging


class WebregDB(object):

    def __init__(self, db_path: str):
        self.DEPARTMENT = "department"
        self.UPDATE_TRACKER = "update_tracker"
        self.INIT_SQL = {
            "department":
                "CREATE TABLE IF NOT EXISTS department ("
                "dept_id integer primary key AUTOINCREMENT,"
                "dept_code TEXT NOT NULL,"
                "dept_description TEXT,"
                "UNIQUE(dept_id, dept_code)"
                ")"
            , "update_tracker":
                "CREATE TABLE IF NOT EXISTS update_tracker ("
                "name TEXT NOT NULL,"
                "last_update TIMESTAMP,"
                "UNIQUE(name)"
                ")"
        }

        logging.info("Initializing webreg database")
        self.db = sqlite3.connect(db_path)
        self.db.row_factory = sqlite3.Row
        self.cursor = self.db.cursor()
        logging.info("Database connected")
        for table in self.INIT_SQL.keys():
            self.init_table(table)
        self.cursor.execute("PRAGMA synchronous = OFF")  # Safety second in this case
        logging.info("Webreg database initialized")

    def __del__(self):
        self.db.commit()
        self.db.close()

    def init_table(self, table: str):
        self.cursor.execute(self.INIT_SQL[table])
        logging.info("%s table initialized" % table)

    def clear_table(self, table: str):
        self.cursor.execute('DROP TABLE IF EXISTS ?', (table,))
        self.init_table(table)
        self.db.commit()
        logging.info("%s table cleared" % table)

    def count_rows(self, table: str):
        return int(self.cursor.execute("SELECT COUNT(*) FROM ?", (table,)))

    def get_time(self, table: str):
        return self.cursor.execute("SELECT * FROM update_tracker WHERE name=?", table)

    def update_time(self, table: str):
        self.cursor.execute("UPDATE update_tracker SET last_update=CURRENT_TIMESTAMP WHERE name=?", table)

    def update_table_time(self, table: str):
        return self.update_time(table)

    def add_department(self, dept: tuple):
        self.cursor.execute("INSERT INTO department(dept_code, dept_description) VALUES(?, ?)", dept)
