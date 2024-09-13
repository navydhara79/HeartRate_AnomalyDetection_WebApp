import io
import base64
import os
import requests
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from datetime import timedelta
import time
import pyrebase
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from sklearn.ensemble import IsolationForest


# Set the page config
st.set_page_config(
    page_title="CARDIO APP",
    page_icon="❤",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Hide Streamlit menu and footer
hide_menu_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
"""
st.markdown(hide_menu_style, unsafe_allow_html=True)

# Firebase configuration
firebaseConfig = {
    "apiKey": "AIzaSyDFh3XYEAfqjGCvRdUKa8tWB1xh1sUghxk",
    "authDomain": "cardio-app-c6a10.firebaseapp.com",
    "projectId": "cardio-app-c6a10",
    "storageBucket": "cardio-app-c6a10.appspot.com",
    "messagingSenderId": "530908745452",
    "appId": "1:530908745452:web:b4a8bab1c57c51c61e5fc9",
    "measurementId": "G-4WQ22MNGH4",
    "databaseURL": "https://cardio-app-c6a10-default-rtdb.firebaseio.com/",
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()


def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


lottie_hello = load_lottieurl(
    "https://assets3.lottiefiles.com/packages/lf20_0ssane8p.json"
)
lottie_anomaly_detection = load_lottieurl(
    "https://lottie.host/896f2b98-7339-4918-931d-86f2f1e4a7e4/M8nTagSdck.json"
)
lottie_about_us = load_lottieurl(
    "https://lottie.host/b232dd42-fd46-4bb3-a3e9-7862e86b0950/BInm3nYwcU.json"
)
lottie_profile = load_lottieurl(
    "https://lottie.host/5fda5c11-7287-4e4a-836f-51d3246821b0/pWGWeHIFK5.json"
)


def main():
    # Sidebar Login/Signup
    st.sidebar.title("CARDIO APP ❤")
    choice = st.sidebar.selectbox("LOGIN/SIGNUP", ["Login", "Signup"])
    email = st.sidebar.text_input("ENTER YOUR EMAIL ADDRESS")
    password = st.sidebar.text_input("ENTER YOUR PASSWORD", type="password")

    global user_id  # Define user_id as global to use it throughout the script

    if choice == "Signup":
        handle = st.sidebar.text_input("ENTER YOUR NAME", value="default")
        submit = st.sidebar.button("CREATE ACCOUNT")

        if submit:
            user = auth.create_user_with_email_and_password(email, password)
            st.sidebar.success("ACCOUNT CREATED SUCCESSFULLY")
            st.info(f"WELCOME -- {handle}")
            st.caption("THANKS FOR SIGNING UP, PLEASE LOGIN TO CONTINUE")
            user = auth.sign_in_with_email_and_password(email, password)
            user_id = user["localId"]  # Assign user_id when the user signs up
            db.child(user_id).child("Handle").set(handle)
            db.child(user_id).child("Id").set(user_id)

    if choice == "Login":
        login = st.sidebar.checkbox("Login")

        if login:
            st.sidebar.success("LOGGED IN SUCCESSFULLY")
            user = auth.sign_in_with_email_and_password(email, password)
            user_id = user["localId"]  # Assign user_id when the user logs in

            # Navigation menu
            selected2 = option_menu(
                None,
                ["Home", "Profile", "Anomaly Detection", "Anomaly Records"],
                icons=["house", "person", "activity", "folder"],
                menu_icon="cast",
                default_index=0,
                orientation="horizontal",
                styles={
                    "container": {
                        "padding": "0!important",
                        "background-color": "#000000",
                    },
                    "icon": {"color": "red", "font-size": "20px"},
                    "nav-link": {
                        "font-size": "15px",
                        "font-family": "Copperplate,Copperplate Gothic Light,fantasy",
                        "text-align": "left",
                        "margin": "0px",
                        "--hover-color": "#413839",
                    },
                    "nav-link-selected": {"background-color": "#f1c40f"},
                },
            )

            # Home Page
            if selected2 == "Home":
                # Add a header with title and description
                st.markdown(
                    '<h1 style="text-align: center; color: #4ad3d3; font-family: Papyrus; font-size: 40px;">Welcome ❤️ Pine Analytics</h1>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    '<p style="text-align: center; color: #e6b0aa; font-family: Copperplate,Copperplate Gothic Light,fantasy; font-size: 23px;">Your partner in monitoring heart health in real-time using advanced AI techniques.</p>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    '<p style="color: #FFFFFF; font-family: Candara,Calibri,Segoe,Segoe UI,Optima,Arial,sans-serif; text-align: center; font-size: 18px;">The Cardio App leverages advanced anomaly detection techniques to monitor your heart rate data in real-time. Our goal is to provide early warnings of potential heart-related issues by detecting irregular patterns or anomalies in your heart activity. The app is user-friendly and powered by AI to help you stay on top of your heart health.</p>',
                    unsafe_allow_html=True,
                )

                st_lottie(lottie_hello, key="hello", height=400)
                # Create informative sections
                st.markdown("---")  # Horizontal line

                st.markdown(
                    '<h1 style="color: #4ad3d3; font-family: Papyrus; text-align: center;">About the App</h2>',
                    unsafe_allow_html=True,
                )

                st.markdown(
                    """
                    <style>
                    .card {
                        background-color: #212f3c;
                        border-radius: 15px;
                        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
                        transition: 0.3s;
                        width: 100%;
                        height: 300px;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        text-align: center;
                        margin: 20px;
                        cursor: pointer;
                    }

                    .card:hover {
                        transform: scale(1.05);
                        box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2);
                    }

                    .card-content {
                        font-family: Consolas,monaco,monospace;
                        font-size: 18px;
                        color: #fbfcfc;
                    }
                    </style>
                """,
                    unsafe_allow_html=True,
                )
                st_lottie(lottie_about_us, key="about_us", height=400)

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown(
                        '<div class="card" onclick="location.href=\'#\'"><div class="card-content"><h2 style="color:#e6b0aa; font-family: system-ui ;">How It Works</h2><p>📊 Upload your heart rate data and monitor it in real-time.</p><p>⚠️ Detect anomalies and receive early warnings for potential issues.</p><p>🧠 Leverages advanced AI algorithms to analyze your data.</p><p>👨‍⚕️ Consult your healthcare provider for accurate diagnosis and guidance.</p></div></div>',
                        unsafe_allow_html=True,
                    )

                with col2:
                    st.markdown(
                        '<div class="card" onclick="location.href=\'#\'"><div class="card-content"><h2 style="color:#e6b0aa; font-family: system-ui ;">Why Choose Us?</h2><p>🚀 Real-time monitoring with easy-to-use interface.</p><p>🔍 Accurate detection powered by state-of-the-art AI.</p><p>🗂 Comprehensive history of heart rate data.</p><p>🔒 Secure and private data handling.</p></div></div>',
                        unsafe_allow_html=True,
                    )

                col3, col4 = st.columns(2)

                with col3:
                    st.markdown(
                        '<div class="card" onclick="location.href=\'#\'"><div class="card-content"><h2 style="color:#e6b0aa; font-family: system-ui ;">Guidelines</h2><p>✅ Ensure your device is properly connected and functional.</p><p>⬆️ Upload accurate heart rate data for best results.</p><p>♻️ Regularly monitor your heart rate data for any anomalies.</p><p>🧑‍⚕️ Consult with your doctor if any irregular patterns are detected.</p></ol></div></div>',
                        unsafe_allow_html=True,
                    )

                with col4:
                    st.markdown(
                        '<div class="card" onclick="location.href=\'#\'"><div class="card-content"><h2 style="color:#e6b0aa; font-family: system-ui ;">Heart Health Tips</h2><ul><p>🚶‍♂️ Stay active: Aim for at least 30 minutes of exercise daily.</p><p>🥦 Eat a balanced diet: Include plenty of fruits, vegetables, and whole grains.</p><p>🧘‍♂️ Manage stress: Practice mindfulness, meditation, or yoga.</p><p>🚭 Avoid smoking: Smoking increases the risk of heart disease.</p></ul></div></div>',
                        unsafe_allow_html=True,
                    )

                st.markdown(
                    """
                    <style>
                    .footer {
                        position: fixed;
                        bottom: 0;
                        width: 100%;
                        background-color: rgba(34, 40, 49, 0.8); /* Semi-transparent background */
                        color: #FFD700;
                        text-align: center;
                        padding: 10px 0;
                        font-family: 'Papyrus', sans-serif;
                        font-size: 16px; /* Smaller font size */
                        backdrop-filter: blur(10px); /* Blur effect */
                        box-shadow: 0 -1px 5px rgba(0, 0, 0, 0.3);
                        z-index: 100;
                    }
                    </style>
                    <div class="footer">
                        Created by Navyadhara ❤️
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            # Profile Page
            if selected2 == "Profile":
                st.markdown(
                    '<p style="text-align: center; font-family:Copperplate,Copperplate Gothic Light,fantasy; color:#66CDAA; font-size: 34px;">Profile</p>',
                    unsafe_allow_html=True,
                )

                # Display Lottie animation for profile
                st_lottie(lottie_profile, key="profile", height=400)

                # Check if profile data exists
                profile_data = db.child(user_id).child("Profile").get().val()

                # Define columns for a 3x3 grid layout
                col1, col2, col3 = st.columns(3)

                if profile_data:
                    with col1:
                        first_name = st.text_input(
                            "First Name",
                            value=profile_data.get("First Name", ""),
                            key="first_name",
                        )
                        dob = st.date_input(
                            "Date of Birth",
                            pd.to_datetime(profile_data.get("Date of Birth", "")),
                            key="dob",
                        )
                        doctor_details = st.text_area(
                            "Doctor Details",
                            value=profile_data.get("Doctor Details", ""),
                            key="doctor_details",
                        )

                    with col2:
                        last_name = st.text_input(
                            "Last Name",
                            value=profile_data.get("Last Name", ""),
                            key="last_name",
                        )
                        weight = st.number_input(
                            "Weight (kg)",
                            min_value=0,
                            value=int(profile_data.get("Weight", 0)),
                            key="weight",
                        )
                        heart_problems = st.text_area(
                            "Previous Heart Problems",
                            value=profile_data.get("Previous Heart Problems", ""),
                            key="heart_problems",
                        )

                    with col3:
                        email_update = st.text_input(
                            "Change Email",
                            value=profile_data.get("Email", email),
                            key="email_update",
                        )
                        height = st.number_input(
                            "Height (cm)",
                            min_value=0,
                            value=int(profile_data.get("Height", 0)),
                            key="height",
                        )
                        sex = st.selectbox(
                            "Sex",
                            ["Male", "Female", "Other"],
                            index=["Male", "Female", "Other"].index(
                                profile_data.get("Sex", "Male")
                            ),
                            key="sex",
                        )

                else:
                    with col1:
                        first_name = st.text_input(
                            "First Name", value="", key="first_name"
                        )
                        dob = st.date_input("Date of Birth", key="dob")
                        doctor_details = st.text_area(
                            "Doctor Details", key="doctor_details"
                        )

                    with col2:
                        last_name = st.text_input(
                            "Last Name", value="", key="last_name"
                        )
                        weight = st.number_input(
                            "Weight (kg)", min_value=0, key="weight"
                        )
                        heart_problems = st.text_area(
                            "Previous Heart Problems", key="heart_problems"
                        )

                    with col3:
                        email_update = st.text_input(
                            "Change Email", value=email, key="email_update"
                        )
                        height = st.number_input(
                            "Height (cm)", min_value=0, key="height"
                        )
                        sex = st.selectbox(
                            "Sex", ["Male", "Female", "Other"], key="sex"
                        )

                # Save Profile Information
                if st.button("Save Profile"):
                    user_data = {
                        "First Name": first_name,
                        "Last Name": last_name,
                        "Email": email_update,
                        "Sex": sex,
                        "Date of Birth": str(dob),
                        "Weight": weight,
                        "Height": height,
                        "Previous Heart Problems": heart_problems,
                        "Doctor Details": doctor_details,
                    }
                    db.child(user_id).child("Profile").set(user_data)
                    st.success("Profile updated successfully!")
            # Anomaly Detection Page
            if selected2 == "Anomaly Detection":
                st.markdown(
                    '<p style="text-align: center; font-family:Copperplate,Copperplate Gothic Light,fantasy; color:#66CDAA; font-size: 34px;">Anomaly Detection in Heart Rate Data</p>',
                    unsafe_allow_html=True,
                )

                # File uploader for CSV files
                uploaded_file = st.file_uploader(
                    "Upload your heart rate CSV file", type="csv"
                )

                if uploaded_file:
                    df = pd.read_csv(uploaded_file)
                    # st.write("Uploaded Data Preview:")
                    # st.write(df.head())

                    # Clean data to handle missing or improper data
                    df = clean_data(df)

                    if "Timestamp" in df.columns and "HeartRate_BPM" in df.columns:
                        st.sidebar.header("Anomaly Detection Settings")
                        threshold = st.sidebar.slider(
                            "Detection Sensitivity (Threshold)",
                            min_value=1.0,
                            max_value=5.0,
                            value=2.0,
                            step=0.1,
                        )
                        window = st.sidebar.slider(
                            "Moving Average Window",
                            min_value=3,
                            max_value=30,
                            value=10,
                            step=1,
                        )

                        st_lottie(
                            lottie_anomaly_detection,
                            height=400,
                            key="anomaly_detection",
                        )

                        # Simulate real-time data streaming
                        simulate_real_time(df, window, threshold)

                    else:
                        st.error(
                            "The uploaded file does not have the required columns: 'Timestamp' and 'HeartRate_BPM'."
                        )
                else:
                    st.info("Please upload a CSV file to begin visualizing the data.")

            # Anomaly Records Page# Anomaly Records Page

            def display_anomaly_records():
                st.markdown(
                    '<p style="text-align: center; font-family:Copperplate,Copperplate Gothic Light,fantasy; color:#66CDAA; font-size: 34px;">Anomaly Records</p>',
                    unsafe_allow_html=True,
                )

                # Fetch anomaly records from the database
                anomaly_records = db.child(user_id).child("AnomalyRecords").get().val()

                if anomaly_records:
                    # Convert the dictionary of records into a list of tuples
                    records = list(anomaly_records.items())

                    # Iterate through the records and display each as a styled card with plot
                    for record_id, record in records:
                        # Display the record details and plot in a single div container using flexbox for alignment
                        plot_path = record.get("PlotFile")
                        st.markdown(
                            f"""
                        <div style="display: flex; align-items: center; background-color: #CD5C5C; padding: 15px; border-radius: 10px; margin-bottom: 15px; box-shadow: 2px 2px 5px rgba(0,0,0,0.3);">
                            <div style="flex: 1; margin-right: 20px;">
                                <h4 style="color: #FFD700;">Anomaly Detected</h4>
                                <p><strong>Timestamp:</strong> {record.get('Timestamp')}</p>
                                <p><strong>Heart Rate:</strong> {record.get('HeartRate')} BPM</p>
                                <p><strong>Details:</strong> Sudden spike or drop detected</p>
                            </div>
                            <div style="flex-shrink: 0;">
                                {"<img src='data:image/png;base64," + base64.b64encode(open(plot_path, "rb").read()).decode() + "' alt='Anomaly Plot' style='max-width: 300px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.3);'>" if plot_path and os.path.exists(plot_path) else ""}
                            </div>
                        </div>
                        """,
                            unsafe_allow_html=True,
                        )
                else:
                    st.info("No anomaly records found for this user.")

            if selected2 == "Anomaly Records":
                display_anomaly_records()


