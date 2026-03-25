import sqlite3

def init_db():
    conexiune = sqlite3.connect("portofoliu.db")

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
    conexiune.close()

def adauga_in_portofoliu(nume_moneda, pret_achizitie, cantitate):
    conexiune = sqlite3.connect("portofoliu.db")
    cursor = conexiune.cursor()

    comanda_sql = "INSERT INTO portofoliu_crypto(nume_moneda, pret_curent, cantitate_detinuta) VALUES (?,?,?)"
    cursor.execute(comanda_sql, (nume_moneda.capitalize(), pret_achizitie, cantitate))

    conexiune.commit()
    conexiune.close()

def citeste_portofoliu():
    conexiune = sqlite3.connect("portofoliu.db")
    cursor = conexiune.cursor()

    cursor.execute("SELECT nume_moneda, pret_curent, cantitate_detinuta FROM portofoliu_crypto")
    date_portfoliu = cursor.fetchall()

    conexiune.close()
    return date_portfoliu