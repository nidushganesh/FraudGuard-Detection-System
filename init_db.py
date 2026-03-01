import sqlite3

def initialize_database():
    # Establishing connection to the local SQLite database
    conn = sqlite3.connect('fraudguard.db')
    cursor = conn.cursor()

    # 1. Transactions Table: Stores ML-generated scores and transaction details
    # Focuses on the London-Colombo corridor (GBP/LKR)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Transactions (
            alert_id TEXT PRIMARY KEY,
            transaction_type TEXT,
            amount REAL,
            currency TEXT,
            risk_score REAL,
            status TEXT DEFAULT 'Pending'
        )
    ''')

    # 2. Audit_Logs Table: Provides non-repudiation for analyst actions
    # This table satisfies the accountability requirements of GDPR
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Audit_Logs (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            alert_id TEXT,
            action_taken TEXT,
            analyst_id TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (alert_id) REFERENCES Transactions (alert_id)
        )
    ''')

    # 3. Seed Data: Sample records for testing the dashboard
    sample_data = [
        ('A1023', 'International', 450.00, 'GBP', 0.92, 'Pending'),
        ('A1024', 'High Frequency', 12000.00, 'LKR', 0.87, 'Pending'),
        ('A1025', 'Merchant Anomaly', 75.50, 'GBP', 0.65, 'Pending')
    ]

    cursor.executemany('''
        INSERT OR IGNORE INTO Transactions 
        (alert_id, transaction_type, amount, currency, risk_score, status) 
        VALUES (?, ?, ?, ?, ?, ?)
    ''', sample_data)

    conn.commit()
    conn.close()
    print("Database initialized successfully with 3NF Audit Tables.")

if __name__ == "__main__":
    initialize_database()