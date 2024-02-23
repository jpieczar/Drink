import sqlite3

conn = sqlite3.connect("dataBase.db")
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS `patrons` (
    `id`        INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    `patron`    TINYTEXT NOT NULL,
    `id_number` TINYTEXT NOT NULL CHECK(length(id_number) = 13),
    `saturation` REAL NOT NULL,
    `weight`    INTEGER NOT NULL
)
""")
conn.commit()

c.execute("""CREATE TABLE IF NOT EXISTS `drinks` (
    `id`        INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    `price`     INTEGER NOT NULL,
    `drink`     TINYTEXT NOT NULL,
    `ABV`       INTEGER NOT NULL,
    `patron`    TINYTEXT NOT NULL
)
""")
conn.commit()

c.execute("""INSERT INTO `patrons` (patron, id_number, saturation, weight) VALUES ('bob', '1234567891123', 0, 80)""")
conn.commit()

c.execute("""INSERT INTO `drinks` (price, drink, ABV, patron) VALUES (10, 'water', 0, 'bob')""")
conn.commit()

c.close()
conn.close()