import MyModuleCS

db = MyModuleCS.db_connection("../third")

cursor = db.cursor()
cursor.execute("""
            CREATE TABLE product (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                name        TEXT    UNIQUE,
                price       REAL,
                quantity    INTEGER,
                category    TEXT,
                fromCity    TEXT,
                isAvailable TEXT,
                views       INTEGER,
                version     INTEGER DEFAULT (1) 
                );
            """)
db.commit()
