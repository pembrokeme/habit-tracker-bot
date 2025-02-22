import sqlite3
import datetime
from typing import List, Optional, Tuple

class HabitDatabase:
    def __init__(self, db_path: str = "habits.db"):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """Initialize the database with required tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create habits table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT 1
            )
        ''')

        # Create habit_logs table for tracking completions
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS habit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                completion_date DATE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (habit_id) REFERENCES habits (id),
                UNIQUE(habit_id, completion_date)
            )
        ''')

        conn.commit()
        conn.close()

    def add_habit(self, user_id: int, name: str, description: str = "") -> int:
        """Add a new habit for a user."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO habits (user_id, name, description)
            VALUES (?, ?, ?)
        ''', (user_id, name, description))

        habit_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return habit_id

    def get_user_habits(self, user_id: int) -> List[Tuple]:
        """Get all active habits for a user."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id, name, description, created_at
            FROM habits
            WHERE user_id = ? AND is_active = 1
            ORDER BY created_at DESC
        ''', (user_id,))

        habits = cursor.fetchall()
        conn.close()
        return habits

    def log_habit_completion(self, user_id: int, habit_id: int, date: str = None) -> bool:
        """Log a habit completion for a specific date."""
        if date is None:
            date = datetime.date.today().isoformat()

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute('''
                INSERT INTO habit_logs (habit_id, user_id, completion_date)
                VALUES (?, ?, ?)
            ''', (habit_id, user_id, date))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            # Habit already completed for this date
            conn.close()
            return False

    def get_habit_stats(self, user_id: int, habit_id: int) -> dict:
        """Get statistics for a specific habit."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Get total completions
        cursor.execute('''
            SELECT COUNT(*) FROM habit_logs
            WHERE habit_id = ? AND user_id = ?
        ''', (habit_id, user_id))
        total_completions = cursor.fetchone()[0]

        # Get current streak
        cursor.execute('''
            SELECT completion_date FROM habit_logs
            WHERE habit_id = ? AND user_id = ?
            ORDER BY completion_date DESC
        ''', (habit_id, user_id))

        dates = [row[0] for row in cursor.fetchall()]
        current_streak = self._calculate_streak(dates)

        conn.close()
        return {
            'total_completions': total_completions,
            'current_streak': current_streak
        }

    def get_all_user_stats(self, user_id: int) -> dict:
        """Get overall statistics for a user."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Get total habits
        cursor.execute('''
            SELECT COUNT(*) FROM habits
            WHERE user_id = ? AND is_active = 1
        ''', (user_id,))
        total_habits = cursor.fetchone()[0]

        # Get total completions this week
        cursor.execute('''
            SELECT COUNT(*) FROM habit_logs hl
            JOIN habits h ON hl.habit_id = h.id
            WHERE hl.user_id = ? AND hl.completion_date >= date('now', '-7 days')
        ''', (user_id,))
        weekly_completions = cursor.fetchone()[0]

        # Get completion rate for active habits today
        cursor.execute('''
            SELECT COUNT(DISTINCT hl.habit_id) FROM habit_logs hl
            JOIN habits h ON hl.habit_id = h.id
            WHERE hl.user_id = ? AND hl.completion_date = date('now')
            AND h.is_active = 1
        ''', (user_id,))
        today_completions = cursor.fetchone()[0]

        completion_rate = (today_completions / total_habits * 100) if total_habits > 0 else 0

        conn.close()
        return {
            'total_habits': total_habits,
            'weekly_completions': weekly_completions,
            'today_completions': today_completions,
            'completion_rate': completion_rate
        }

    def _calculate_streak(self, dates: List[str]) -> int:
        """Calculate current streak from a list of completion dates."""
        if not dates:
            return 0

        today = datetime.date.today()
        streak = 0

        for i, date_str in enumerate(dates):
            date = datetime.date.fromisoformat(date_str)
            expected_date = today - datetime.timedelta(days=i)

            if date == expected_date:
                streak += 1
            else:
                break

        return streak