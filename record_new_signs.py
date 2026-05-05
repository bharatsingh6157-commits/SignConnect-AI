import cv2
import os

DATA_DIR = './data/asl_alphabet_train'
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# The new words you want to add
new_words = ['HELLO', 'HI', 'HOW ARE YOU']
dataset_size = 300 # number of images to capture per word

cap = cv2.VideoCapture(0)

print("Starting custom data collection...")

for word in new_words:
    class_dir = os.path.join(DATA_DIR, word)
    if not os.path.exists(class_dir):
        os.makedirs(class_dir)

    print(f"Preparing to record: {word}")
    
    while True:
        ret, frame = cap.read()
        if not ret: continue
        
        cv2.putText(frame, f'Ready? Press "Q" to start recording "{word}"', (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.imshow('Recording Signs', frame)
        
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    print(f"Recording {word} now! Please hold your sign in front of the camera...")
    counter = 0
    while counter < dataset_size:
        ret, frame = cap.read()
        if not ret: continue
        
        # Show feedback
        display_frame = frame.copy()
        cv2.putText(display_frame, f'Recording "{word}"... {counter}/{dataset_size}', (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.imshow('Recording Signs', display_frame)
        cv2.waitKey(25)
        
        # Save original clean image
        cv2.imwrite(os.path.join(class_dir, f'{counter}.jpg'), frame)
        counter += 1

cap.release()
cv2.destroyAllWindows()
print("\n--- Data collection complete! ---")
print("Now run 'python process_kaggle_data.py' and then 'python train_model.py'")
