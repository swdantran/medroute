"use client";

import {
  CircleMarker,
  MapContainer,
  Popup,
  TileLayer,
} from "react-leaflet";

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
      <TileLayer
        attribution="&copy; OpenStreetMap contributors"
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
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
          Your location
        </Popup>
      </CircleMarker>


      {/* Hospitals */}
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

                Drive:{" "}
                {hospital.travel_minutes.toFixed(1)} min

                <br />

                Predicted wait:{" "}
                {hospital.predicted_wait_minutes.toFixed(1)} min

                <br />

                Time-to-care:{" "}
                {hospital.time_to_care_minutes.toFixed(1)} min
              </div>
            </Popup>
          </CircleMarker>
        )
      )}
    </MapContainer>
  );
}