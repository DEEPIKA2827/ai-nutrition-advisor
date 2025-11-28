"""
Recipe Suggestions Feature
Simple recipes using ingredients from meal plans
"""

# 🍳 SIMPLE INDIAN RECIPES FOR ANGANWADI

RECIPES = {
    "Dal Tadka": {
        "category": "Main Course",
        "ingredients": {
            "Toor Dal": 200,  # grams
            "Onion": 50,
            "Tomato": 100,
            "Oil": 15,
            "Turmeric": 2,
            "Salt": 5
        },
        "instructions": [
            "Wash toor dal and pressure cook with water for 3-4 whistles",
            "Heat oil in a pan, add chopped onions and fry till golden",
            "Add chopped tomatoes, turmeric, salt and cook till soft",
            "Add cooked dal and mix well",
            "Boil for 2-3 minutes and serve hot"
        ],
        "cooking_time": 30,  # minutes
        "servings": 4,
        "difficulty": "Easy",
        "meal_type": "Lunch/Dinner",
        "nutrition_per_serving": {
            "calories": 180,
            "protein": 11,
            "carbs": 28,
            "fat": 4
        }
    },
    
    "Vegetable Khichdi": {
        "category": "Main Course",
        "ingredients": {
            "Rice": 150,
            "Moong Dal": 100,
            "Potato": 100,
            "Carrot": 50,
            "Green Beans": 50,
            "Oil": 10,
            "Turmeric": 2,
            "Salt": 5
        },
        "instructions": [
            "Wash rice and dal together",
            "Chop all vegetables into small pieces",
            "In a pressure cooker, add rice, dal, vegetables, turmeric, salt",
            "Add water (3 cups) and pressure cook for 3 whistles",
            "Let it cool, then open and mix well",
            "Serve hot with curd or pickle"
        ],
        "cooking_time": 25,
        "servings": 4,
        "difficulty": "Easy",
        "meal_type": "Lunch/Dinner",
        "nutrition_per_serving": {
            "calories": 220,
            "protein": 8,
            "carbs": 40,
            "fat": 3
        }
    },
    
    "Ragi Porridge": {
        "category": "Breakfast",
        "ingredients": {
            "Ragi": 50,
            "Milk": 250,
            "Jaggery": 20,
            "Cardamom": 1
        },
        "instructions": [
            "Dry roast ragi flour till aromatic",
            "Boil milk in a pan",
            "Add roasted ragi flour slowly while stirring",
            "Cook for 5 minutes, stirring continuously",
            "Add jaggery and cardamom powder",
            "Serve warm"
        ],
        "cooking_time": 15,
        "servings": 2,
        "difficulty": "Easy",
        "meal_type": "Breakfast",
        "nutrition_per_serving": {
            "calories": 210,
            "protein": 7,
            "carbs": 38,
            "fat": 4
        }
    },
    
    "Vegetable Pulao": {
        "category": "Main Course",
        "ingredients": {
            "Rice": 200,
            "Mixed Vegetables": 150,
            "Onion": 50,
            "Oil": 20,
            "Whole Spices": 5,
            "Salt": 5
        },
        "instructions": [
            "Wash and soak rice for 15 minutes",
            "Heat oil, add whole spices (bay leaf, cardamom, cloves)",
            "Add sliced onions and fry till golden",
            "Add chopped vegetables and fry for 2 minutes",
            "Add drained rice and mix gently",
            "Add water (2 cups), salt and cook till rice is done"
        ],
        "cooking_time": 30,
        "servings": 4,
        "difficulty": "Medium",
        "meal_type": "Lunch",
        "nutrition_per_serving": {
            "calories": 240,
            "protein": 5,
            "carbs": 45,
            "fat": 5
        }
    },
    
    "Poha": {
        "category": "Breakfast/Snack",
        "ingredients": {
            "Poha": 150,
            "Onion": 50,
            "Potato": 100,
            "Oil": 15,
            "Peanuts": 30,
            "Turmeric": 2,
            "Salt": 5
        },
        "instructions": [
            "Wash poha gently and drain water",
            "Heat oil, add peanuts and fry till crispy",
            "Add chopped onions and diced potatoes",
            "Add turmeric, salt and cover till potatoes are cooked",
            "Add washed poha and mix gently",
            "Cover and cook for 2 minutes",
            "Serve hot with lemon juice"
        ],
        "cooking_time": 20,
        "servings": 4,
        "difficulty": "Easy",
        "meal_type": "Breakfast",
        "nutrition_per_serving": {
            "calories": 190,
            "protein": 4,
            "carbs": 32,
            "fat": 6
        }
    },
    
    "Banana Milkshake": {
        "category": "Beverage",
        "ingredients": {
            "Banana": 100,
            "Milk": 200,
            "Sugar": 10
        },
        "instructions": [
            "Peel and chop banana",
            "Add banana, milk, and sugar to a blender",
            "Blend till smooth and frothy",
            "Serve immediately"
        ],
        "cooking_time": 5,
        "servings": 1,
        "difficulty": "Easy",
        "meal_type": "Snack",
        "nutrition_per_serving": {
            "calories": 185,
            "protein": 7,
            "carbs": 32,
            "fat": 4
        }
    },
    
    "Mixed Vegetable Curry": {
        "category": "Main Course",
        "ingredients": {
            "Potato": 100,
            "Carrot": 50,
            "Green Beans": 50,
            "Peas": 50,
            "Onion": 50,
            "Tomato": 100,
            "Oil": 15,
            "Spices": 5
        },
        "instructions": [
            "Chop all vegetables into bite-size pieces",
            "Heat oil, add chopped onions and fry",
            "Add tomatoes and cook till soft",
            "Add all vegetables and spices",
            "Add water and cook till vegetables are tender",
            "Serve hot with roti or rice"
        ],
        "cooking_time": 25,
        "servings": 4,
        "difficulty": "Easy",
        "meal_type": "Lunch/Dinner",
        "nutrition_per_serving": {
            "calories": 120,
            "protein": 3,
            "carbs": 18,
            "fat": 4
        }
    },
    
    "Egg Bhurji": {
        "category": "Protein Dish",
        "ingredients": {
            "Eggs": 4,
            "Onion": 50,
            "Tomato": 50,
            "Oil": 10,
            "Spices": 3,
            "Salt": 3
        },
        "instructions": [
            "Beat eggs with salt",
            "Heat oil, add chopped onions and fry",
            "Add chopped tomatoes and spices",
            "Pour beaten eggs and scramble continuously",
            "Cook till eggs are done",
            "Serve hot with bread or roti"
        ],
        "cooking_time": 10,
        "servings": 2,
        "difficulty": "Easy",
        "meal_type": "Breakfast/Dinner",
        "nutrition_per_serving": {
            "calories": 220,
            "protein": 14,
            "carbs": 6,
            "fat": 16
        }
    }
}

