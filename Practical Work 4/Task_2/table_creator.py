import MyModuleCS

db = MyModuleCS.db_connection("../first")

cursor = db.cursor()
cursor.execute("""
            CREATE TABLE comment (
                id            INTEGER    PRIMARY KEY AUTOINCREMENT,
                building_id              REFERENCES building (id),
                rating       REAL,
                convenience   INTEGER,
                security      INTEGER,
                functionality INTEGER,
                comment_text  TEXT (256)
                );
            """)
db.commit()