# Supporting functions for data cleaning and anomaly detection
def clean_data(df):
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")
    df = df.dropna(subset=["Timestamp"])
    df = df[df["HeartRate_BPM"] >= 0]
    df["HeartRate_BPM"] = df["HeartRate_BPM"].interpolate(method="linear")
    df = df.dropna()
    return df


def display_heart_animation():
    heart_animation = """
    <style>
    .heart {
        width: 100px;
        height: 100px;
        background-color: red;
        position: relative;
        left: 50%;
        top: 50%;
        margin: -50px 0 0 -50px;
        transform: rotate(-45deg);
        animation: beat 1s infinite;
    }

    .heart:before, .heart:after {
        content: "";
        width: 100px;
        height: 100px;
        background-color: red;
        border-radius: 50%;
        position: absolute;
    }

    .heart:before {
        top: -50px;
        left: 0;
    }

    .heart:after {
        left: 50px;
        top: 0;
    }

    @keyframes beat {
        0%, 100% {
            transform: scale(1) rotate(-45deg);
        }
        50% {
            transform: scale(1.2) rotate(-45deg);
        }
    }
    </style>
    <div class="heart"></div>
    """
    st.markdown(heart_animation, unsafe_allow_html=True)


def detect_anomalies_isolation_forest(data, contamination=0.05):
    # Reshape data for IsolationForest
    data = np.array(data).reshape(-1, 1)
    model = IsolationForest(contamination=contamination)
    model.fit(data)
    predictions = model.predict(data)
    # -1 indicates anomaly in IsolationForest
    anomalies = predictions == -1
    return anomalies


