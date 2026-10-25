from flask import Flask, render_template, request, jsonify
import joblib
import re
import numpy as np

app = Flask(__name__)

# Load the optimized model pipeline
try:
    pipeline = joblib.load('phishing_svm_pipeline.joblib')
except Exception as e:
    print("Error loading pipeline. Ensure 'phishing_svm_pipeline.joblib' is generated:", e)
    pipeline = None

# Session stats simulation
stats = {
    'total': 0,
    'phishing': 0,
    'safe': 0
}

def extract_heuristics(text):
    text_lower = text.lower()
    
    # Count suspicious keywords
    keywords = ['urgent', 'verify', 'bank', 'suspend', 'restricted', 'login', 'click here', 
                'password', 'security', 'winner', 'lottery', 'fund', 'free', 'update', 'account']
    keyword_count = sum(1 for kw in keywords if kw in text_lower)
    
    # Special character and URL patterns
    special_symbols = sum(text.count(char) for char in ['$', '%', '@', '#', '!'])
    urls = re.findall(r'https?:\/\/\S+|www\.\S+', text)
    
    return {
        'char_length': len(text),
        'suspicious_keyword_count': keyword_count,
        'special_symbols': special_symbols,
        'url_count': len(urls)
    }

def calculate_risk_and_predict(text):
    if not pipeline:
        return {'prediction': 'Model Uninitialized', 'risk_score': 0.0, 'confidence': 0.0, 'heuristics': {}}
        
    # Run inference
    pred_code = int(pipeline.predict([text])[0])
    confidence = float(pipeline.decision_function([text])[0])
    
    # Sigmoid function mapper to estimate threat risk from SVM margins
    risk_score = 100 / (1 + np.exp(-confidence))
    
    heuristics = extract_heuristics(text)
    prediction = 'Phishing' if pred_code == 1 else 'Safe'
    
    return {
        'prediction': prediction,
        'risk_score': risk_score,
        'confidence': confidence,
        'heuristics': heuristics
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    last_text = ""
    
    if request.method == 'POST':
        last_text = request.form.get('email_text', '')
        if last_text.strip():
            result = calculate_risk_and_predict(last_text)
            # Update server statistics
            stats['total'] += 1
            if result['prediction'] == 'Phishing':
                stats['phishing'] += 1
            else:
                stats['safe'] += 1
                
    return render_template('index.html', result=result, last_text=last_text, stats=stats)

@app.route('/predict', methods=['POST'])
def api_predict():
    data = request.get_json(force=True)
    if not data or 'text' not in data:
        return jsonify({'error': 'Please provide text in the JSON body.'}), 400
        
    result = calculate_risk_and_predict(data['text'])
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
