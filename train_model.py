import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np

print("Loading data...")
try:
    with open('./data.pickle', 'rb') as f:
        data_dict = pickle.load(f)
except FileNotFoundError:
    print("Error: data.pickle not found. Please run process_kaggle_data.py first.")
    exit()

data = data_dict['data']
labels = data_dict['labels']

# We need to filter out elements that don't have exactly 42 coordinates (21 landmarks * 2 [x,y])
# Sometimes MediaPipe finds two hands or misses some points.
valid_data = []
valid_labels = []

for i in range(len(data)):
    if len(data[i]) == 42:
        valid_data.append(data[i])
        valid_labels.append(labels[i])

if len(valid_data) == 0:
    print("No valid data points found. Make sure process_kaggle_data.py ran successfully.")
    exit()

data = np.asarray(valid_data)
labels = np.asarray(valid_labels)

print("Splitting data into training and testing sets...")
x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, shuffle=True, stratify=labels)

print("Training Random Forest Classifier (Updated with better parameters)...")
model = RandomForestClassifier(n_estimators=200, max_depth=None, min_samples_split=2, min_samples_leaf=1, n_jobs=-1, random_state=42)
model.fit(x_train, y_train)

print("Testing model...")
y_predict = model.predict(x_test)

score = accuracy_score(y_predict, y_test)
print(f'Done! Model Accuracy: {score * 100:.2f}%')

print("Saving model...")
with open('model.p', 'wb') as f:
    pickle.dump({'model': model}, f)

print("Model successfully saved as model.p! You can now run app.py.")
