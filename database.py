import sqlite3

def init_db():
    """Creează baza de date și tabelul de scoruri dacă nu există."""
    conn = sqlite3.connect('scoruri_joc.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS statistici (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            jucator1 TEXT,
            jucator2 TEXT,
            scor_j1 INTEGER DEFAULT 0,
            scor_j2 INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def get_score(j1, j2):
    """Caută dacă acești doi jucători au mai jucat și returnează scorul."""
    conn = sqlite3.connect('scoruri_joc.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT scor_j1, scor_j2 FROM statistici 
        WHERE (jucator1=? AND jucator2=?) OR (jucator1=? AND jucator2=?)
    ''', (j1, j2, j2, j1))
    result = cursor.fetchone()
    conn.close()
    return result if result else (0, 0)

def update_score(j1, j2, castigator_nume):
    """Actualizează scorul în baza de date."""
    conn = sqlite3.connect('scoruri_joc.db')
    cursor = conn.cursor()
    
    current = get_score(j1, j2)
    
    cursor.execute('''
        SELECT id FROM statistici 
        WHERE (jucator1=? AND jucator2=?) OR (jucator1=? AND jucator2=?)
    ''', (j1, j2, j2, j1))
    row = cursor.fetchone()

    if not row:
        s1 = 1 if castigator_nume == j1 else 0
        s2 = 1 if castigator_nume == j2 else 0
        cursor.execute('INSERT INTO statistici (jucator1, jucator2, scor_j1, scor_j2) VALUES (?, ?, ?, ?)', 
                       (j1, j2, s1, s2))
    else:
        if castigator_nume == j1:
            cursor.execute('UPDATE statistici SET scor_j1 = scor_j1 + 1 WHERE id = ?', (row[0],))
        elif castigator_nume == j2:
            cursor.execute('UPDATE statistici SET scor_j2 = scor_j2 + 1 WHERE id = ?', (row[0],))
            
    conn.commit()
    conn.close()