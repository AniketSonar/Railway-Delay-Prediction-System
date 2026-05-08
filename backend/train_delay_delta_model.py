import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    mean_absolute_error,
    r2_score,
    mean_squared_error
)

from xgboost import XGBRegressor

# ======================================
# LOAD DATASET
# ======================================

df = pd.read_csv(
    "railway_ml_data.csv"
)

print("\n✅ Dataset Loaded")
print(df.shape)

# ======================================
# SORT JOURNEYS
# ======================================

df = df.sort_values(
    by=[
        "train_number",
        "date",
        "sequence"
    ]
)

# ======================================
# CREATE NEXT DELAY
# ======================================

df["next_delay"] = (

    df.groupby(
        ["train_number", "date"]
    )["delay_arrival_minutes"]

    .shift(-1)

)

# ======================================
# TARGET = DELAY DELTA
# ======================================

df["target_delay_delta"] = (

    df["next_delay"]

    -

    df["delay_arrival_minutes"]

)

# ======================================
# REMOVE LAST STATIONS
# ======================================

df = df.dropna(
    subset=[
        "target_delay_delta"
    ]
)

# ======================================
# CLEAN
# ======================================

df = df.fillna(0)

df = df.drop_duplicates()

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
# TRAIN TEST SPLIT
# ======================================

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.2,

    random_state=42

)

# ======================================
# MODEL
# ======================================

model = XGBRegressor(

    n_estimators=300,

    learning_rate=0.05,

    max_depth=6,

    subsample=0.8,

    colsample_bytree=0.8,

    objective="reg:squarederror",

    random_state=42

)

# ======================================
# TRAIN
# ======================================

print("\n🚀 Training Optimized XGBoost...\n")

model.fit(
    X_train,
    y_train
)

# ======================================
# PREDICT
# ======================================

predictions = model.predict(
    X_test
)

# ======================================
# METRICS
# ======================================

mae = mean_absolute_error(
    y_test,
    predictions
)

rmse = mean_squared_error(
    y_test,
    predictions
) ** 0.5

r2 = r2_score(
    y_test,
    predictions
)

# ======================================
# RESULTS
# ======================================

print("================================")
print("📊 OPTIMIZED MODEL RESULTS")
print("================================")

print(f"\n✅ MAE: {mae:.2f}")

print(f"\n✅ RMSE: {rmse:.2f}")

print(f"\n✅ R² Score: {r2:.4f}")

# ======================================
# FEATURE IMPORTANCE
# ======================================

importance = pd.DataFrame({

    "Feature": FEATURES,

    "Importance":
        model.feature_importances_

})

importance = importance.sort_values(

    by="Importance",

    ascending=False

)

print("\n================================")
print("🔥 FEATURE IMPORTANCE")
print("================================\n")

print(importance)

# ======================================
# SAVE MODEL
# ======================================

joblib.dump(

    model,

    "delay_delta_xgb_model.pkl"

)

print("\n✅ Optimized Model Saved")
print("delay_delta_xgb_model.pkl")