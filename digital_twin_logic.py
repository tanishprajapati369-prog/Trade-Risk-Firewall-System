import sqlite3

def get_or_create_digital_twin(conn: sqlite3.Connection, user_id: int):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM digital_twin WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    if row:
        return dict(row)
    
    cursor.execute(
        "INSERT INTO digital_twin (user_id, total_trades, win_rate, median_qty, consecutive_losses, fomo_score) VALUES (?, 0, 0.50, 1.0, 0, 0.10)",
        (user_id,)
    )
    conn.commit()
    return {
        "user_id": user_id, "total_trades": 0, "win_rate": 0.50,
        "median_qty": 1.0, "consecutive_losses": 0, "fomo_score": 0.10
    }