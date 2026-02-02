import sqlite3
import json
from datetime import datetime

class HistoryManager:
    def __init__(self, db_path="kashrut_history.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS scans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                product_name TEXT,
                status TEXT,
                category TEXT,
                details TEXT,
                is_favorite INTEGER DEFAULT 0
            )
        ''')
        conn.commit()
        conn.close()

    def add_scan(self, result):
        """
        Guarda un resultado en el historial.
        """
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Extract fields safely from result (which is a dict)
        product_name = result.get('producto', 'Desconocido')
        status = result.get('resultado', 'Dudoso')
        category = result.get('categoria', 'Desconocido')
        details = json.dumps(result, ensure_ascii=False) # Store full JSON for retrieval

        c.execute('''
            INSERT INTO scans (timestamp, product_name, status, category, details)
            VALUES (?, ?, ?, ?, ?)
        ''', (timestamp, product_name, status, category, details))
        
        conn.commit()
        conn.close()

    def delete_scan(self, scan_id):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('DELETE FROM scans WHERE id = ?', (scan_id,))
        conn.commit()
        conn.close()

    def get_history(self, limit=50):
        """
        Recupera los últimos escaneos.
        """
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('SELECT * FROM scans ORDER BY id DESC LIMIT ?', (limit,))
        rows = c.fetchall()
        conn.close()
        
        history = []
        for row in rows:
            history.append({
                "id": row[0],
                "timestamp": row[1],
                "product_name": row[2],
                "status": row[3],
                "category": row[4],
                "details": json.loads(row[5]),
                "is_favorite": bool(row[6])
            })
        return history

    def clear_history(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('DELETE FROM scans')
        conn.commit()
        conn.close()
