"use client";

import { useState } from "react";
import dynamic from "next/dynamic";


type HospitalRecommendation = {
  hospital_name: string;
  city: string;
  latitude: number;
  longitude: number;
  travel_minutes: number;
  driving_miles: number;
  predicted_wait_minutes: number;
  time_to_care_minutes: number;
  occupancy_rate: number;
};


const HospitalMap = dynamic(
  () => import("./components/HospitalMap"),
  {
    ssr: false,
  }
);


export default function Home() {
  const [loading, setLoading] = useState(false);

  const [recommendations, setRecommendations] =
    useState<HospitalRecommendation[]>([]);

  const [error, setError] = useState("");

  const [latitude, setLatitude] =
    useState<number | null>(null);

  const [longitude, setLongitude] =
    useState<number | null>(null);

  const [locationLoading, setLocationLoading] =
    useState(false);

  const [age, setAge] = useState("");

  const [triageCategory, setTriageCategory] =
    useState("Urgent");


  function getCurrentLocation() {
    setLocationLoading(true);
    setError("");

    if (!navigator.geolocation) {
      setError(
        "Geolocation is not supported by your browser."
      );

      setLocationLoading(false);
      return;
    }

    navigator.geolocation.getCurrentPosition(
      (position) => {
        setLatitude(
          position.coords.latitude
        );

        setLongitude(
          position.coords.longitude
        );

        setLocationLoading(false);
      },

      (locationError) => {
        console.error(locationError);

        setError(
          "Unable to access your location. Please allow location access."
        );

        setLocationLoading(false);
      }
    );
  }


  function getAgeGroup(ageValue: number) {
    if (ageValue <= 17) {
      return "Pediatric (0-17)";
    }

    if (ageValue <= 35) {
      return "Young Adult (18-35)";
    }

    if (ageValue <= 60) {
      return "Adult (36-60)";
    }

    return "Senior (61+)";
  }


  async function findHospitals() {
    if (
      latitude === null ||
      longitude === null
    ) {
      setError(
        "Please use your current location first."
      );

      return;
    }

    const numericAge = Number(age);

    if (
      !age ||
      Number.isNaN(numericAge) ||
      numericAge < 0 ||
      numericAge > 120
    ) {
      setError(
        "Please enter a valid age."
      );

      return;
    }

    const ageGroup = getAgeGroup(
      numericAge
    );

    setLoading(true);
    setError("");

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/recommend",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({
            user_latitude: latitude,
            user_longitude: longitude,
            triage_category: triageCategory,
            age_group: ageGroup,
            arrival_method: "Walk-in",
            limit: 5,
          }),
        }
      );

      if (!response.ok) {
        throw new Error(
          "Unable to get recommendations."
        );
      }

      const data = await response.json();

      setRecommendations(
        data.recommendations
      );

    } catch (err) {
      console.error(err);

      setError(
        "Something went wrong while finding hospitals."
      );

    } finally {
      setLoading(false);
    }
  }


  return (
    <main className="min-h-screen bg-gray-50">

      <div className="mx-auto max-w-5xl px-6 py-16">

        {/* Header */}
        <div className="mb-12">

          <h1 className="text-4xl font-bold text-gray-900">
            MedRoute
          </h1>

          <p className="mt-3 text-lg text-gray-600">
            Find nearby emergency departments
            ranked by estimated time-to-care.
          </p>

        </div>


        {/* Search card */}
        <div className="rounded-2xl bg-white p-6 shadow-sm">

          <h2 className="text-xl font-semibold text-gray-900">
            Find care
          </h2>

          <p className="mt-2 text-gray-600">
            Tell MedRoute where you are and a little
            about the patient.
          </p>


          {/* Location */}
          <div className="mt-6">

            <p className="text-sm font-medium text-gray-700">
              Current location
            </p>

            <button
              onClick={getCurrentLocation}
              disabled={locationLoading}
              className="mt-2 rounded-lg border border-gray-300 px-5 py-3 font-medium text-gray-900 hover:bg-gray-50 disabled:opacity-50"
            >
              {locationLoading
                ? "Getting location..."
                : "Use my current location"}
            </button>

          </div>


          {/* Location found */}
          {latitude !== null &&
            longitude !== null && (

              <div className="mt-4 rounded-lg bg-green-50 p-4">

                <p className="font-medium text-green-800">
                  Location found
                </p>

                <p className="mt-1 text-sm text-green-700">
                  Latitude:{" "}
                  {latitude.toFixed(4)}
                  {" · "}
                  Longitude:{" "}
                  {longitude.toFixed(4)}
                </p>

              </div>
            )}


          {/* Patient inputs */}
          <div className="mt-8 grid gap-6 md:grid-cols-2">

            {/* Age */}
            <div>

              <label
                htmlFor="age"
                className="block text-sm font-medium text-gray-700"
              >
                Age
              </label>

              <input
                id="age"
                type="number"
                min="0"
                max="120"
                value={age}
                onChange={(event) =>
                  setAge(event.target.value)
                }
                placeholder="21"
                className="mt-2 w-full rounded-lg border border-gray-300 px-4 py-3 text-gray-900 outline-none focus:border-black"
              />

            </div>


            {/* Urgency */}
            <div>

              <label
                htmlFor="urgency"
                className="block text-sm font-medium text-gray-700"
              >
                Urgency
              </label>

              <select
                id="urgency"
                value={triageCategory}
                onChange={(event) =>
                  setTriageCategory(
                    event.target.value
                  )
                }
                className="mt-2 w-full rounded-lg border border-gray-300 px-4 py-3 text-gray-900 outline-none focus:border-black"
              >

                <option value="Immediate">
                  Immediate
                </option>

                <option value="Emergency">
                  Emergency
                </option>

                <option value="Urgent">
                  Urgent
                </option>

                <option value="Semi-urgent">
                  Semi-urgent
                </option>

                <option value="Non-urgent">
                  Non-urgent
                </option>

              </select>

            </div>

          </div>


          {/* Find button */}
          <button
            onClick={findHospitals}
            disabled={
              loading ||
              latitude === null ||
              longitude === null
            }
            className="mt-6 rounded-lg bg-black px-5 py-3 font-medium text-white hover:bg-gray-800 disabled:cursor-not-allowed disabled:opacity-40"
          >
            {loading
              ? "Finding hospitals..."
              : "Find hospitals"}
          </button>


          {/* Error */}
          {error && (
            <p className="mt-4 text-red-600">
              {error}
            </p>
          )}

        </div>


        {/* Results */}
        {recommendations.length > 0 && (

          <section className="mt-10">

            <h2 className="mb-5 text-2xl font-semibold text-gray-900">
              Recommended hospitals
            </h2>


            {/* Best option */}
            {recommendations[0] && (

              <div className="mb-8 rounded-2xl bg-green-50 p-6">

                <p className="text-sm font-semibold uppercase tracking-wide text-green-700">
                  Best option
                </p>


                <div className="mt-3 flex flex-col gap-4 md:flex-row md:items-end md:justify-between">

                  <div>

                    <h3 className="text-2xl font-bold text-gray-900">
                      {recommendations[0].hospital_name}
                    </h3>

                    <p className="mt-1 text-gray-600">
                      {recommendations[0].city}, MA
                    </p>

                  </div>


                  <div className="md:text-right">

                    <p className="text-sm text-gray-500">
                      Estimated time-to-care
                    </p>

                    <p className="text-4xl font-bold text-gray-900">
                      {recommendations[0]
                        .time_to_care_minutes
                        .toFixed(0)}
                      {" min"}
                    </p>

                  </div>

                </div>


                <div className="mt-6 grid gap-4 border-t border-green-200 pt-5 sm:grid-cols-2">

                  <div>

                    <p className="text-sm text-gray-500">
                      Driving time
                    </p>

                    <p className="text-lg font-semibold text-gray-900">
                      {recommendations[0]
                        .travel_minutes
                        .toFixed(1)}
                      {" min"}
                    </p>

                  </div>


                  <div>

                    <p className="text-sm text-gray-500">
                      Predicted wait
                    </p>

                    <p className="text-lg font-semibold text-gray-900">
                      {recommendations[0]
                        .predicted_wait_minutes
                        .toFixed(1)}
                      {" min"}
                    </p>

                  </div>

                </div>


                <p className="mt-5 text-sm text-gray-700">
                  Ranked first because it has the lowest
                  estimated combined driving time and
                  predicted wait among the nearby
                  hospitals evaluated.
                </p>

              </div>
            )}


            {/* Map */}
            {latitude !== null &&
              longitude !== null && (

                <div className="mb-8">

                  <HospitalMap
                    userLatitude={latitude}
                    userLongitude={longitude}
                    hospitals={recommendations}
                  />

                </div>
              )}


            {/* Hospital cards */}
            <div className="space-y-4">

              {recommendations.map(
                (hospital, index) => (

                  <div
                    key={hospital.hospital_name}
                    className="rounded-2xl bg-white p-6 shadow-sm"
                  >

                    <div className="flex items-start justify-between gap-6">

                      <div>

                        <p className="text-sm font-medium text-gray-500">
                          #{index + 1}
                        </p>

                        <h3 className="mt-1 text-lg font-semibold text-gray-900">
                          {hospital.hospital_name}
                        </h3>

                        <p className="text-gray-500">
                          {hospital.city}, MA
                        </p>

                      </div>


                      <div className="text-right">

                        <p className="text-sm text-gray-500">
                          Time-to-care
                        </p>

                        <p className="text-2xl font-bold text-gray-900">
                          {hospital
                            .time_to_care_minutes
                            .toFixed(0)}
                          {" min"}
                        </p>

                      </div>

                    </div>


                    <div className="mt-5 grid grid-cols-3 gap-4 border-t pt-5">

                      {/* Drive */}
                      <div>

                        <p className="text-sm text-gray-500">
                          Drive
                        </p>

                        <p className="font-medium text-gray-900">
                          {hospital
                            .travel_minutes
                            .toFixed(1)}
                          {" min"}
                        </p>

                      </div>


                      {/* Wait */}
                      <div>

                        <p className="text-sm text-gray-500">
                          Predicted wait
                        </p>

                        <p className="font-medium text-gray-900">
                          {hospital
                            .predicted_wait_minutes
                            .toFixed(1)}
                          {" min"}
                        </p>

                      </div>


                      {/* Distance */}
                      <div>

                        <p className="text-sm text-gray-500">
                          Distance
                        </p>

                        <p className="font-medium text-gray-900">
                          {hospital
                            .driving_miles
                            .toFixed(1)}
                          {" mi"}
                        </p>

                      </div>

                    </div>

                  </div>
                )
              )}

            </div>

          </section>
        )}


        {/* Disclaimer */}
        <div className="mt-10 border-t border-gray-200 pt-6">

          <p className="text-sm text-gray-500">
            Prototype only. Predicted wait times use
            simulated hospital operating conditions
            and should not be used for emergency
            medical decisions.
          </p>

        </div>

      </div>

    </main>
  );
}