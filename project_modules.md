Based on the structure of the codebase, the project is segmented into several distinct functional modules. Here is how the code and responsibilities are mapped out:

*   **Web Server & Routing Module (`app.py`)**
    *   This is the core entry point of the application built with Flask.
    *   It defines all the web routes (`/`, `/register`, `/login`, `/prediction`, `/dashboard`).
    *   It handles user sessions, processes file uploads, controls the application logic, and dynamically generates visualizations using `matplotlib`.

*   **Deep Learning & Inference Module (`cnn_model.h5`, `scaler.pkl`)**
    *   `cnn_model.h5`: The pre-trained 1D Convolutional Neural Network (CNN) that acts as the brain of the project. It receives processed data and predicts one of the 5 brain states.
    *   `scaler.pkl`: A Scikit-Learn preprocessing object. When a user uploads new EEG data, it scales and normalizes the 178 feature columns exactly as was done during model training before feeding it to the CNN.

*   **Database Management Module (`users.db` / integrated in `app.py`)**
    *   An SQLite database that stores application data persistently.
    *   It consists of an initialization script built into `app.py` that auto-creates two tables: `users` (for authentication) and `predictions` (to track history and populate user dashboards).

*   **Frontend Template & Asset Module (`templates/`, `static/`)**
    *   `templates/`: Contains all the HTML files (`home.html`, `login.html`, `prediction.html`, etc.) powered by the Jinja2 templating engine to render data sent from the backend.
    *   `static/`: Contains the `style.css` file for visual styling and acts as a directory to save dynamically generated chart images (like `prediction_graph.png`) before they are displayed on the frontend.

*   **Model Maintenance & Patching Utilities (`patch_model.py`, `read_model_config.py`)**
    *   `patch_model.py`: A crucial utility script that modifies the internal configuration (JSON schema) of the saved `cnn_model.h5`. It fixes TensorFlow/Keras version mismatches (like `dtype` or `batch_shape` errors) so the model can load smoothly on different machines.
    *   `read_model_config.py`: A helper script likely used to inspect the internal layers and configuration of the saved model.

*   **Data Validation & Analysis Utilities (`analyze_files.py`, `check_dataset_size.py`)**
    *   These are standalone Python scripts used offline to analyze the EEG `.xlsx` or `.csv` files.
    *   They ensure the datasets have the correct dimensions (exactly 178 features) and validate the integrity of the data being used for training or testing.
