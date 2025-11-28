"""
📈 Predictive Analytics & Trend Forecasting
Unique Feature: Predict malnutrition risks, food waste, and budget trends
"""

import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import json

class PredictiveAnalytics:
    """
    Advanced analytics for predicting nutrition trends and risks
    """
    
    def __init__(self, db_path='nutrition_advisor.db'):
        self.db_path = db_path
    
    def predict_malnutrition_risk(self, child_id):
        """
        Predict malnutrition risk based on growth tracking data
        Returns risk level: Low, Medium, High, Critical
        """
        conn = sqlite3.connect(self.db_path)
        
        # Get growth tracking history
        query = """
            SELECT measurement_date, weight_kg, height_cm, bmi
            FROM growth_tracking
            WHERE child_id = ?
            ORDER BY measurement_date DESC
            LIMIT 6
        """
        
        df = pd.read_sql_query(query, conn, params=(child_id,))
        conn.close()
        
        if len(df) < 2:
            return {
                'risk_level': 'Unknown',
                'confidence': 0,
                'reason': 'Insufficient data'
            }
        
        # Calculate trends
        weight_trend = df['weight_kg'].iloc[0] - df['weight_kg'].iloc[-1]
        height_trend = df['height_cm'].iloc[0] - df['height_cm'].iloc[-1]
        bmi_current = df['bmi'].iloc[0]
        
        # Risk scoring
        risk_score = 0
        reasons = []
        
        # Weight loss
        if weight_trend < 0:
            risk_score += 3
            reasons.append("Weight decreasing")
        elif weight_trend < 0.5:
            risk_score += 1
            reasons.append("Weight gain is slow")
        
        # BMI below normal
        if bmi_current < 14:
            risk_score += 4
            reasons.append("BMI critically low")
        elif bmi_current < 16:
            risk_score += 2
            reasons.append("BMI below normal")
        
        # Height growth
        if height_trend < 1:
            risk_score += 1
            reasons.append("Growth stunting detected")
        
        # Determine risk level
        if risk_score >= 6:
            risk_level = 'Critical'
        elif risk_score >= 4:
            risk_level = 'High'
        elif risk_score >= 2:
            risk_level = 'Medium'
        else:
            risk_level = 'Low'
        
        return {
            'risk_level': risk_level,
            'risk_score': risk_score,
            'confidence': min(100, len(df) * 15),
            'reasons': reasons,
            'recommendation': self._get_intervention_recommendation(risk_level)
        }
    
    def _get_intervention_recommendation(self, risk_level):
        """Get intervention recommendations based on risk level"""
        recommendations = {
            'Critical': [
                "Immediate medical consultation required",
                "Increase protein intake by 50%",
                "Daily monitoring needed",
                "Consider therapeutic feeding program"
            ],
            'High': [
                "Medical checkup recommended within 1 week",
                "Increase calorie-dense foods",
                "Weekly monitoring required",
                "Add protein supplements"
            ],
            'Medium': [
                "Monitor growth monthly",
                "Ensure balanced diet",
                "Include more nutrient-rich foods",
                "Regular health checkups"
            ],
            'Low': [
                "Continue current nutrition plan",
                "Regular growth monitoring",
                "Maintain balanced diet"
            ]
        }
        return recommendations.get(risk_level, [])
    
    def forecast_food_waste(self, anganwadi_id, days=30):
        """
        Predict food waste for next period based on historical data
        """
        conn = sqlite3.connect(self.db_path)
        
        # Get historical waste data
        query = """
            SELECT date, ingredient_name, quantity_wasted_g, reason
            FROM food_waste
            WHERE anganwadi_id = ?
            AND date >= date('now', '-90 days')
            ORDER BY date
        """
        
        df = pd.read_sql_query(query, conn, params=(anganwadi_id,))
        conn.close()
        
        if len(df) == 0:
            return {
                'forecast': 'No historical data',
                'predicted_waste_kg': 0,
                'confidence': 0
            }
        
        # Calculate average daily waste
        total_waste = df['quantity_wasted_g'].sum() / 1000  # Convert to kg
        days_recorded = (pd.to_datetime(df['date'].max()) - pd.to_datetime(df['date'].min())).days
        
        if days_recorded == 0:
            days_recorded = 1
        
        avg_daily_waste = total_waste / days_recorded
        predicted_waste = avg_daily_waste * days
        
        # Identify most wasted items
        most_wasted = df.groupby('ingredient_name')['quantity_wasted_g'].sum().sort_values(ascending=False).head(5)
        
        # Analyze reasons
        reasons = df['reason'].value_counts().to_dict()
        
        return {
            'predicted_waste_kg': round(predicted_waste, 2),
            'avg_daily_waste_kg': round(avg_daily_waste, 2),
            'most_wasted_items': most_wasted.to_dict(),
            'waste_reasons': reasons,
            'recommendations': [
                f"Reduce purchase of {item} by 20%" for item in most_wasted.index[:3]
            ],
            'confidence': min(100, len(df) * 2)
        }
    
    def budget_trend_analysis(self, anganwadi_id, months=6):
        """
        Analyze budget spending trends and predict future costs
        """
        conn = sqlite3.connect(self.db_path)
        
        query = """
            SELECT created_at, total_cost, num_children
            FROM meal_plans
            WHERE created_at >= date('now', '-{} months')
            ORDER BY created_at
        """.format(months)
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        if len(df) == 0:
            return {'error': 'No data available'}
        
        df['created_at'] = pd.to_datetime(df['created_at'])
        df['cost_per_child'] = df['total_cost'] / df['num_children']
        
        # Calculate trends
        avg_cost = df['total_cost'].mean()
        avg_per_child = df['cost_per_child'].mean()
        cost_trend = 'increasing' if df['total_cost'].iloc[-1] > avg_cost else 'decreasing'
        
        # Predict next month cost
        monthly_avg = df.groupby(df['created_at'].dt.to_period('M'))['total_cost'].mean()
        predicted_next_month = monthly_avg.iloc[-1] * 1.05  # 5% inflation adjustment
        
        return {
            'avg_monthly_cost': round(avg_cost, 2),
            'avg_cost_per_child': round(avg_per_child, 2),
            'cost_trend': cost_trend,
            'predicted_next_month': round(predicted_next_month, 2),
            'savings_opportunity': round(max(0, avg_cost - (avg_per_child * df['num_children'].mean() * 0.9)), 2),
            'monthly_breakdown': monthly_avg.to_dict()
        }
    
    def immunization_coverage_prediction(self, village_id):
        """
        Predict immunization coverage and identify at-risk children
        """
        conn = sqlite3.connect(self.db_path)
        
        query = """
            SELECT 
                c.id, c.name, c.date_of_birth,
                COUNT(i.id) as total_vaccines,
                SUM(CASE WHEN i.status = 'Completed' THEN 1 ELSE 0 END) as completed_vaccines,
                SUM(CASE WHEN i.due_date < date('now') AND i.status != 'Completed' THEN 1 ELSE 0 END) as overdue_vaccines
            FROM children c
            LEFT JOIN immunisation_schedule i ON c.id = i.child_id
            WHERE c.village = ?
            GROUP BY c.id
        """
        
        df = pd.read_sql_query(query, conn, params=(village_id,))
        conn.close()
        
        if len(df) == 0:
            return {'error': 'No children data'}
        
        # Calculate coverage
        df['coverage_percentage'] = (df['completed_vaccines'] / df['total_vaccines'] * 100).fillna(0)
        
        overall_coverage = df['coverage_percentage'].mean()
        at_risk_children = df[df['overdue_vaccines'] > 0].to_dict('records')
        
        return {
            'overall_coverage': round(overall_coverage, 2),
            'total_children': len(df),
            'fully_vaccinated': len(df[df['coverage_percentage'] == 100]),
            'at_risk_count': len(at_risk_children),
            'at_risk_children': at_risk_children[:10],  # Top 10
            'predicted_coverage_3months': round(min(100, overall_coverage + 10), 2),
            'recommendation': 'Urgent action needed' if overall_coverage < 70 else 'On track'
        }


