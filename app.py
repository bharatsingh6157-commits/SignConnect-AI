import pickle
import cv2
import mediapipe as mp
import numpy as np

# Load the trained model
print("Loading Model...")
try:
    with open('./model.p', 'rb') as f:
        model_dict = pickle.load(f)
    model = model_dict['model']
except FileNotFoundError:
    print("Error: model.p not found! Please train the model using train_model.py first.")
    exit()

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Start Video Capture
cap = cv2.VideoCapture(0)

# Create a dictionary for labels if needed (e.g., if labels are numbers 0,1,2, map them to A,B,C)
# Since we used the Kaggle alphabet folder names, the prediction directly gives the letter (e.g. 'A').
# So we don't strictly need a dict unless we want custom mappings like {'A': 'Hello'}
labels_dict = {} 

print("Real-time Prediction Started. Press 'Q' to quit.")

while True:
    data_aux = []
    x_ = []
    y_ = []

    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame. Exiting...")
        break

    H, W, _ = frame.shape
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        # We only process the first hand detected to keep it simple
        hand_landmarks = results.multi_hand_landmarks[0]
        
        # Draw connections on the hand
        mp_drawing.draw_landmarks(
            frame,  # image to draw
            hand_landmarks,  # model output
            mp_hands.HAND_CONNECTIONS,  # hand connections
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())

        for i in range(len(hand_landmarks.landmark)):
            x = hand_landmarks.landmark[i].x
            y = hand_landmarks.landmark[i].y

            x_.append(x)
            y_.append(y)

        for i in range(len(hand_landmarks.landmark)):
            data_aux.append(hand_landmarks.landmark[i].x - min(x_))
            data_aux.append(hand_landmarks.landmark[i].y - min(y_))

        x1 = int(min(x_) * W) - 10
        y1 = int(min(y_) * H) - 10
        x2 = int(max(x_) * W) - 10
        y2 = int(max(y_) * H) - 10

        # Sometimes due to false positives, landmark size might not be exactly 42 (21*2)
        # Random Forest expects exactly the number of features used in training (42)
        if len(data_aux) == 42:
            prediction = model.predict([np.asarray(data_aux)])

            predicted_character = str(prediction[0])

            # Draw a box and show text around the hand
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)
            cv2.putText(frame, predicted_character, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3,
                        cv2.LINE_AA)

    cv2.imshow('Sign Language AI', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
