import MyModuleCS

db = MyModuleCS.db_connection("../first")

cursor = db.cursor()
cursor.execute("""
            CREATE TABLE building (
                id         INTEGER    PRIMARY KEY AUTOINCREMENT,
                name       TEXT (256),
                street     TEXT (256),
                city       TEXT (256),
                zipcode    INTEGER,
                floors     INTEGER,
                year       INTEGER,
                parking    TEXT,
                prob_price INTEGER,
                views      INTEGER
                );
            """)
db.commit()
