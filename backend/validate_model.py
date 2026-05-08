import pandas as pd
import joblib

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

# ======================================
# LOAD DATA
# ======================================

df = pd.read_csv(
    "railway_ml_data.csv"
)

# ======================================
# SORT
# ======================================

df = df.sort_values(
    by=[
        "train_number",
        "date",
        "sequence"
    ]
)

# ======================================
# CREATE TARGET
# ======================================

df["next_delay"] = (

    df.groupby(
        ["train_number", "date"]
    )["delay_arrival_minutes"]

    .shift(-1)

)

df["target_delay_delta"] = (

    df["next_delay"]

    -

    df["delay_arrival_minutes"]

)

# ======================================
# CLEAN
# ======================================

df = df.dropna(
    subset=[
        "target_delay_delta"
    ]
)

df = df.fillna(0)

# ======================================
# FEATURES
# ======================================

FEATURES = [

    "sequence",

    "is_origin",

    "is_destination",

    "scheduled_hour",

    "scheduled_departure_hour",

    "actual_hour",

    "day_of_week",

    "dwell_time_scheduled_mins",

    "inter_station_scheduled_mins",

    "platform_num",

    "prev_delay_arrival",

    "prev_delay_departure",

    "delay_trend",

    "journey_max_delay_so_far",

    "journey_avg_delay_so_far"

]

TARGET = "target_delay_delta"

# ======================================
# X / Y
# ======================================

X = df[FEATURES]

y = df[TARGET]

# ======================================
# LOAD MODEL
# ======================================

model = joblib.load(
    "models/best_model_v1.pkl"
)

# ======================================
# PREDICT
# ======================================

predictions = model.predict(X)

# ======================================
# METRICS
# ======================================

mae = mean_absolute_error(
    y,
    predictions
)

rmse = mean_squared_error(
    y,
    predictions
) ** 0.5

r2 = r2_score(
    y,
    predictions
)

# ======================================
# RESULTS
# ======================================

print("\n================================")
print("📊 MODEL VALIDATION")
print("================================")

print(f"\n✅ MAE: {mae:.2f}")

print(f"\n✅ RMSE: {rmse:.2f}")

print(f"\n✅ R² Score: {r2:.4f}")

# ======================================
# QUALITY CHECK
# ======================================

print("\n================================")
print("🎯 MODEL QUALITY")
print("================================")

if r2 >= 0.80:

    print("\n🔥 Excellent Model")

elif r2 >= 0.65:

    print("\n✅ Good Model")

elif r2 >= 0.50:

    print("\n⚠️ Average Model")

else:

    print("\n❌ Weak Model")