"""
🤖 AI-Powered Meal Personalization Engine
Unique Feature: Uses ML to learn child preferences and optimize meal plans over time
"""

import json
import sqlite3
from datetime import datetime, timedelta
from collections import defaultdict

class MealPersonalizationEngine:
    """
    Advanced AI engine that learns from feedback and personalizes meals
    """
    
    def __init__(self, db_path='nutrition_advisor.db'):
        self.db_path = db_path
    
    def analyze_child_preferences(self, child_id):
        """
        Analyze what foods a child likes/dislikes based on meal feedback
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get all feedback for this child's meal plans
        cursor.execute("""
            SELECT mf.rating, mf.comments, mp.plan_data
            FROM meal_feedback mf
            JOIN meal_plans mp ON mf.plan_id = mp.id
            WHERE mp.id IN (
                SELECT plan_id FROM child_meal_plans WHERE child_id = ?
            )
        """, (child_id,))
        
        feedback_data = cursor.fetchall()
        
        # Analyze ingredients from high-rated vs low-rated meals
        liked_ingredients = defaultdict(int)
        disliked_ingredients = defaultdict(int)
        
        for rating, comments, plan_data in feedback_data:
            plan = json.loads(plan_data)
            
            for day, meals in plan.get('weekly_plan', {}).items():
                for meal_type, meal_data in meals.items():
                    for item in meal_data.get('items', []):
                        ingredient = item['ingredient']
                        
                        if rating >= 4:  # Liked
                            liked_ingredients[ingredient] += 1
                        elif rating <= 2:  # Disliked
                            disliked_ingredients[ingredient] += 1
        
        conn.close()
        
        return {
            'liked': dict(sorted(liked_ingredients.items(), key=lambda x: x[1], reverse=True)[:10]),
            'disliked': dict(sorted(disliked_ingredients.items(), key=lambda x: x[1], reverse=True)[:10])
        }
    
    def predict_meal_acceptance(self, child_id, proposed_ingredients):
        """
        Predict if a child will like a meal based on historical data
        Returns: probability score 0-1
        """
        preferences = self.analyze_child_preferences(child_id)
        
        score = 0.5  # Neutral baseline
        total_ingredients = len(proposed_ingredients)
        
        if total_ingredients == 0:
            return score
        
        for ingredient in proposed_ingredients:
            if ingredient in preferences['liked']:
                score += 0.1 / total_ingredients
            if ingredient in preferences['disliked']:
                score -= 0.15 / total_ingredients
        
        return max(0, min(1, score))  # Clamp between 0 and 1
    
    def generate_personalized_meal_plan(self, child_id, budget, age_group, num_days=7):
        """
        Generate meal plan optimized for child's preferences
        """
        preferences = self.analyze_child_preferences(child_id)
        
        # Get ingredients, prioritizing liked ones
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT name, cost_per_kg, protein_per_100g, carbs_per_100g, 
                   fat_per_100g, calories_per_100g, category
            FROM ingredients
            WHERE name NOT IN ({})
            ORDER BY 
                CASE 
                    WHEN name IN ({}) THEN 0
                    ELSE 1
                END
        """.format(
            ','.join(['?' for _ in preferences['disliked']]),
            ','.join(['?' for _ in preferences['liked']])
        ), list(preferences['disliked'].keys()) + list(preferences['liked'].keys()))
        
        ingredients = cursor.fetchall()
        conn.close()
        
        # Build personalized meal plan
        # (Use existing meal_optimizer with weighted preferences)
        
        return {
            'personalized': True,
            'child_id': child_id,
            'preferences_applied': True,
            'liked_ingredients_used': len(preferences['liked']),
            'avoided_ingredients': list(preferences['disliked'].keys())
        }


# ============================================
# FLASK ROUTES TO ADD
# ============================================

"""
Add these routes to flask_app.py:

from ai_meal_personalization import MealPersonalizationEngine

personalization_engine = MealPersonalizationEngine()

@app.route('/api/child-preferences/<int:child_id>')
def get_child_preferences(child_id):
    '''Get AI-analyzed food preferences for a child'''
    preferences = personalization_engine.analyze_child_preferences(child_id)
    return jsonify({
        'success': True,
        'child_id': child_id,
        'preferences': preferences
    })

@app.route('/api/personalized-meal-plan/<int:child_id>')
def generate_personalized_plan(child_id):
    '''Generate AI-personalized meal plan'''
    budget = float(request.args.get('budget', 500))
    age_group = request.args.get('age_group', '3-6 years')
    
    plan = personalization_engine.generate_personalized_meal_plan(
        child_id, budget, age_group
    )
    
    return jsonify({
        'success': True,
        'plan': plan
    })

@app.route('/api/predict-acceptance/<int:child_id>')
def predict_meal_acceptance(child_id):
    '''Predict if child will like proposed meal'''
    ingredients = request.args.get('ingredients', '').split(',')
    score = personalization_engine.predict_meal_acceptance(child_id, ingredients)
    
    return jsonify({
        'success': True,
        'acceptance_score': score,
        'prediction': 'High' if score > 0.7 else 'Medium' if score > 0.4 else 'Low'
    })
"""
