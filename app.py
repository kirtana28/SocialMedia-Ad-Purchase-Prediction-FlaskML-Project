# Importing necessary modules from Flask
from flask import Flask, request, jsonify, render_template

# Importing pickle to load the trained ML model and scaler
import pickle

# Importing numpy for numerical array handling
import numpy as np


# Initializing the Flask web application
app = Flask(__name__)

# Loading the trained machine learning model from file
model = pickle.load(open('nbclassifier.pkl', 'rb'))

# Loading the saved scaler object for feature scaling
scaler = pickle.load(open('scaler.pickle', 'rb'))

# Setting the route for homepage – when user visits the root URL
@app.route('/')
def home():
    # This will render the HTML page named 'index.html'
    return render_template('index.html')


# Defining the route to handle form submission and prediction
@app.route('/predict', methods=['POST'])
def predict():
    '''
    This function handles form data, scales it, makes prediction,
    and returns result to HTML page.
    '''

    # STEP 1: Fetching user input from the form (as strings), converting to int
    int_features = [int(x) for x in request.form.values()]
    print("Initial values -->", int_features)  # ✅ DEBUGGING: You can REMOVE in final version

    # STEP 2: Converting the list into NumPy array for scaler
    pre_final_features = [np.array(int_features)]

    # STEP 3: Scaling the input data to match model training format
    final_features = scaler.transform(pre_final_features)
    print("Scaled values -->", final_features)  # ✅ DEBUGGING: You can REMOVE in final version

    # STEP 4: Predicting using the loaded ML model
    prediction = model.predict(final_features)
    print('Prediction value is:', prediction[0])  # ✅ DEBUGGING: You can REMOVE in final version

    # STEP 5: Converting prediction into human-readable output
    if (prediction[0] == 1):
        output = "True"
    elif (prediction[0] == 0):
        output = "False"
    else:
        output = "Not sure"

    # STEP 6: Sending the result back to the same HTML page
    return render_template('index.html', prediction_text='This user will buy from social network ad  {}'.format(output))


# This line starts the Flask application (only when this file is run directly)
if __name__ == "__main__":
    app.run(debug=True)