# 🔧 FLASK ROUTE TO ADD TO flask_app.py

"""
Add this to your flask_app.py:

from recipes import RECIPES

@app.route('/recipes')
def recipes():
    '''Display all recipes'''
    return render_template('recipes.html', recipes=RECIPES)

@app.route('/api/recipes/search')
def search_recipes():
    '''Search recipes by ingredients'''
    ingredients = request.args.get('ingredients', '').split(',')
    matching_recipes = {}
    
    for recipe_name, recipe_data in RECIPES.items():
        recipe_ingredients = recipe_data['ingredients'].keys()
        # Check if any user ingredient matches recipe ingredients
        if any(ing.strip() in recipe_ingredients for ing in ingredients):
            matching_recipes[recipe_name] = recipe_data
    
    return jsonify({
        'success': True,
        'recipes': matching_recipes,
        'count': len(matching_recipes)
    })

@app.route('/api/recipe/<recipe_name>')
def get_recipe(recipe_name):
    '''Get specific recipe details'''
    recipe = RECIPES.get(recipe_name)
    if recipe:
        return jsonify({
            'success': True,
            'recipe': recipe
        })
    return jsonify({
        'success': False,
        'error': 'Recipe not found'
    }), 404
"""

# 📄 HTML TEMPLATE TO CREATE: templates/recipes.html

