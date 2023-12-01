import MyModuleCS

db = MyModuleCS.db_connection("../fourth")

cursor = db.cursor()

cursor.execute("""
            CREATE TABLE movies_part_1 (
                id          INTEGER    PRIMARY KEY AUTOINCREMENT,
                ranking     INTEGER,
                name        TEXT (256),
                year        INTEGER,
                certificate TEXT
                );
            """)
db.commit()

cursor.execute("""
            CREATE TABLE movies_part_2 (
                id          INTEGER    PRIMARY KEY AUTOINCREMENT
                                REFERENCES movies_part_1 (id),
                runtime_min INTEGER,
                genre       TEXT (256),
                rating      REAL,
                metascore   INTEGER
                );
            """)
db.commit()

cursor.execute("""
            CREATE TABLE movies_part_3 (
                id                       INTEGER    PRIMARY KEY AUTOINCREMENT
                                            REFERENCES movies_part_1 (id),
                info                     TEXT (256),
                director                 TEXT,
                actors                   TEXT (256),
                votes                    INTEGER,
                gross_collection_mln_USD REAL
                );
            """)
db.commit()
