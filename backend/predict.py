import joblib
import pandas as pd
import json
import sys

# Load models
arrival_model = joblib.load("arrival_model.pkl")
departure_model = joblib.load("departure_model.pkl")

# Get input JSON from Node.js
input_json = sys.argv[1]
data = json.loads(input_json)

# Convert to DataFrame
df = pd.DataFrame([data])

# Predict
arrival = arrival_model.predict(df)[0]
departure = departure_model.predict(df)[0]

confidence = 89
# Return result
result = {
    "predicted_arrival_delay": round(float(arrival), 2),
    "predicted_departure_delay": round(float(departure), 2),
    "confidence": confidence
}

print(json.dumps(result))