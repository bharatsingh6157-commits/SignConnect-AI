import os
import pickle
import mediapipe as mp
import cv2

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

# Path to your Kaggle data
DATA_DIR = './data/asl_alphabet_train' 

data = []
labels = []

print("Processing Kaggle Dataset...")
try:
    if not os.path.exists(DATA_DIR):
        print(f"Error: Could not find the data directory at '{DATA_DIR}'.")
        print("Please download the 'ASL Alphabet' dataset from Kaggle and place the 'asl_alphabet_train' folder inside a 'data' folder in this directory.")
        exit()

    for dir_ in os.listdir(DATA_DIR):
        dir_path = os.path.join(DATA_DIR, dir_)
        
        # Only process directories (skip files like .DS_Store)
        if not os.path.isdir(dir_path):
            continue
            
        print(f"Processing gesture: {dir_}...")
        
        # We process a maximum of 500 images per class to save time. You can increase this.
        count = 0
        for img_path in os.listdir(dir_path):
            if count >= 500: 
                break
                
            data_aux = []
            x_ = []
            y_ = []
            
            img_full_path = os.path.join(dir_path, img_path)
            img = cv2.imread(img_full_path)
            
            if img is None:
                continue
                
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            # Extract landmarks
            results = hands.process(img_rgb)
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    for i in range(len(hand_landmarks.landmark)):
                        x = hand_landmarks.landmark[i].x
                        y = hand_landmarks.landmark[i].y

                        x_.append(x)
                        y_.append(y)

                    for i in range(len(hand_landmarks.landmark)):
                        # Normalize coordinates
                        data_aux.append(hand_landmarks.landmark[i].x - min(x_))
                        data_aux.append(hand_landmarks.landmark[i].y - min(y_))

                data.append(data_aux)
                labels.append(dir_)
                count += 1

    # Save the data
    with open('data.pickle', 'wb') as f:
        pickle.dump({'data': data, 'labels': labels}, f)
        
    print(f"Successfully processed and saved {len(data)} hand landmarks to data.pickle!")

except Exception as e:
    print(f"An error occurred: {e}")
