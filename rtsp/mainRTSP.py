# import torch
# import ultralytics.models.yolo
# from ultralytics import YOLO
# import cv2
# import numpy as np

# # Check for GPU availability
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# # Initialize the YOLO model
# models_dir = "models"  # Update this to your model directory
# SEG_MODEL_NAME = "yolov8n-seg"
# seg_model = YOLO(models_dir + f'/{SEG_MODEL_NAME}.pt').to(device)

# # Replace the STREAM_URL with the URL of the video stream
# STREAM_URL = "rtsp://admin:Crl@12345@192.168.0.102:554/cam/realmonitor?channel=5&subtype=0"

# # Create a VideoCapture object for the RTSP stream
# cap = cv2.VideoCapture(STREAM_URL)

# # Initialize an empty list for box_multi_list
# box_multi_list = []

# while True:
#     # Read a frame from the RTSP stream
#     ret, frame = cap.read()

#     if not ret:
#         print("Failed to retrieve frame from the stream.")
#         break

#     # Resize the frame if necessary
#     frame = cv2.resize(frame, (640, 640))

#     # Convert BGR to RGB channel order
#     frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

#     # Normalize the frame to have pixel values in the range [0, 1]
#     frame_normalized = frame_rgb / 255.0

#     # Move the frame data to the GPU
#     frame_tensor = torch.from_numpy(frame_normalized).permute(2, 0, 1).unsqueeze(0).to(device)

#     # Perform inference on the frame
#     res = seg_model(frame_tensor)

#     # Initialize box_multi_list for this frame
#     box_multi_list = []

#   # --------- list that stores the centroids of the current frame---------#
#     centr_pt_cur_fr = []

#     # results = seg_model(frame)
#     result = res[0]
#     # ------- to get the classes of the yolo model to filter out the people---------------#
#     classes = np.array(result.boxes.cls.cpu(), dtype="int")
#     # print("this is classes:", classes)

#     # ---------confidence level of detections-----------#
#     confidence = np.array(result.boxes.conf.cpu())
#     # print("this is confidence:", confidence)

#     # --------- anarray of bounding boxes---------------#
#     bboxes = np.array(result.boxes.xyxy.cpu(), dtype="int")
#     # print("this is boxes", bboxes)

#     # -------- getting indexes of the detections containing persons--------#
#     idx = []
#     for i in range(0, len(classes)):
#         if classes[i] == 0:
#             idx.append(i)

#     # print("these are indexes:", idx)

#     # ----------- bounding boxes for person detections---------------#
#     bbox = []
#     for i in idx:
#         temp = bboxes[i]
#         # print("this is temp", temp)
#         bbox.append(temp)

#         # Convert to bbox to multidimensional list
#         box_multi_list = [arr.tolist() for arr in bbox]

#     # ------------ drawing of bounding boxes-------------#
#     for box in box_multi_list:
#         (x, y, x2, y2) = box

#         cv2.rectangle(frame, (x, y), (x2, y2), (0, 0, 255), 2)
#         cx = int((x+x2)/2)
#         cy = int((y+y2)/2)
#         centr_pt_cur_fr.append((cx, cy))
#         cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

#     # ------------- counting of total people in the footage ------------#
#     head_count = len(centr_pt_cur_fr)

#     # counting the number of faces with count_var variable
#     count_var = head_count

#     text = f'Head Count: {head_count}'
#     cv2.putText(frame, text, (15, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 3, cv2.LINE_AA)

#     # Display the frame
#     cv2.imshow("Result Image", frame)

#     # Check if the user presses the 'q' key to exit the loop
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Release the VideoCapture object and close OpenCV windows
# cap.release()
# cv2.destroyAllWindows()