# SurveillanceX: Intelligent Video Surveillance 

SurveillanceX is an innovative project that combines cutting-edge technology with video surveillance systems. Using deep learning and YOLO object detection, it enables real-time tracking and head counting in video streams. The system can seamlessly switch between multiple streams and provides detailed logs of detection results in a SQLite database. SurveillanceX offers an intuitive GUI through Tkinter, making it user-friendly and adaptable for various surveillance applications. By enhancing traditional surveillance with intelligence and automation, this project aims to improve security and monitoring capabilities for a wide range of scenarios.

# Installation

To set up and run **SurveillanceX: Intelligent Video Surveillance**, follow these steps:

1. **Clone the Repository:**
   Clone this repository to your local machine using the following command:
   ```bash
   git clone https://github.com/yourusername/SurveillanceX.git
   ```

2. **Navigate to the Project Directory:**
   ```bash
   cd SurveillanceX
   ```

3. **Install Dependencies:**
   Make sure you have Python 3.x installed. Then, install the required Python packages using `pip`:
   ```bash
   pip install -r requirements.txt
   ```

4. **Download YOLO Model Weights:**
   Download the YOLOv8 model weights and place them in the `models` directory. You can find the model weights at [link-to-model-weights](https://example.com/model-weights).

5. **Configure Stream URLs:**
   Edit the `STREAM_URLS` list in the code to include the URLs of the video streams you want to monitor.

6. **Create a SQLite Database:**
   Make sure you have SQLite installed. The application uses a SQLite database to log detection results. You can create a new database using a command like this:
   ```bash
   sqlite3 detection_log.db
   ```

7. **Run the Application:**
   Start the SurveillanceX application by running the following command:
   ```bash
   python vision.py
   ```

8. **Use the GUI:**
   Once the application is running, use the GUI to select the stream, start and stop video feeds, and monitor the intelligent video surveillance system.

9. **Close the Application:**
   To close the application, click the close button on the GUI window or use the standard window close operation.

10. **Retrieve Logs:**
    You can retrieve detection logs from the SQLite database (`detection_log.db`) for further analysis or reporting.