RECIPES_HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Recipes - AI Nutrition Advisor</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
</head>
<body>
    {% extends "base.html" %}
    
    {% block content %}
    <div class="container mt-5">
        <h1 class="mb-4"><i class="fas fa-utensils"></i> Simple Recipes for Anganwadi</h1>
        
        <!-- Search Box -->
        <div class="row mb-4">
            <div class="col-md-6">
                <input type="text" class="form-control" id="searchRecipes" 
                       placeholder="Search recipes...">
            </div>
        </div>
        
        <!-- Recipe Cards -->
        <div class="row">
            {% for recipe_name, recipe_data in recipes.items() %}
            <div class="col-md-6 col-lg-4 mb-4">
                <div class="card h-100 shadow-sm recipe-card">
                    <div class="card-body">
                        <h5 class="card-title">{{ recipe_name }}</h5>
                        <span class="badge bg-success mb-2">{{ recipe_data.category }}</span>
                        <span class="badge bg-info mb-2">{{ recipe_data.difficulty }}</span>
                        
                        <p class="card-text">
                            <small class="text-muted">
                                <i class="fas fa-clock"></i> {{ recipe_data.cooking_time }} mins
                                | <i class="fas fa-users"></i> {{ recipe_data.servings }} servings
                            </small>
                        </p>
                        
                        <button class="btn btn-primary btn-sm" 
                                onclick="showRecipe('{{ recipe_name }}')">
                            View Recipe
                        </button>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
    
    <!-- Recipe Modal -->
    <div class="modal fade" id="recipeModal" tabindex="-1">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="recipeModalTitle"></h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body" id="recipeModalBody">
                    <!-- Recipe details will be loaded here -->
                </div>
            </div>
        </div>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        function showRecipe(recipeName) {
            fetch(`/api/recipe/${recipeName}`)
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        const recipe = data.recipe;
                        document.getElementById('recipeModalTitle').textContent = recipeName;
                        
                        let html = `
                            <h6>Ingredients:</h6>
                            <ul>
                        `;
                        
                        for (const [ingredient, quantity] of Object.entries(recipe.ingredients)) {
                            html += `<li>${ingredient}: ${quantity}g</li>`;
                        }
                        
                        html += `</ul><h6>Instructions:</h6><ol>`;
                        
                        recipe.instructions.forEach(step => {
                            html += `<li>${step}</li>`;
                        });
                        
                        html += `</ol>
                            <h6>Nutrition (per serving):</h6>
                            <p>Calories: ${recipe.nutrition_per_serving.calories} kcal | 
                               Protein: ${recipe.nutrition_per_serving.protein}g | 
                               Carbs: ${recipe.nutrition_per_serving.carbs}g | 
                               Fat: ${recipe.nutrition_per_serving.fat}g</p>
                        `;
                        
                        document.getElementById('recipeModalBody').innerHTML = html;
                        new bootstrap.Modal(document.getElementById('recipeModal')).show();
                    }
                });
        }
        
        // Search functionality
        document.getElementById('searchRecipes').addEventListener('input', function(e) {
            const searchTerm = e.target.value.toLowerCase();
            document.querySelectorAll('.recipe-card').forEach(card => {
                const recipeName = card.querySelector('.card-title').textContent.toLowerCase();
                if (recipeName.includes(searchTerm)) {
                    card.parentElement.style.display = 'block';
                } else {
                    card.parentElement.style.display = 'none';
                }
            });
        });
    </script>
    {% endblock %}
</body>
</html>
"""

# 💾 Save the HTML template
if __name__ == "__main__":
    with open('templates/recipes.html', 'w', encoding='utf-8') as f:
        f.write(RECIPES_HTML_TEMPLATE)
    print("✅ recipes.html template created!")
    print("✅ Add the Flask routes to flask_app.py")
    print("✅ Add navigation link in base.html")