# Import os module at the top of your file

import os  # Ensure 'os' is imported
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def simulate_real_time(df, window, threshold, update_interval=0.5):
    df = df.sort_values(by="Timestamp")
    df = df.reset_index(drop=True)
    heart_rate_data = []
    timestamps = []
    anomalies_detected = []

    # Directory to save anomaly plots
    plot_dir = "anomaly_plots"
    os.makedirs(plot_dir, exist_ok=True)

    # Stream data row by row
    for i in range(len(df)):
        new_row = df.iloc[i]
        heart_rate_data.append(new_row["HeartRate_BPM"])
        timestamps.append(new_row["Timestamp"])
        heart_rate_series = pd.Series(heart_rate_data)

        # Detect anomalies using Isolation Forest
        if len(heart_rate_series) > window:
            anomalies = detect_anomalies_isolation_forest(heart_rate_series)
            if anomalies[-1]:  # Check if the last point is an anomaly
                st.warning(
                    f"Anomaly detected at {timestamps[-1]} with {heart_rate_data[-1]} BPM"
                )
                anomalies_detected.append((timestamps[-1], heart_rate_data[-1]))

                # Save anomaly plot locally
                fig_anomaly = go.Figure()
                fig_anomaly.add_trace(
                    go.Scatter(
                        x=timestamps,
                        y=heart_rate_data,
                        mode="lines+markers",
                        name="Heart Rate (BPM)",
                        line=dict(color="deepskyblue", width=2),
                        marker=dict(size=6),
                    )
                )
                fig_anomaly.add_trace(
                    go.Scatter(
                        x=[timestamps[-1]],
                        y=[heart_rate_data[-1]],
                        mode="markers",
                        name="Anomaly",
                        marker=dict(color="red", size=10, symbol="x"),
                    )
                )

                # Define the path to save the plot
                plot_path = os.path.join(
                    plot_dir,
                    f"anomaly_{user_id}_{timestamps[-1].strftime('%Y%m%d_%H%M%S')}.png",
                )
                fig_anomaly.write_image(plot_path)

                # Check if the node exists; if not, create it
                if not db.child(user_id).child("AnomalyRecords").shallow().get().val():
                    db.child(user_id).child("AnomalyRecords").set({})

                # Save the anomaly record to the database
                anomaly_record = {
                    "Timestamp": str(timestamps[-1]),
                    "HeartRate": heart_rate_data[-1],
                    "PlotFile": plot_path,  # Store the local path in the database
                }
                db.child(user_id).child("AnomalyRecords").push(anomaly_record)

        # Create a Plotly figure for real-time visualization
        fig = make_subplots()
        fig.add_trace(
            go.Scatter(
                x=timestamps,
                y=heart_rate_data,
                mode="lines+markers",
                name="Heart Rate (BPM)",
                line=dict(color="deepskyblue", width=2),
                marker=dict(size=6),
            )
        )

        # Plot anomalies
        if anomalies_detected:
            for anomaly_time, anomaly_rate in anomalies_detected:
                fig.add_trace(
                    go.Scatter(
                        x=[anomaly_time],
                        y=[anomaly_rate],
                        mode="markers",
                        name="Anomaly",
                        marker=dict(color="red", size=10, symbol="x"),
                        showlegend=True,
                    )
                )

        # Update layout for better visualization
        fig.update_layout(
            title="Heart Rate Data Streaming",
            xaxis_title="Time",
            yaxis_title="Heart Rate (BPM)",
            template="plotly_dark",
            legend=dict(
                orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
            ),
            margin=dict(l=40, r=40, t=40, b=40),
        )

        # Display the plot using Plotly
        st.plotly_chart(fig)

        # Wait for the next update
        time.sleep(
            update_interval
        )  # Adjust the interval to control the speed of data simulation


