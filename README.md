### Deployed at https://navyadhara-heartratewebapp.streamlit.app/

# ❤️ CARDIO APP: Real-Time Heart Rate Monitoring

Welcome to the **Cardio App**, a web-based application designed to process and visualize real-time heart rate data. The app identifies and handles anomalies (e.g., sudden spikes, drops, and missing data) using advanced AI techniques. This tool is ideal for monitoring heart health in real-time.

## 🌟 Features

- **Real-Time Simulation:** Processes heart rate data as if it were being received in real-time.
- **Anomaly Detection:** Utilizes the Isolation Forest algorithm to detect irregularities such as sudden spikes, drops, or missing data.
- **Visualization:** Displays real-time and historical data visually using Plotly.
- **User Management:** Secure user authentication and profile management using Firebase.
- **Interactive UI:** A user-friendly interface built with Streamlit, incorporating modern design elements and animations.

## 🚀 Getting Started

### Prerequisites

- Python 3.x
- Required Python packages: `streamlit`, `pandas`, `matplotlib`, `plotly`, `numpy`, `requests`, `pyrebase`, `scikit-learn`

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/cardio-app.git
   cd cardio-app


2. **Install the required packages:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**

   ```bash
   streamlit run app.py
   ```

4. **Access the application:**

   Open your web browser and go to `http://localhost:8501`.

## ⚙️ How It Works

### Real-Time Simulation

- The application processes heart rate data in a simulated real-time environment.
- It reads the heart rate data file row by row, simulating the continuous arrival of new data points.

### Anomaly Detection

- The Isolation Forest algorithm detects anomalies in heart rate data based on historical patterns.
- Anomalies are visualized in real-time and stored for future reference.

### Visualization

- Real-time heart rate data and detected anomalies are displayed using interactive Plotly graphs.
- The user can view historical anomaly records and their corresponding visualizations.

## 📁 File Structure

- **`app.py`**: The main application file containing the logic for real-time simulation, anomaly detection, and visualization.
- **`requirements.txt`**: A list of required Python packages.
- **`README.md`**: This file, providing an overview of the application and setup instructions.

## 📊 Example Data

Upload your CSV file with heart rate data in the format:

| Timestamp             | HeartRate_BPM |
|-----------------------|---------------|
| 2024-08-01 08:00:00   | 72            |
| 2024-08-01 08:01:00   | 75            |
| ...                   | ...           |

## ✨ Animations and Visuals

- **Lottie Animations:** Lottie animations are used to enhance the user experience.
- **Custom Visuals:** Interactive Plotly charts for real-time data visualization and anomaly detection.

## 🛠️ Customization

You can customize the application by modifying:

- **Anomaly Detection Parameters:** Adjust the sensitivity and detection window in the sidebar settings.
- **Visuals and Layout:** Update the `app.py` file to modify the layout and styles.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## 🙏 Acknowledgments

- Developed by [Navyadhara](https://www.linkedin.com/in/navyadhara/)
- Special thanks to [LottieFiles](https://lottiefiles.com/) for animations.

## 📞 Contact

Feel free to reach out for any questions or feedback:

- **Email:** navyadhara.1805@gmail.com
- **LinkedIn:** [linkedin.com/in/navyadhara/](https://linkedin.com/in/navyadhara/)

---

*Created with ❤️ by Navyadhara.*
```


### What to Do Next:
1. Replace `https://github.com/yourusername/cardio-app.git` with the actual URL of your GitHub repository.
2. Add a `LICENSE` file if you plan to specify licensing terms.
3. Add any specific usage notes or examples that would be useful to users of your app.

Feel free to make any modifications based on your needs or additional details!
