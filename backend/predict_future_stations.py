import sys
import json
import joblib
import pandas as pd

# ======================================
# LOAD MODEL
# ======================================

arrival_model = joblib.load(
    "arrival_model.pkl"
)

# ======================================
# INPUT JSON
# ======================================

input_json = sys.argv[1]

data = json.loads(input_json)

stations = data["stations"]

predictions = []

# ======================================
# HELPER
# ======================================

def minutes_to_time(minutes):

    hours = int(minutes // 60) % 24

    mins = int(minutes % 60)

    return f"{hours:02}:{mins:02}"

# ======================================
# START
# ======================================

previous_delay = 0

for index, station in enumerate(stations):

    scheduled_time = station.get(
        "scheduled_time",
        "00:00"
    )

    scheduled_hour = station.get(
        "scheduled_hour",
        12
    )

    actual_delay = station.get(
        "actual_delay",
        None
    )

    # SPLIT TIME

    hh, mm = map(
        int,
        scheduled_time.split(":")
    )

    # ======================================
    # ML FEATURES
    # ======================================

    features = pd.DataFrame([{

        "train_number":
            data["train_number"],

        "sequence":
            index + 1,

        "stop_index":
            index + 1,

        "is_origin":
            1 if index == 0 else 0,

        "is_destination":
            1 if index == len(stations)-1 else 0,

        "scheduled_hour":
            scheduled_hour,

        "scheduled_departure_hour":
            scheduled_hour,

        "actual_hour":
    station.get(
        "actual_hour",
        scheduled_hour
    ),

        "day_of_week":
            data["day_of_week"],

        "dwell_time_scheduled_mins":
    station.get(
        "dwell_time_scheduled_mins",
        0
    ),

"inter_station_scheduled_mins":
    station.get(
        "inter_station_scheduled_mins",
        0
    ),

"platform_num":
    station.get(
        "platform_num",
        1
    ),

        "prev_delay_arrival":
    previous_delay,

"prev_delay_departure":
    previous_delay,

"delay_trend":
    previous_delay,

"journey_max_delay_so_far":
    previous_delay,

"journey_avg_delay_so_far":
    previous_delay

    }])

    # ======================================
    # PREDICT ML DELAY
    # ======================================

    predicted_delay = arrival_model.predict(
        features
    )[0]

    predicted_delay = round(
        float(predicted_delay),
        2
    )

    # ======================================
    # CALCULATE PREDICTED TIME
    # ======================================

    predicted_total_minutes = (
        hh * 60
        + mm
        + predicted_delay
    )

    predicted_time = minutes_to_time(
        predicted_total_minutes
    )

    # ======================================
    # REAL STATIONS
    # ======================================

    if actual_delay is not None:

        previous_delay = actual_delay

        actual_total_minutes = (
            hh * 60
            + mm
            + actual_delay
        )

        actual_time = minutes_to_time(
            actual_total_minutes
        )

        predictions.append({

            "station":
                station["station"],

            "scheduled_time":
                scheduled_time,

            "actual_time":
                actual_time,

            "predicted_time":
                predicted_time,

            "delay":
                actual_delay,

            "predicted_delay":
                predicted_delay,

            "type":
                "real"

        })

    # ======================================
    # FUTURE STATIONS
    # ======================================

    else:

        previous_delay = predicted_delay

        predictions.append({

            "station":
                station["station"],

            "scheduled_time":
                scheduled_time,

            "actual_time":
                None,

            "predicted_time":
                predicted_time,

            "delay":
                predicted_delay,

            "predicted_delay":
                predicted_delay,

            "type":
                "predicted"

        })

# ======================================
# OUTPUT
# ======================================

print(
    json.dumps(predictions)
)