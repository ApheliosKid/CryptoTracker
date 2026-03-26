import sqlite3

class DatabaseManager:
    def __init__(self, db_name="portofoliu.db"):
        self.db_name = db_name
        self.init_db()

    def _get_connection(self):
        return sqlite3.connect(self.db_name)

    def init_db(self):

        with self._get_connection() as conexiune:

            cursor = conexiune.cursor()

            cursor.execute('''CREATE TABLE IF NOT EXISTS portofoliu_crypto
                              (
                                  id
                                  INTEGER
                                  PRIMARY
                                  KEY
                                  AUTOINCREMENT,
                                  nume_moneda
                                  TEXT,
                                  pret_curent
                                  REAL,
                                  cantitate_detinuta
                                  REAL
                              )
                           ''')
            conexiune.commit()

    def adauga_in_portofoliu(self, nume_moneda, pret_achizitie, cantitate):
        with self._get_connection() as conexiune:
            cursor = conexiune.cursor()

            comanda_sql = "INSERT INTO portofoliu_crypto(nume_moneda, pret_curent, cantitate_detinuta) VALUES (?,?,?)"
            cursor.execute(comanda_sql, (nume_moneda.capitalize(), pret_achizitie, cantitate))

            conexiune.commit()

    def citeste_portofoliu(self):
        with self._get_connection() as conexiune:

            cursor = conexiune.cursor()
            cursor.execute("SELECT nume_moneda, pret_curent, cantitate_detinuta FROM portofoliu_crypto")
            return cursor.fetchall()