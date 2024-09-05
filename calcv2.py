import streamlit as st
import csv
from datetime import datetime
import os
import dropbox
from dropbox import DropboxOAuth2Flow

# Retrieve Dropbox App key and secret from Streamlit secrets
APP_KEY = st.secrets["dropbox"]["app_key"]
APP_SECRET = st.secrets["dropbox"]["app_secret"]
REDIRECT_URI = "https://calcv2.streamlit.app/"

# Streamlit state management for OAuth flow
if 'access_token' not in st.session_state:
  st.session_state.access_token = None

def dropbox_oauth_flow():
  if st.session_state.access_token is None:
      if 'oauth_result' not in st.session_state:
          auth_flow = DropboxOAuth2Flow(
              APP_KEY,
              APP_SECRET,
              REDIRECT_URI,
              st.session_state,
              "dropbox-auth-csrf-token"
          )
          auth_url = auth_flow.start()
          st.markdown(f"[Authorize the app]({auth_url})")
          st.write("After authorization, you'll be redirected back to this app.")
      else:
          st.session_state.access_token = st.session_state.oauth_result.access_token
          st.success("Successfully authenticated with Dropbox!")
          del st.session_state.oauth_result
  else:
      st.success("Already authenticated with Dropbox.")

def upload_to_dropbox(file_path, destination_path):
  if st.session_state.access_token is None:
      st.error("Not authenticated with Dropbox. Please complete the OAuth flow first.")
      return None
  
  try:
      with dropbox.Dropbox(st.session_state.access_token) as dbx:
          with open(file_path, "rb") as f:
              dbx.files_upload(f.read(), destination_path, mode=dropbox.files.WriteMode("overwrite"))
          shared_link = dbx.sharing_create_shared_link(destination_path)
          return shared_link.url.replace("?dl=0", "?dl=1")
  except dropbox.exceptions.AuthError:
      st.error("Authentication token is invalid. Please re-authenticate.")
      st.session_state.access_token = None
      return None
  except Exception as e:
      st.error(f"Error uploading to Dropbox: {str(e)}")
      return None

def ev_energy_calculator():
  st.title("EV Energy Calculator")

  # Run OAuth flow
  dropbox_oauth_flow()

  # Input for the user to name their fleet
  fleet_name = st.text_input("Enter your fleet name:", value="MyFleet")

  # Input 1: Vehicle Information
  st.header("Vehicle Information")
  st.write("How many EVs will be needed and how much energy is needed?")

  total_cars_per_day = st.number_input("Total # of cars charging per day:", min_value=0, value=5, step=1)
  avg_capacity_ev = st.number_input("Average Capacity of EVs (kWh):", min_value=0.0, value=150.0, step=1.0)
  capacity_charging_station = st.number_input("Capacity of Charging Station (kW):", min_value=0.0, value=50.0, step=1.0)
  rate_of_charging_per_hour = st.number_input("Rate of charging per hour (kW):", min_value=0.0, value=50.0, step=1.0)
  miles_per_vehicle_per_day = st.number_input("Miles Per Vehicle driven per day:", min_value=0.0, value=50.0, step=1.0)
  max_mileage_per_vehicle = st.number_input("Max Mileage Per Vehicle:", min_value=0.0, value=150.0, step=1.0)
  days_of_operation_per_week = st.number_input("Days of Operation per week:", min_value=0, value=5, step=1)
  number_of_stations = st.number_input("Number of Stations (dual port):", min_value=0, value=6, step=1)

  # Calculate energy needed
  energy_needed_per_vehicle = (miles_per_vehicle_per_day / max_mileage_per_vehicle) * avg_capacity_ev
  total_energy_needed_per_day = total_cars_per_day * energy_needed_per_vehicle

  # Visual separator
  st.markdown("---")

  # Input 2: Amount of Hours of Charge Needed
  st.header("Amount of Hours of Charge Needed")
  st.write("How long do you have to charge?")

  avg_charge_time_per_ev = energy_needed_per_vehicle / rate_of_charging_per_hour
  total_charge_time_all_evs = (total_energy_needed_per_day / capacity_charging_station) / number_of_stations

  st.success(f"Hours to charge average per vehicle when needed: {avg_charge_time_per_ev:.2f} hours")
  st.warning("If larger than 5 hours, recommend demand rate calculations")
  st.success(f"Hours to charge all vehicles: {total_charge_time_all_evs:.2f} hours (subtract 8 hours from total)")

  # Button to save inputs to CSV and upload to Dropbox
  if st.button("Save Inputs to CSV and Upload to Dropbox"):
      # Generate a CSV filename with the fleet name and the current timestamp
      timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
      csv_file = f"{fleet_name}_{timestamp}_ev_energy_calculator_log.csv"

      # Save inputs to a CSV file
      with open(csv_file, mode="w", newline="") as file:
          writer = csv.writer(file)
          writer.writerow([
              "Timestamp", "Fleet Name", "Total Cars Per Day", "Avg Capacity EV", 
              "Capacity Charging Station", "Rate of Charging Per Hour", 
              "Miles Per Vehicle Per Day", "Max Mileage Per Vehicle", 
              "Days of Operation Per Week", "Number of Stations", 
              "Total Energy Needed Per Day", "Avg Charge Time Per EV", 
              "Total Charge Time All EVs"
          ])
          writer.writerow([datetime.now(), fleet_name, total_cars_per_day, avg_capacity_ev, capacity_charging_station,
                           rate_of_charging_per_hour, miles_per_vehicle_per_day, max_mileage_per_vehicle,
                           days_of_operation_per_week, number_of_stations, total_energy_needed_per_day, avg_charge_time_per_ev, total_charge_time_all_evs])
      
      st.success(f"Inputs have been saved to {csv_file}")

      # Show download button for the CSV file
      with open(csv_file, "rb") as f:
          st.download_button(
              label="Download CSV File",
              data=f,
              file_name=csv_file,
              mime="text/csv"
          )

      # Upload the CSV to Dropbox and share the link
      dropbox_path = f"/{csv_file}"
      dropbox_link = upload_to_dropbox(csv_file, dropbox_path)
      if dropbox_link:
          st.success(f"CSV file has been uploaded to Dropbox. [Download it here]({dropbox_link})")
      else:
          st.error("Failed to upload the file to Dropbox. Please check the authentication and try again.")

# Handle OAuth 2 redirect
if 'code' in st.experimental_get_query_params():
  auth_flow = DropboxOAuth2Flow(
      APP_KEY,
      APP_SECRET,
      REDIRECT_URI,
      st.session_state,
      "dropbox-auth-csrf-token"
  )
  try:
      st.session_state.oauth_result = auth_flow.finish(st.experimental_get_query_params())
  except Exception as e:
      st.error(f"Error finishing OAuth flow: {str(e)}")

# Run the calculator
if __name__ == '__main__':
  ev_energy_calculator()
