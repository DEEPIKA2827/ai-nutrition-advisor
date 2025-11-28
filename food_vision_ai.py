"""
📸 Computer Vision for Food Recognition & Portion Estimation
Unique Feature: Take photo of plate, AI identifies foods and calculates nutrition
"""

import cv2
import numpy as np
from PIL import Image
import io

class FoodVisionAI:
    """
    Computer Vision for food recognition and nutrition estimation
    Uses image analysis to identify foods and estimate portions
    """
    
    def __init__(self):
        self.food_colors = {
            'Rice': [(245, 245, 245), (255, 255, 255)],  # White
            'Dal': [(200, 180, 100), (255, 220, 150)],   # Yellow
            'Spinach': [(50, 100, 50), (100, 180, 100)], # Green
            'Carrot': [(200, 100, 50), (255, 150, 100)], # Orange
            'Tomato': [(150, 50, 50), (255, 100, 100)],  # Red
        }
    
    def analyze_plate_image(self, image_path):
        """
        Analyze plate image and identify foods
        """
        # Load image
        img = cv2.imread(image_path)
        if img is None:
            return {'error': 'Could not load image'}
        
        # Convert to HSV for better color detection
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        # Detect plate (circular shape)
        plate_info = self._detect_plate(img)
        
        # Identify food items by color regions
        foods_detected = self._identify_foods(img, hsv)
        
        # Estimate portions based on area
        portions = self._estimate_portions(foods_detected, plate_info)
        
        # Calculate nutrition
        nutrition = self._calculate_nutrition_from_portions(portions)
        
        return {
            'foods_detected': list(foods_detected.keys()),
            'portions': portions,
            'nutrition': nutrition,
            'plate_diameter_cm': plate_info['diameter_cm'],
            'confidence': self._calculate_confidence(foods_detected)
        }
    
    def _detect_plate(self, img):
        """
        Detect circular plate in image
        """
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (9, 9), 2)
        
        circles = cv2.HoughCircles(
            blurred,
            cv2.HOUGH_GRADIENT,
            dp=1,
            minDist=100,
            param1=50,
            param2=30,
            minRadius=50,
            maxRadius=500
        )
        
        if circles is not None:
            circles = np.uint16(np.around(circles))
            largest_circle = max(circles[0], key=lambda x: x[2])
            
            # Estimate plate diameter (assuming standard 25cm plate)
            diameter_pixels = largest_circle[2] * 2
            diameter_cm = 25  # Standard plate
            
            return {
                'center': (largest_circle[0], largest_circle[1]),
                'radius': largest_circle[2],
                'diameter_cm': diameter_cm,
                'pixels_per_cm': diameter_pixels / diameter_cm
            }
        
        return {
            'diameter_cm': 25,
            'pixels_per_cm': 10
        }
    
    def _identify_foods(self, img, hsv):
        """
        Identify foods based on color regions
        """
        foods_found = {}
        
        for food_name, (lower_color, upper_color) in self.food_colors.items():
            # Create mask for this color range
            lower = np.array(lower_color)
            upper = np.array(upper_color)
            
            mask = cv2.inRange(img, lower, upper)
            
            # Calculate area of detected color
            area = cv2.countNonZero(mask)
            
            if area > 1000:  # Minimum threshold
                foods_found[food_name] = {
                    'area_pixels': area,
                    'color_match': True
                }
        
        return foods_found
    
    def _estimate_portions(self, foods_detected, plate_info):
        """
        Estimate portion sizes based on area
        """
        portions = {}
        pixels_per_cm = plate_info.get('pixels_per_cm', 10)
        
        for food_name, food_data in foods_detected.items():
            area_pixels = food_data['area_pixels']
            area_cm2 = area_pixels / (pixels_per_cm ** 2)
            
            # Estimate portion size
            # Assuming 1cm² of food on plate ≈ 5-10g depending on density
            portion_g = area_cm2 * 7  # Average density factor
            
            portions[food_name] = {
                'grams': round(portion_g, 1),
                'area_cm2': round(area_cm2, 1)
            }
        
        return portions
    
    def _calculate_nutrition_from_portions(self, portions):
        """
        Calculate nutrition from detected portions
        """
        # Nutrition data per 100g (simplified)
        nutrition_db = {
            'Rice': {'calories': 130, 'protein': 2.7, 'carbs': 28, 'fat': 0.3},
            'Dal': {'calories': 116, 'protein': 9, 'carbs': 20, 'fat': 0.4},
            'Spinach': {'calories': 23, 'protein': 2.9, 'carbs': 3.6, 'fat': 0.4},
            'Carrot': {'calories': 41, 'protein': 0.9, 'carbs': 10, 'fat': 0.2},
            'Tomato': {'calories': 18, 'protein': 0.9, 'carbs': 3.9, 'fat': 0.2},
        }
        
        total_nutrition = {
            'calories': 0,
            'protein': 0,
            'carbs': 0,
            'fat': 0
        }
        
        for food_name, portion_data in portions.items():
            grams = portion_data['grams']
            if food_name in nutrition_db:
                for nutrient, value in nutrition_db[food_name].items():
                    total_nutrition[nutrient] += (value * grams / 100)
        
        # Round values
        for key in total_nutrition:
            total_nutrition[key] = round(total_nutrition[key], 1)
        
        return total_nutrition
    
    def _calculate_confidence(self, foods_detected):
        """
        Calculate confidence score for detection
        """
        if not foods_detected:
            return 0
        
        # Higher confidence with more foods detected
        confidence = min(95, 50 + len(foods_detected) * 10)
        return confidence
    
    def generate_nutrition_label(self, analysis_result):
        """
        Generate visual nutrition label from analysis
        """
        from PIL import Image, ImageDraw, ImageFont
        
        # Create image
        img = Image.new('RGB', (400, 500), color='white')
        draw = ImageDraw.Draw(img)
        
        # Try to load font, fallback to default
        try:
            font_large = ImageFont.truetype("arial.ttf", 24)
            font_medium = ImageFont.truetype("arial.ttf", 18)
            font_small = ImageFont.truetype("arial.ttf", 14)
        except:
            font_large = ImageFont.load_default()
            font_medium = ImageFont.load_default()
            font_small = ImageFont.load_default()
        
        # Draw title
        draw.text((20, 20), "Nutrition Facts", fill='black', font=font_large)
        draw.line([(20, 60), (380, 60)], fill='black', width=2)
        
        # Draw foods detected
        y_pos = 80
        draw.text((20, y_pos), "Foods Detected:", fill='black', font=font_medium)
        y_pos += 30
        
        for food in analysis_result['foods_detected']:
            portion = analysis_result['portions'][food]['grams']
            draw.text((40, y_pos), f"• {food}: {portion}g", fill='black', font=font_small)
            y_pos += 25
        
        # Draw nutrition
        y_pos += 20
        draw.line([(20, y_pos), (380, y_pos)], fill='black', width=2)
        y_pos += 20
        
        nutrition = analysis_result['nutrition']
        draw.text((20, y_pos), f"Calories: {nutrition['calories']} kcal", fill='black', font=font_medium)
        y_pos += 30
        draw.text((20, y_pos), f"Protein: {nutrition['protein']}g", fill='black', font=font_small)
        y_pos += 25
        draw.text((20, y_pos), f"Carbs: {nutrition['carbs']}g", fill='black', font=font_small)
        y_pos += 25
        draw.text((20, y_pos), f"Fat: {nutrition['fat']}g", fill='black', font=font_small)
        
        # Save
        img.save('nutrition_label.png')
        return 'nutrition_label.png'


