from flask import Flask, request, jsonify, render_template
import numpy as np
import pickle
from datetime import datetime
from sklearn.preprocessing import LabelEncoder, StandardScaler

app = Flask(__name__)
# Load the machine learning model
randomForest = pickle.load(open('randomForest_without_scaling.pkl', 'rb'))
gtadientboosting = pickle.load(open('gradientboosting.pkl', 'rb'))
lgbm = pickle.load(open('lgbm.pkl', 'rb'))
# Define label encoder for category feature
categories = ['entertainment', 'food_dining', 'gas_transport', 'grocery_net', 'grocery_pos', 'health_fitness', 'kids_pets', 'misc_net', 'misc_pos', 'personal_care', 'shopping_net', 'shopping_pos', 'travel', 'kids_', 'home']
encoder = LabelEncoder()
encoder.fit(categories)
# Define preprocessing function
def preprocess_data(data):
    # Extract features
    category = data['category']
    amount = float(data['amount'])
    transaction_date = datetime.strptime(data['transactiondate'], '%Y-%m-%d')
    transaction_time = datetime.strptime(data['transactiontime'], '%H:%M')
    transaction_timestamp = transaction_date.timestamp() + transaction_time.hour * 3600 + transaction_time.minute * 60
    diff_seconds = abs(transaction_timestamp - 18658590)
    hour = transaction_time.hour
    category_encoded = encoder.transform([category])[0]
    features = np.array([[category_encoded, amount, diff_seconds, hour]])
    return features

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hello', methods=['POST'])
def hello():
    # Get data from the request
    data = request.get_json()
    
    # Preprocess the data
    processed_data = preprocess_data(data)
    model = data['model']
    print(model)
    # Make predictions using the loaded model
    if model == "randomForest":
        prediction = randomForest.predict(processed_data)

    elif model == "gradientboosting":
        prediction = gtadientboosting.predict(processed_data)

    elif model == "lgbm":
        prediction = lgbm.predict(processed_data)
    
    

    return jsonify({'prediction': prediction.tolist()})

if __name__ == '__main__':
    app.run(debug=True)
