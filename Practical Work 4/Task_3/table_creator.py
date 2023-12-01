import MyModuleCS

db = MyModuleCS.db_connection("../second")

cursor = db.cursor()
cursor.execute("""
            CREATE TABLE music (
                id          INTEGER    PRIMARY KEY AUTOINCREMENT,
                artist      TEXT (256),
                song        TEXT (256),
                duration_ms INTEGER,
                year        INTEGER,
                tempo       REAL,
                genre       TEXT
                );
            """)
db.commit()
