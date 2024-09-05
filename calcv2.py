import streamlit as st
import csv
from datetime import datetime
import os
import dropbox
from dropbox import DropboxOAuth2FlowNoRedirect

# Retrieve Dropbox App key and secret from Streamlit secrets
APP_KEY = st.secrets["dropbox"]["app_key"]
APP_SECRET = st.secrets["dropbox"]["app_secret"]

# Streamlit state management for OAuth flow
if 'access_token' not in st.session_state:
  st.session_state.access_token = None

def dropbox_oauth_flow():
  auth_flow = DropboxOAuth2FlowNoRedirect(APP_KEY, APP_SECRET, token_access_type='offline')
  
  if st.session_state.access_token is None:
      auth_url = auth_flow.start()
      st.write("1. Click on this URL to authorize the app:")
      st.write(auth_url)
      st.write("2. Click 'Allow' (you might have to log in first).")
      st.write("3. Copy the authorization code.")
      auth_code = st.text_input("Enter the authorization code here:")
      
      if auth_code:
          try:
              oauth_result = auth_flow.finish(auth_code)
              st.session_state.access_token = oauth_result.access_token
              st.success("Successfully authenticated with Dropbox!")
          except Exception as e:
              st.error(f"Error in OAuth flow: {str(e)}")
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

# Your existing EV calculator function
def ev_energy_calculator():
  st.title("EV Energy Calculator")

  # Run OAuth flow
  dropbox_oauth_flow()

  # ... (rest of your calculator code)

  # When saving to Dropbox:
  if st.button("Save Inputs to CSV and Upload to Dropbox"):
      # ... (your CSV creation code)

      # Upload to Dropbox
      dropbox_path = f"/{csv_file}"
      dropbox_link = upload_to_dropbox(csv_file, dropbox_path)
      if dropbox_link:
          st.success(f"CSV file has been uploaded to Dropbox. [Download it here]({dropbox_link})")
      else:
          st.error("Failed to upload the file to Dropbox. Please check the authentication and try again.")

# Run the calculator
if __name__ == '__main__':
  ev_energy_calculator()
