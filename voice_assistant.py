"""
🎤 Voice Assistant for Anganwadi Workers
Unique Feature: Voice commands in Hindi/Kannada for illiterate workers
Uses speech recognition to generate meal plans hands-free
"""

import speech_recognition as sr
from gtts import gTTS
import os

class VoiceAssistant:
    """
    Voice-controlled nutrition advisor for regional language support
    """
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.supported_languages = {
            'hindi': 'hi-IN',
            'kannada': 'kn-IN',
            'tamil': 'ta-IN',
            'telugu': 'te-IN',
            'english': 'en-IN'
        }
    
    def listen_command(self, language='hindi'):
        """
        Listen to voice command in specified language
        """
        lang_code = self.supported_languages.get(language, 'hi-IN')
        
        with sr.Microphone() as source:
            print(f"🎤 Listening in {language}...")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)
        
        try:
            text = self.recognizer.recognize_google(audio, language=lang_code)
            print(f"✅ Recognized: {text}")
            return text
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError as e:
            return f"Error: {e}"
    
    def speak_response(self, text, language='hindi'):
        """
        Convert text to speech in specified language
        """
        lang_code = language.split('-')[0] if '-' in language else language
        
        tts = gTTS(text=text, lang=lang_code, slow=False)
        filename = "response.mp3"
        tts.save(filename)
        
        # Play the audio (platform-specific)
        if os.name == 'nt':  # Windows
            os.system(f'start {filename}')
        else:  # Linux/Mac
            os.system(f'mpg321 {filename}')
        
        return filename
    
    def parse_meal_plan_request(self, voice_text):
        """
        Parse voice command to extract meal plan parameters
        Example: "100 बच्चों के लिए 500 रुपये में खाना बनाना है"
        """
        import re
        
        # Extract numbers (budget and children count)
        numbers = re.findall(r'\d+', voice_text)
        
        params = {
            'num_children': int(numbers[0]) if len(numbers) > 0 else 50,
            'budget': int(numbers[1]) if len(numbers) > 1 else 500,
            'voice_command': voice_text
        }
        
        # Detect age group keywords
        if any(word in voice_text.lower() for word in ['छोटे', 'small', 'baby']):
            params['age_group'] = '1-3 years'
        elif any(word in voice_text.lower() for word in ['बड़े', 'big', 'older']):
            params['age_group'] = '6-10 years'
        else:
            params['age_group'] = '3-6 years'
        
        return params


# ============================================
# INSTALLATION REQUIRED
# ============================================
"""
pip install SpeechRecognition
pip install gTTS
pip install pyaudio
"""

# ============================================
# FLASK ROUTES TO ADD
# ============================================
"""
Add to flask_app.py:

from voice_assistant import VoiceAssistant

voice_assistant = VoiceAssistant()

@app.route('/voice-assistant')
def voice_assistant_page():
    '''Voice assistant interface'''
    return render_template('voice_assistant.html')

@app.route('/api/voice/listen', methods=['POST'])
def voice_listen():
    '''Listen to voice command'''
    data = request.json
    language = data.get('language', 'hindi')
    
    text = voice_assistant.listen_command(language)
    params = voice_assistant.parse_meal_plan_request(text)
    
    return jsonify({
        'success': True,
        'recognized_text': text,
        'parsed_params': params
    })

@app.route('/api/voice/speak', methods=['POST'])
def voice_speak():
    '''Convert text to speech'''
    data = request.json
    text = data.get('text', '')
    language = data.get('language', 'hindi')
    
    audio_file = voice_assistant.speak_response(text, language)
    
    return send_file(audio_file, mimetype='audio/mpeg')
"""
