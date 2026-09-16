"use client";

import { useEffect } from "react";

import {
  CircleMarker,
  MapContainer,
  Popup,
  TileLayer,
  useMap,
} from "react-leaflet";

import L from "leaflet";

import "leaflet/dist/leaflet.css";


type Hospital = {
  hospital_name: string;
  city: string;
  latitude: number;
  longitude: number;
  travel_minutes: number;
  predicted_wait_minutes: number;
  time_to_care_minutes: number;
};


type Props = {
  userLatitude: number;
  userLongitude: number;
  hospitals: Hospital[];
};


function FitMapBounds({
  userLatitude,
  userLongitude,
  hospitals,
}: Props) {
  const map = useMap();

  useEffect(() => {
    const points: [number, number][] = [
      [
        userLatitude,
        userLongitude,
      ],

      ...hospitals.map(
        (hospital) =>
          [
            hospital.latitude,
            hospital.longitude,
          ] as [number, number]
      ),
    ];

    const bounds = L.latLngBounds(
      points
    );

    map.fitBounds(
      bounds,
      {
        padding: [40, 40],
      }
    );

  }, [
    map,
    userLatitude,
    userLongitude,
    hospitals,
  ]);

  return null;
}


export default function HospitalMap({
  userLatitude,
  userLongitude,
  hospitals,
}: Props) {
  return (
    <MapContainer
      center={[
        userLatitude,
        userLongitude,
      ]}
      zoom={9}
      scrollWheelZoom={true}
      className="h-[450px] w-full rounded-2xl"
    >

      {/* OpenStreetMap background */}
      <TileLayer
        attribution="&copy; OpenStreetMap contributors"
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />


      {/* Automatically fit all locations */}
      <FitMapBounds
        userLatitude={userLatitude}
        userLongitude={userLongitude}
        hospitals={hospitals}
      />


      {/* User location */}
      <CircleMarker
        center={[
          userLatitude,
          userLongitude,
        ]}
        radius={9}
        pathOptions={{
          color: "blue",
          fillColor: "blue",
          fillOpacity: 1,
        }}
      >
        <Popup>
          <strong>
            Your location
          </strong>
        </Popup>
      </CircleMarker>


      {/* Hospital markers */}
      {hospitals.map(
        (hospital, index) => (

          <CircleMarker
            key={hospital.hospital_name}
            center={[
              hospital.latitude,
              hospital.longitude,
            ]}
            radius={
              index === 0 ? 10 : 7
            }
            pathOptions={{
              color:
                index === 0
                  ? "green"
                  : "red",

              fillColor:
                index === 0
                  ? "green"
                  : "red",

              fillOpacity: 0.9,
            }}
          >

            <Popup>

              <div>

                <strong>
                  #{index + 1}{" "}
                  {hospital.hospital_name}
                </strong>

                <br />

                {hospital.city}, MA

                <br />
                <br />

                Drive:{" "}
                {hospital.travel_minutes.toFixed(
                  1
                )}{" "}
                min

                <br />

                Predicted wait:{" "}
                {hospital.predicted_wait_minutes.toFixed(
                  1
                )}{" "}
                min

                <br />

                <strong>
                  Time-to-care:{" "}
                  {hospital.time_to_care_minutes.toFixed(
                    1
                  )}{" "}
                  min
                </strong>

              </div>

            </Popup>

          </CircleMarker>

        )
      )}

    </MapContainer>
  );
}