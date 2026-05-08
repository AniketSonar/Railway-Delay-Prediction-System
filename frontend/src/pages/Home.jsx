import { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

import Header from "../components/Header";
import TrainCard from "../components/TrainCard";

export default function Home() {

  const navigate = useNavigate();

  // ======================================
  // STATES
  // ======================================

  const [from, setFrom] =
    useState("");

  const [to, setTo] =
    useState("");

  const today = new Date()
  .toISOString()
  .split("T")[0];

const [journeyDate, setJourneyDate] =
  useState(today);

  const [trains, setTrains] =
    useState([]);

  const [loading, setLoading] =
    useState(false);

  // ======================================
  // STATION SUGGESTIONS
  // ======================================

  const [

    fromSuggestions,
    setFromSuggestions

  ] = useState([]);

  const [

    toSuggestions,
    setToSuggestions

  ] = useState([]);

  // ======================================
  // SEARCH STATIONS
  // ======================================

  const searchStations =
    async (
      value,
      type
    ) => {

      try {

        if (!value) {

          if (type === "from") {

            setFromSuggestions([]);

          }

          else {

            setToSuggestions([]);

          }

          return;

        }

        const response =
          await axios.get(

            `http://localhost:5000/search-stations?query=${value}`

          );

        if (type === "from") {

          setFromSuggestions(
            response.data || []
          );

        }

        else {

          setToSuggestions(
            response.data || []
          );

        }

      } catch (err) {

        console.error(err);

      }

    };

  // ======================================
  // SEARCH TRAINS
  // ======================================

  const searchTrains =
    async () => {

      try {

        setLoading(true);

        const response =
          await axios.post(
            "http://localhost:5000/search-trains",
            {
              from,
              to,
              journeyDate
            }
          );

        let trainData = [];

        // ======================================
        // HANDLE API STRUCTURE
        // ======================================

        if (

          response.data?.data?.trains &&
          Array.isArray(
            response.data.data.trains
          )

        ) {

          trainData =
            response.data.data.trains;

        }

        else if (

          Array.isArray(
            response.data?.data
          )

        ) {

          trainData =
            response.data.data;

        }

        else if (

          Array.isArray(
            response.data
          )

        ) {

          trainData =
            response.data;

        }

        setTrains(trainData);

      } catch (err) {

        console.error(err);

        alert(
          "Failed to fetch trains"
        );

      } finally {

        setLoading(false);

      }

    };

  // ======================================
  // TRACK TRAIN
  // ======================================

  const trackTrain =
    (train) => {

      navigate(

        `/train/${train.trainNumber}`,

        {
          state: {

            train,

            from,
            to,

            journeyDate

          }
        }

      );

    };

  // ======================================
  // UI
  // ======================================

  return (

    <div className="min-h-screen bg-slate-100 p-6">

      <div className="max-w-7xl mx-auto space-y-6">

        {/* HEADER */}

        <Header />

        {/* SEARCH CARD */}

        <div className="bg-white rounded-3xl border shadow-sm p-6">

          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">

            {/* FROM */}

            <div className="relative">

              <input
                value={from}
                onChange={(e) => {

                  setFrom(
                    e.target.value
                  );

                  searchStations(
                    e.target.value,
                    "from"
                  );

                }}
                placeholder="FROM"
                className="border rounded-2xl p-4 outline-none w-full"
              />

              {

                fromSuggestions.length > 0 && (

                  <div className="absolute z-20 bg-white border rounded-2xl shadow-lg mt-2 w-full max-h-60 overflow-y-auto">

                    {

                      fromSuggestions.map(

                        (station, index) => (

                          <div
                            key={index}
                            onClick={() => {

                              setFrom(
                                station.code
                              );

                              setFromSuggestions([]);

                            }}
                            className="p-3 hover:bg-slate-100 cursor-pointer border-b"
                          >

                            <div className="font-semibold">

                              {station.code}

                            </div>

                            <div className="text-sm text-slate-500">

                              {station.name}

                            </div>

                          </div>

                        )

                      )

                    }

                  </div>

                )

              }

            </div>

            {/* TO */}

            <div className="relative">

              <input
                value={to}
                onChange={(e) => {

                  setTo(
                    e.target.value
                  );

                  searchStations(
                    e.target.value,
                    "to"
                  );

                }}
                placeholder="TO"
                className="border rounded-2xl p-4 outline-none w-full"
              />

              {

                toSuggestions.length > 0 && (

                  <div className="absolute z-20 bg-white border rounded-2xl shadow-lg mt-2 w-full max-h-60 overflow-y-auto">

                    {

                      toSuggestions.map(

                        (station, index) => (

                          <div
                            key={index}
                            onClick={() => {

                              setTo(
                                station.code
                              );

                              setToSuggestions([]);

                            }}
                            className="p-3 hover:bg-slate-100 cursor-pointer border-b"
                          >

                            <div className="font-semibold">

                              {station.code}

                            </div>

                            <div className="text-sm text-slate-500">

                              {station.name}

                            </div>

                          </div>

                        )

                      )

                    }

                  </div>

                )

              }

            </div>

            {/* DATE */}

            <input
              type="date"
              value={journeyDate}
              onChange={(e) =>
                setJourneyDate(
                  e.target.value
                )
              }
              className="border rounded-2xl p-4 outline-none"
            />

            {/* BUTTON */}

            <button
              onClick={searchTrains}
              className="bg-slate-800 text-white rounded-2xl font-bold hover:bg-slate-900 transition-all"
            >

              {
                loading
                  ? "Searching..."
                  : "Search Trains"
              }

            </button>

          </div>

        </div>

        {/* TOTAL */}

        <div className="text-slate-600 font-semibold">

          Total Trains:
          {" "}
          {trains.length}

        </div>

        {/* TRAIN LIST */}

        <div className="space-y-4">

          {

            Array.isArray(trains) &&

            trains.map((train, index) => (

              <TrainCard
                key={index}
                train={train}
                from={from}
                to={to}
                trackTrain={trackTrain}
              />

            ))

          }

        </div>

      </div>

    </div>

  );

}