# ============================================
# FLASK ROUTES TO ADD
# ============================================
"""
Add to flask_app.py:

from predictive_analytics import PredictiveAnalytics

analytics = PredictiveAnalytics()

@app.route('/api/predict/malnutrition/<int:child_id>')
def predict_malnutrition(child_id):
    '''Predict malnutrition risk for a child'''
    prediction = analytics.predict_malnutrition_risk(child_id)
    return jsonify({
        'success': True,
        'child_id': child_id,
        'prediction': prediction
    })

@app.route('/api/predict/waste/<int:anganwadi_id>')
def predict_waste(anganwadi_id):
    '''Forecast food waste'''
    days = int(request.args.get('days', 30))
    forecast = analytics.forecast_food_waste(anganwadi_id, days)
    return jsonify({
        'success': True,
        'forecast': forecast
    })

@app.route('/api/analytics/budget/<int:anganwadi_id>')
def budget_analytics(anganwadi_id):
    '''Budget trend analysis'''
    months = int(request.args.get('months', 6))
    analysis = analytics.budget_trend_analysis(anganwadi_id, months)
    return jsonify({
        'success': True,
        'analysis': analysis
    })

@app.route('/api/predict/immunization/<int:village_id>')
def predict_immunization(village_id):
    '''Predict immunization coverage'''
    prediction = analytics.immunization_coverage_prediction(village_id)
    return jsonify({
        'success': True,
        'prediction': prediction
    })
"""