class PortionSizeGuide:
    """
    AR-style portion size guide using hand reference
    """
    
    def __init__(self):
        self.hand_based_portions = {
            'Palm': '3oz protein (chicken, fish) = 85g',
            'Fist': '1 cup vegetables or fruits = 150g',
            'Cupped Hand': '1/2 cup rice or grains = 75g',
            'Thumb': '1 tablespoon oil or butter = 15ml',
            'Handful': '1oz nuts or snacks = 30g',
            'Two Hands': '1 large salad = 200g'
        }
    
    def detect_hand_in_image(self, image_path):
        """
        Detect hand in image for portion comparison
        """
        import mediapipe as mp
        
        # Initialize MediaPipe Hands
        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands(static_image_mode=True, max_num_hands=1)
        
        # Load image
        img = cv2.imread(image_path)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Detect hands
        results = hands.process(img_rgb)
        
        if results.multi_hand_landmarks:
            # Hand detected
            hand_landmarks = results.multi_hand_landmarks[0]
            
            # Calculate hand size (palm width)
            palm_width = self._calculate_palm_width(hand_landmarks, img.shape)
            
            return {
                'hand_detected': True,
                'palm_width_cm': palm_width,
                'portion_reference': 'Palm-sized portion'
            }
        
        return {'hand_detected': False}
    
    def _calculate_palm_width(self, landmarks, img_shape):
        """
        Calculate palm width from landmarks
        """
        # Simplified: use distance between wrist and middle finger base
        # Average human palm is 8-10cm
        return 9.0  # Average


# ============================================
# INSTALLATION REQUIRED
# ============================================
"""
pip install opencv-python
pip install Pillow
pip install mediapipe  # For hand detection
"""

# ============================================
# FLASK ROUTES TO ADD
# ============================================
"""
Add to flask_app.py:

from food_vision_ai import FoodVisionAI, PortionSizeGuide

food_vision = FoodVisionAI()
portion_guide = PortionSizeGuide()

@app.route('/food-scanner')
def food_scanner_page():
    '''Food scanner page'''
    return render_template('food_scanner.html')

@app.route('/api/scan-food', methods=['POST'])
def scan_food():
    '''Scan food from image'''
    if 'image' not in request.files:
        return jsonify({'success': False, 'error': 'No image uploaded'}), 400
    
    file = request.files['image']
    
    # Save temporarily
    temp_path = 'temp_food_image.jpg'
    file.save(temp_path)
    
    # Analyze
    result = food_vision.analyze_plate_image(temp_path)
    
    # Generate nutrition label
    label_path = food_vision.generate_nutrition_label(result)
    
    return jsonify({
        'success': True,
        'analysis': result,
        'nutrition_label': label_path
    })

@app.route('/api/portion-guide', methods=['POST'])
def check_portion_size():
    '''Compare food portion with hand'''
    if 'image' not in request.files:
        return jsonify({'success': False, 'error': 'No image uploaded'}), 400
    
    file = request.files['image']
    temp_path = 'temp_hand_image.jpg'
    file.save(temp_path)
    
    result = portion_guide.detect_hand_in_image(temp_path)
    
    return jsonify({
        'success': True,
        'result': result,
        'portions': portion_guide.hand_based_portions
    })
"""
