import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

scope = [
"https://spreadsheets.google.com/feeds",
"https://www.googleapis.com/auth/drive"
]

credentials = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"], scopes=scope
)

client = gspread.authorize(credentials)

SHEET_ID = "1BlpIqsugN-afDSgHAzpHIdjYfVJKP5QBkXidjT6YfB0"

sheet = client.open_by_key(SHEET_ID)

execution = pd.DataFrame(sheet.worksheet("Execution_Log").get_all_records())
ai = pd.DataFrame(sheet.worksheet("AI_Builder").get_all_records())
hcf = pd.DataFrame(sheet.worksheet("HCF_Impact").get_all_records())
playplate = pd.DataFrame(sheet.worksheet("PLAYPLATE_Milestones").get_all_records())

col1, col2, col3 = st.columns(3)

col1.metric("Execution Entries", len(execution))
ai_tools_built = 0
if "Status" in ai.columns:
    ai_tools_built = (ai["Status"] == "Completed").sum()

col2.metric("AI Tools Built", ai_tools_built)
people_served = 0

if not hcf.empty and "People_Served" in hcf.columns:
    people_served = pd.to_numeric(hcf["People_Served"], errors="coerce").sum()

col3.metric("People Served", int(people_served))

st.divider()

st.subheader("PLAYPLATE Launch Progress")
st.dataframe(playplate)

st.subheader("AI Builder Progress")
st.dataframe(ai)

st.subheader("HCF Impact")
st.dataframe(hcf)

st.subheader("Execution Log")

st.dataframe(execution)
