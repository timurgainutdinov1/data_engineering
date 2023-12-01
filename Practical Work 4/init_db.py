"""
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
"""
"""
CREATE TABLE comment (
                id            INTEGER    PRIMARY KEY AUTOINCREMENT,
                building_id              REFERENCES building (id),
                rating       REAL,
                convenience   INTEGER,
                security      INTEGER,
                functionality INTEGER,
                comment_text  TEXT (256)
                );
"""
"""
CREATE TABLE music (
                id          INTEGER    PRIMARY KEY AUTOINCREMENT,
                artist      TEXT (256),
                song        TEXT (256),
                duration_ms INTEGER,
                year        INTEGER,
                tempo       REAL,
                genre       TEXT,
                explicit    TEXT
                );
"""
"""
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
"""
"""
CREATE TABLE movies_part_1 (
                id          INTEGER    PRIMARY KEY AUTOINCREMENT,
                ranking     INTEGER,
                name        TEXT (256),
                year        INTEGER,
                certificate TEXT
                );
"""
"""
CREATE TABLE movies_part_2 (
                id          INTEGER    PRIMARY KEY AUTOINCREMENT
                                REFERENCES movies_part_1 (id),
                runtime_min INTEGER,
                genre       TEXT (256),
                rating      REAL,
                metascore   INTEGER
                );
"""
"""
CREATE TABLE movies_part_3 (
                id                       INTEGER    PRIMARY KEY AUTOINCREMENT
                                            REFERENCES movies_part_1 (id),
                info                     TEXT (256),
                director                 TEXT,
                actors                   TEXT (256),
                votes                    INTEGER,
                gross_collection_mln_USD REAL
);
"""