def plot_anomaly_window(df, timestamps, heart_rate_data, anomaly_index):
    anomaly_time = timestamps.iloc[anomaly_index]
    start_time = anomaly_time - pd.Timedelta(seconds=3)
    end_time = anomaly_time + pd.Timedelta(seconds=3)

    window_data = df[(df["Timestamp"] >= start_time) & (df["Timestamp"] <= end_time)]

    if window_data.empty:
        st.warning("No data found in the specified time window.")
        return

    # Plot the data within the window
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(
        window_data["Timestamp"],
        window_data["HeartRate_BPM"],
        label="Heart Rate (BPM)",
        color="deepskyblue",
        marker="o",
        linestyle="-",
        linewidth=2,
        markersize=8,
    )
    ax.scatter(
        [anomaly_time],
        [heart_rate_data.iloc[anomaly_index]],
        color="red",
        label="Anomaly",
        s=100,
        zorder=5,
    )

    # Annotate the anomaly point
    ax.annotate(
        "Anomaly Detected",
        xy=(anomaly_time, heart_rate_data.iloc[anomaly_index]),
        xytext=(anomaly_time, heart_rate_data.iloc[anomaly_index] + 5),
        arrowprops=dict(facecolor="red", shrink=0.05),
        fontsize=12,
        color="black",
        weight="bold",
    )

    # Enhance plot styling
    ax.set_title("Heart Rate Data with Anomaly Detection", fontsize=16, weight="bold")
    ax.set_xlabel("Time", fontsize=14, weight="bold")
    ax.set_ylabel("Heart Rate (BPM)", fontsize=14, weight="bold")
    ax.grid(True, linestyle="--", alpha=0.6)
    ax.legend(loc="upper left", fontsize=12)

    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(fig)


if __name__ == "__main__":
    main()
