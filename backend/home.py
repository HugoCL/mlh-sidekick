import streamlit as st
import pandas as pd
import requests
import json
import re

# --- Configuration ---
# API Base URL (Assumes you run FastAPI on localhost:8000)
API_URL = "http://localhost:8000"

st.set_page_config(page_title="MLH Sidekick", page_icon="🤖", layout="wide")
st.title("MLH Sidekick 🤖")

# --- Helper to call API ---
def call_api(endpoint, payload):
    try:
        response = requests.post(f"{API_URL}{endpoint}", json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        return {"error": "Could not connect to backend API. Is it running?"}
    except Exception as e:
        return {"error": str(e)}

# --- Sidebar Navigation ---
page = st.sidebar.radio("Select View", ["Coaches", "Fellowship"])

# ==========================================
# COACHES PAGE
# ==========================================
if page == "Coaches":
    st.header("🏆 Coaches Dashboard")
    st.write("Upload the submission CSV to check prizes.")

    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write("### Preview Data")
        st.dataframe(df.head())

        # --- Column Mapping ---
        col_github = "Submission Url"
        col_gemini_num = "If You Are Submitting To The Best Use Of Gemini Api Prize Category, Please Provide Your Gemini Project Number."
        col_domain = "List All Of The Domain Names Your Team Has Registered With Go Daddy Registry During This Hackathon."
        
        # Verify columns exist
        missing_cols = [c for c in [col_github, col_gemini_num, col_domain] if c not in df.columns]
        if missing_cols:
            st.error(f"Missing expected columns: {missing_cols}")
        else:
            st.success("Required columns found!")

            # --- Prize Selection ---
            st.subheader("Select Prizes to Judge")
            prizes = st.multiselect(
                "Choose Agents:",
                ["Gemini", ".Tech", "MongoDB", "ElevenLabs"],
                default=["Gemini"]
            )

            if st.button("Run Judges"):
                results_data = []
                progress_bar = st.progress(0)
                status_text = st.empty()

                for index, row in df.iterrows():
                    status_text.text(f"Processing row {index + 1}/{len(df)}...")
                    progress_bar.progress((index + 1) / len(df))

                    # Basic info
                    row_result = {
                        "Project Title": row.get("Project Title", "N/A"),
                        "Submission Url": row.get(col_github, "N/A")
                    }
                    
                    repo_url = str(row.get(col_github, "")).strip()

                    # 1. GEMINI
                    if "Gemini" in prizes:
                        project_num = str(row.get(col_gemini_num, "")).strip()
                        payload = {"repo_url": repo_url, "project_number": project_num}
                        data = call_api("/api/agents/check-gemini-prize", payload)
                        row_result["Gemini_Result"] = json.dumps(data.get("result", data))

                    # 2. .TECH
                    if ".Tech" in prizes:
                        raw_domain = str(row.get(col_domain, "")).strip()
                        # Extract first URL-like string
                        url_match = re.search(r'(https?://[^\s]+)|(www\.[^\s]+)|([a-zA-Z0-9-]+\.tech)', raw_domain)
                        clean_url = url_match.group(0) if url_match else raw_domain
                        
                        payload = {"project_url": clean_url}
                        data = call_api("/api/agents/check-dot-tech-prize", payload)
                        row_result["DotTech_Result"] = json.dumps(data.get("result", data))

                    # 3. MONGODB
                    if "MongoDB" in prizes:
                        payload = {"repo_url": repo_url}
                        data = call_api("/api/agents/check-mongodb-prize", payload)
                        row_result["MongoDB_Result"] = json.dumps(data.get("result", data))

                    # 4. ELEVENLABS
                    if "ElevenLabs" in prizes:
                        payload = {"repo_url": repo_url}
                        data = call_api("/api/agents/check-elevenlabs-prize", payload)
                        row_result["ElevenLabs_Result"] = json.dumps(data.get("result", data))

                    results_data.append(row_result)

                status_text.text("Processing Complete!")
                
                results_df = pd.DataFrame(results_data)
                st.dataframe(results_df)

                csv = results_df.to_csv(index=False).encode('utf-8')
                st.download_button("Download Results CSV", csv, "judging_results.csv", "text/csv")

# ==========================================
# FELLOWSHIP PAGE
# ==========================================
elif page == "Fellowship":
    st.header("🎓 Fellowship Assessment")
    tab1, tab2 = st.tabs(["Code Reviewer", "Sidekick Chat"])

    # --- Code Reviewer ---
    with tab1:
        st.subheader("Code Quality Assessment")
        repo_url = st.text_input("GitHub Repository URL", placeholder="https://github.com/username/repo")
        
        if st.button("Review Code"):
            if not repo_url:
                st.error("Please enter a URL.")
            else:
                with st.spinner("Asking API to review code..."):
                    payload = {"repo_url": repo_url}
                    data = call_api("/api/agents/code-review", payload)
                    
                    if "error" in data:
                        st.error(data["error"])
                    else:
                        st.success("Review Complete")
                        st.json(data.get("result", {}))

    # --- Sidekick Chat ---
    with tab2:
        st.subheader("Chat with Sidekick")
        
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Ask a question..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    payload = {"message": prompt}
                    data = call_api("/api/agents/chat", payload)
                    
                    if "error" in data:
                        response_text = f"Error: {data['error']}"
                    else:
                        response_text = data.get("response", "No response received.")
                    
                    st.markdown(response_text)
            
            st.session_state.messages.append({"role": "assistant", "content": response_text})