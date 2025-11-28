# 🚀 Guide: Adding New Features & Fixing Nutrition Data

## 📊 Method 1: Fix Nutrition Data with USDA API

### Step 1: Get Free API Key
1. Go to: https://fdc.nal.usda.gov/api-key-signup.html
2. Sign up for a free API key
3. You'll receive it via email instantly

### Step 2: Add API Key to Your Project
Create a file called `.env` in the project folder:
```
USDA_API_KEY=your_api_key_here
GEMINI_API_KEY=your_gemini_key_here (optional)
```

### Step 3: Use the USDA API (Already Built-in!)
The app already has `usda_api.py`. You can now:
- Search for foods and get accurate nutrition data
- Auto-populate ingredient database with real values
- Verify existing data against USDA database

---

## 📝 Method 2: Manually Update Nutrition Data

### Edit `database.py` (Lines 170-350)

Replace the fake data with accurate values from:
- **IFCT 2017** (Indian Food Composition Tables)
- **USDA Food Database**
- **NIN India** (National Institute of Nutrition)

Example of accurate data for Rice (per 100g):
```python
("Rice, raw", "Grains", 45, 6.8, 78.2, 0.5, 345, 0.2, 0.7, 10, 100),
```

---

## 🎯 New Features You Can Add

### Feature 1: Recipe Suggestions
**What it does:** Suggest actual recipes using the meal plan ingredients

**How to add:**
1. Create `recipes.py`:
```python
RECIPES = {
    "Dal Tadka": {
        "ingredients": ["Toor Dal", "Onion", "Tomato", "Oil"],
        "instructions": "...",
        "cooking_time": 30,
        "servings": 4
    }
}
```

2. Add route in `flask_app.py`:
```python
@app.route('/recipes')
def recipes():
    return render_template('recipes.html', recipes=RECIPES)
```

3. Create `templates/recipes.html`

---

### Feature 2: Shopping List Generator
**What it does:** Create a shopping list from the meal plan

**How to add:**
Add to `flask_app.py`:
```python
@app.route('/api/shopping-list/<int:plan_id>')
def generate_shopping_list(plan_id):
    # Get meal plan
    # Aggregate all ingredients
    # Calculate total quantities
    # Return as PDF/CSV
    pass
```

---

### Feature 3: Food Allergen Alerts
**What it does:** Warn if meal plan contains allergens

**Already exists!** Just enhance it:
1. Edit `database.py` - add allergen data to ingredients
2. Add allergen checking in `meal_optimizer.py`
3. Display warnings in the UI

---

### Feature 4: Meal Photos/Images
**What it does:** Show photos of suggested meals

**How to add:**
1. Create `static/images/meals/` folder
2. Add image URLs to ingredients table
3. Display in `templates/index.html`

---

### Feature 5: SMS Reminders for Vaccination
**What it does:** Send SMS reminders to parents

**How to add:**
1. Install: `pip install twilio` (or use India's SMS APIs like MSG91, Fast2SMS)
2. Create `sms_service.py`:
```python
def send_vaccination_reminder(phone, child_name, vaccine, date):
    # Send SMS
    pass
```

3. Add to `flask_app.py`:
```python
@app.route('/api/send-reminders')
def send_reminders():
    # Check due vaccinations
    # Send SMS to parents
    pass
```

---

### Feature 6: Parent/Anganwadi Worker Login
**What it does:** Secure access with user accounts

**How to add:**
1. Install: `pip install flask-login`
2. Add users table to `database.py`
3. Add authentication routes
4. Protect sensitive routes

---

### Feature 7: Nutrition Comparison Tool
**What it does:** Compare different meal plans side-by-side

**How to add:**
1. Add route in `flask_app.py`:
```python
@app.route('/compare')
def compare_plans():
    plans = db.get_all_meal_plans()
    return render_template('compare.html', plans=plans)
```

2. Create comparison charts using Chart.js

---

### Feature 8: Food Waste Tracker
**What it does:** Track what food gets wasted to optimize future plans

**How to add:**
1. Add table in `database.py`:
```python
CREATE TABLE food_waste (
    id INTEGER PRIMARY KEY,
    plan_id INTEGER,
    ingredient_name TEXT,
    quantity_wasted_g REAL,
    reason TEXT,
    date DATE
)
```

2. Add waste tracking UI
3. Use data to optimize future meal plans

---

### Feature 9: Seasonal Food Suggestions
**What it does:** Suggest seasonal ingredients (cheaper & fresher)

**How to add:**
1. Add `season` field to ingredients
2. Filter ingredients by current month
3. Prioritize seasonal items in meal plans

---

### Feature 10: Multi-Language Support (Already 50% done!)
**What it does:** Support Hindi, Kannada, Tamil, etc.

**Already exists!** Just needs:
1. Gemini API key for translation
2. Or use Google Translate API
3. Add more language translations in `translator.py`

---

### Feature 11: Print-Friendly Meal Plans
**What it does:** Generate printer-friendly meal plans for Anganwadis

**How to add:**
1. Create `templates/print_plan.html` (simple, no colors)
2. Add CSS for print: `@media print { ... }`
3. Add Print button in UI

---

### Feature 12: Nutrition Quiz/Education
**What it does:** Teach Anganwadi workers about nutrition

**How to add:**
1. Create `quiz.py` with questions
2. Add route for quiz
3. Track scores and certificates

---

### Feature 13: Budget Comparison Report
**What it does:** Compare costs across different vendors/markets

**How to add:**
1. Add `price_history` table
2. Track ingredient prices over time
3. Show trends and best buying times

---

### Feature 14: WhatsApp Integration
**What it does:** Send meal plans via WhatsApp

**How to add:**
1. Use WhatsApp Business API or Twilio
2. Add "Share to WhatsApp" button
3. Format meal plan for WhatsApp message

---

### Feature 15: AI Chatbot Enhancement
**What it does:** Better AI assistant with Gemini

**Already exists!** Just needs:
1. Get Gemini API key from: https://makersuite.google.com/app/apikey
2. Add to `.env` file
3. Restart the app

---

## 🛠️ Quick Start: Pick Your First Feature

### Easiest to Add (Start Here):
1. **Shopping List** - 30 minutes
2. **Print-Friendly View** - 20 minutes  
3. **Seasonal Suggestions** - 1 hour

### Most Impactful:
1. **SMS Reminders** - Very useful for parents
2. **Recipe Suggestions** - Makes meal plans practical
3. **Food Photos** - Visual appeal

### Most Advanced:
1. **User Authentication** - Security & personalization
2. **WhatsApp Integration** - Better reach
3. **AI Chatbot** - Intelligent assistance

---

## 📞 Need Help?

1. Check existing code in the project - many features are partially built
2. Use AI to help you code (like me!)
3. Read Flask documentation: https://flask.palletsprojects.com/

## 🎓 Learning Resources

- Flask Tutorial: https://flask.palletsprojects.com/tutorial/
- Chart.js Docs: https://www.chartjs.org/docs/
- Bootstrap Docs: https://getbootstrap.com/docs/
- Python SQLite: https://docs.python.org/3/library/sqlite3.html

---

**Ready to build? Pick a feature and let's code it together!** 🚀
