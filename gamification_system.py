"""
🎮 Gamification System for Children & Anganwadi Workers
Unique Feature: Make nutrition fun with rewards, achievements, and leaderboards
"""

import sqlite3
from datetime import datetime
import json

class NutritionGamification:
    """
    Gamification engine to encourage healthy eating habits
    """
    
    def __init__(self, db_path='nutrition_advisor.db'):
        self.db_path = db_path
        self.init_gamification_tables()
    
    def init_gamification_tables(self):
        """Create tables for gamification"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Achievements table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS achievements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                icon TEXT,
                points INTEGER DEFAULT 10,
                category TEXT,
                requirement TEXT
            )
        """)
        
        # User achievements
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_achievements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                achievement_id INTEGER,
                earned_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (achievement_id) REFERENCES achievements(id)
            )
        """)
        
        # Points table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_points (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                points INTEGER DEFAULT 0,
                level INTEGER DEFAULT 1,
                total_meals_completed INTEGER DEFAULT 0,
                streak_days INTEGER DEFAULT 0,
                last_activity TIMESTAMP
            )
        """)
        
        # Leaderboard
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS leaderboard (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                username TEXT,
                total_points INTEGER,
                rank INTEGER,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
        
        # Initialize achievements
        self.create_default_achievements()
    
    def create_default_achievements(self):
        """Create default achievements"""
        achievements = [
            # Eating achievements
            ("🥗 Veggie Lover", "Ate vegetables for 7 days straight", "🥗", 50, "Eating", "7_day_veggie_streak"),
            ("🥛 Milk Master", "Drank milk every day for a week", "🥛", 30, "Eating", "7_day_milk"),
            ("🍎 Fruit Fan", "Ate fruits 5 times this week", "🍎", 40, "Eating", "5_fruits_week"),
            ("💪 Protein Power", "Met protein goals for 10 days", "💪", 60, "Eating", "10_day_protein"),
            ("🌟 Balanced Eater", "Completed all meals for a month", "🌟", 100, "Eating", "30_day_complete"),
            
            # Growth achievements
            ("📈 Growing Strong", "Gained healthy weight this month", "📈", 70, "Growth", "weight_gain"),
            ("📏 Height Hero", "Grew 2cm in 3 months", "📏", 80, "Growth", "height_growth"),
            ("💚 Healthy BMI", "Maintained healthy BMI for 3 months", "💚", 90, "Growth", "healthy_bmi"),
            
            # Worker achievements
            ("👨‍🍳 Master Chef", "Prepared 100 meals", "👨‍🍳", 120, "Worker", "100_meals"),
            ("📊 Data Wizard", "Logged 50 meal plans", "📊", 80, "Worker", "50_plans"),
            ("⭐ 5-Star Rating", "Got 5-star feedback 10 times", "⭐", 150, "Worker", "10_five_stars"),
            ("🎯 Zero Waste", "Achieved zero food waste for a week", "🎯", 100, "Worker", "zero_waste_week"),
            
            # Community achievements
            ("🤝 Helper", "Helped other Anganwadis 5 times", "🤝", 60, "Community", "help_5_times"),
            ("🌍 Eco Warrior", "Reduced waste by 50%", "🌍", 110, "Community", "waste_reduction"),
            ("🏆 Champion", "Top of leaderboard for a month", "🏆", 200, "Community", "leaderboard_top"),
        ]
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for ach in achievements:
            cursor.execute("""
                INSERT OR IGNORE INTO achievements 
                (name, description, icon, points, category, requirement)
                VALUES (?, ?, ?, ?, ?, ?)
            """, ach)
        
        conn.commit()
        conn.close()
    
    def award_points(self, user_id, points, reason):
        """Award points to user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get current points
        cursor.execute("SELECT points, level FROM user_points WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()
        
        if result:
            current_points, current_level = result
            new_points = current_points + points
            new_level = self._calculate_level(new_points)
            
            cursor.execute("""
                UPDATE user_points 
                SET points = ?, level = ?, last_activity = ?
                WHERE user_id = ?
            """, (new_points, new_level, datetime.now(), user_id))
        else:
            new_points = points
            new_level = 1
            cursor.execute("""
                INSERT INTO user_points (user_id, points, level, last_activity)
                VALUES (?, ?, ?, ?)
            """, (user_id, new_points, new_level, datetime.now()))
        
        conn.commit()
        conn.close()
        
        # Check for new achievements
        self.check_achievements(user_id)
        
        return {
            'points_awarded': points,
            'total_points': new_points,
            'level': new_level,
            'reason': reason,
            'level_up': new_level > current_level if result else False
        }
    
    def _calculate_level(self, points):
        """Calculate level based on points"""
        # Level 1: 0-99, Level 2: 100-299, Level 3: 300-599, etc.
        if points < 100:
            return 1
        elif points < 300:
            return 2
        elif points < 600:
            return 3
        elif points < 1000:
            return 4
        elif points < 1500:
            return 5
        else:
            return 6 + (points - 1500) // 500
    
    def unlock_achievement(self, user_id, achievement_id):
        """Unlock achievement for user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if already unlocked
        cursor.execute("""
            SELECT id FROM user_achievements 
            WHERE user_id = ? AND achievement_id = ?
        """, (user_id, achievement_id))
        
        if cursor.fetchone():
            conn.close()
            return {'already_unlocked': True}
        
        # Unlock achievement
        cursor.execute("""
            INSERT INTO user_achievements (user_id, achievement_id)
            VALUES (?, ?)
        """, (user_id, achievement_id))
        
        # Get achievement details
        cursor.execute("""
            SELECT name, description, points FROM achievements WHERE id = ?
        """, (achievement_id,))
        
        achievement = cursor.fetchone()
        
        conn.commit()
        conn.close()
        
        # Award points
        if achievement:
            self.award_points(user_id, achievement[2], f"Achievement: {achievement[0]}")
        
        return {
            'unlocked': True,
            'achievement_name': achievement[0] if achievement else 'Unknown',
            'points_earned': achievement[2] if achievement else 0
        }
    
    def check_achievements(self, user_id):
        """Check if user qualifies for new achievements"""
        # This would check various conditions
        # For example: check eating streak, meal completions, etc.
        pass
    
    def get_leaderboard(self, limit=10, category='all'):
        """Get leaderboard rankings"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = """
            SELECT 
                user_id,
                (SELECT name FROM users WHERE id = user_id) as username,
                points,
                level,
                ROW_NUMBER() OVER (ORDER BY points DESC) as rank
            FROM user_points
            ORDER BY points DESC
            LIMIT ?
        """
        
        cursor.execute(query, (limit,))
        leaderboard = cursor.fetchall()
        
        conn.close()
        
        return [
            {
                'rank': row[4],
                'user_id': row[0],
                'username': row[1] or f"User {row[0]}",
                'points': row[2],
                'level': row[3]
            }
            for row in leaderboard
        ]
    
    def get_user_stats(self, user_id):
        """Get comprehensive user statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get points and level
        cursor.execute("""
            SELECT points, level, total_meals_completed, streak_days
            FROM user_points WHERE user_id = ?
        """, (user_id,))
        
        stats = cursor.fetchone()
        
        # Get achievements count
        cursor.execute("""
            SELECT COUNT(*) FROM user_achievements WHERE user_id = ?
        """, (user_id,))
        
        achievements_count = cursor.fetchone()[0]
        
        # Get total achievements available
        cursor.execute("SELECT COUNT(*) FROM achievements")
        total_achievements = cursor.fetchone()[0]
        
        # Get rank
        cursor.execute("""
            SELECT COUNT(*) + 1
            FROM user_points
            WHERE points > (SELECT points FROM user_points WHERE user_id = ?)
        """, (user_id,))
        
        rank = cursor.fetchone()[0]
        
        conn.close()
        
        if not stats:
            return {
                'points': 0,
                'level': 1,
                'rank': rank,
                'achievements': 0,
                'total_achievements': total_achievements,
                'meals_completed': 0,
                'streak_days': 0
            }
        
        return {
            'points': stats[0],
            'level': stats[1],
            'rank': rank,
            'achievements': achievements_count,
            'total_achievements': total_achievements,
            'achievements_percentage': round(achievements_count / total_achievements * 100, 1) if total_achievements > 0 else 0,
            'meals_completed': stats[2],
            'streak_days': stats[3],
            'next_level_points': self._points_for_next_level(stats[1])
        }
    
    def _points_for_next_level(self, current_level):
        """Calculate points needed for next level"""
        level_thresholds = [0, 100, 300, 600, 1000, 1500, 2000, 2500]
        if current_level < len(level_thresholds):
            return level_thresholds[current_level]
        return (current_level - 5) * 500 + 1500


# ============================================
# FLASK ROUTES TO ADD
# ============================================
"""
Add to flask_app.py:

from gamification_system import NutritionGamification

gamification = NutritionGamification()

@app.route('/gamification')
def gamification_page():
    '''Gamification dashboard'''
    return render_template('gamification.html')

@app.route('/api/gamification/award-points', methods=['POST'])
def award_points():
    '''Award points to user'''
    data = request.json
    result = gamification.award_points(
        user_id=data['user_id'],
        points=data['points'],
        reason=data['reason']
    )
    return jsonify({'success': True, 'result': result})

@app.route('/api/gamification/leaderboard')
def get_leaderboard():
    '''Get leaderboard'''
    limit = int(request.args.get('limit', 10))
    leaderboard = gamification.get_leaderboard(limit)
    return jsonify({'success': True, 'leaderboard': leaderboard})

@app.route('/api/gamification/stats/<int:user_id>')
def get_user_stats(user_id):
    '''Get user statistics'''
    stats = gamification.get_user_stats(user_id)
    return jsonify({'success': True, 'stats': stats})

@app.route('/api/gamification/unlock/<int:user_id>/<int:achievement_id>', methods=['POST'])
def unlock_achievement(user_id, achievement_id):
    '''Unlock achievement'''
    result = gamification.unlock_achievement(user_id, achievement_id)
    return jsonify({'success': True, 'result': result})
"""
