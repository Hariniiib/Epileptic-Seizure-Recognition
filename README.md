# Epileptic Seizure Recognition System

## 📌 Project Overview
The **Epileptic Seizure Recognition System** is a Deep Learning-based web application designed to analyze EEG (Electroencephalogram) signals and classify them into different categories, including seizure activity. 

It uses a **1D Convolutional Neural Network (CNN)** to process raw EEG data and provides a user-friendly interface for doctors or researchers to upload data and get instant predictions.

---

## 🚀 Tech Stack

### **Frontend**
*   **HTML5 / CSS3**: For structure and styling of the web pages.
*   **Jinja2**: Templating engine used to render dynamic content from Flask.

### **Backend**
*   **Python 3.8+**: The core programming language.
*   **Flask**: A lightweight WSGI web application framework to handle routing and server-side logic.
*   **SQLite**: A lightweight, disk-based database to store user credentials and prediction history.

### **Deep Learning & Data Processing**
*   **TensorFlow / Keras**: The framework used to build, train, and run the CNN model.
*   **Pandas**: For data manipulation and reading Excel files.
*   **NumPy**: For numerical computations and array processing.
*   **Scikit-Learn (Joblib)**: Used for loading the data scaler (`scaler.pkl`).
*   **Matplotlib**: For generating data visualization graphs on the dashboard.

---

## 📂 Project Structure
```
Epileptic Seizure Recognition/
├── app.py                  # Main Flask application file
├── cnn_model.h5            # Pre-trained CNN model
├── scaler.pkl              # Data scaler for preprocessing
├── requirements.txt        # List of dependencies
├── users.db                # SQLite database (auto-generated)
├── static/                 # CSS, Images, and generated Graphs
│   └── style.css
├── templates/              # HTML Templates
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   ├── prediction.html
│   └── dashboard.html
└── patch_model.py          # Utility to fix Keras model compatibility
```

---

## 🧠 Model Architecture
The project uses a **1D Convolutional Neural Network (CNN)** which is effective for processing time-series data like EEG signals.

*   **Input Layer**: Accepts 178 feature points (1 second of EEG recording).
*   **Conv1D Layers**: Extract features from the EEG signals.
*   **MaxPooling1D**: Reduces dimensionality while retaining important features.
*   **Flatten & Dense Layers**: Fully connected layers for classification.
*   **Output Layer**: Softmax activation to predict one of 5 classes.

---

## 📊 Dataset Classes
The system classifies EEG data into 5 categories:
1.  **Seizure Activity** (Epileptic Seizure)
2.  **Tumor Region** (Non-Seizure)
3.  **Healthy Brain Region** (Non-Seizure)
4.  **Eyes Closed** (Normal)
5.  **Eyes Open** (Normal)

---

## 🛠️ Installation & Setup

### Prerequisites
*   Python 3.8 or higher installed on your system.
*   Git installed (optional, for cloning).

### 1. Clone the Repository
```bash
git clone https://github.com/vedhapprakashni/Epilepsy-Detection.git
cd Epilepsy-Detection
```

### 2. Create a Virtual Environment (Optional but Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Patch the Model (If necessary)
If you encounter a "ValueError: batch_shape" or Keras incompatibility error, run the included patch script:
```bash
python patch_model.py
```

### 5. Run the Application
```bash
python app.py
```
The application will start at `http://127.0.0.1:5000`.

---

## 📖 How to Use
1.  **Register/Login**: Create an account to access the system.
2.  **Upload Data**: Go to the **Prediction** page and upload an `.xlsx` file containing EEG data (must have 178 columns excluding index).
3.  **View Results**: The system will display the predicted class (e.g., "Seizure Activity").
4.  **Dashboard**: Check your prediction history and visualizations in the **Dashboard** tab.

---

## 🤝 Contribution
Feel free to fork this repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License
[MIT](https://choosealicense.com/licenses/mit/)
