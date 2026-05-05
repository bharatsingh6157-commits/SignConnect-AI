import streamlit as st
import pickle
import cv2
import mediapipe as mp
import numpy as np
import requests
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu
import base64
import os
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, RTCConfiguration
import av

RTC_CONFIGURATION = RTCConfiguration({"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})
def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

def get_base64_of_bin_file(bin_file):
    if os.path.exists(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return None

# --- Page Configuration ---
st.set_page_config(page_title="SignConnect AI", page_icon="🤟", layout="wide", initial_sidebar_state="expanded")

# --- Sidebar ---
with st.sidebar:
    logo_base64 = get_base64_of_bin_file('logo.png')
    if logo_base64:
        logo_html = f'<img src="data:image/png;base64,{logo_base64}" style="width: 60px; height: auto; filter: drop-shadow(0 0 10px rgba(0, 242, 254, 0.5));">'
    else:
        logo_html = '<div class="sidebar-logo-icon">🖐️</div>'

    st.markdown(f"""
    <div class="sidebar-logo-container">
        {logo_html}
        <div>
            <h1 class="sidebar-title">SignConnect</h1>
            <p class="sidebar-subtitle">Sign Language for Everyone</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Theme Toggle
    dark_mode = st.toggle("🌙 Dark Mode", value=True)
    
    # Colors setup based on theme
    if dark_mode:
        bg_color = "#0b1120"
        text_color = "#e2e8f0"
        sidebar_bg = "#0d1424"
        sidebar_border = "#1e293b"
        accent = "#00f2fe"
        accent_gradient = "linear-gradient(90deg, #00f2fe 0%, #4facfe 100%)"
        card_bg = "rgba(30, 41, 59, 0.4)"
        card_border = "rgba(0, 242, 254, 0.2)"
        card_shadow = "rgba(0, 0, 0, 0.2)"
        card_hover_shadow = "rgba(0, 242, 254, 0.15)"
        text_muted = "#94a3b8"
        text_darker = "#cbd5e1"
        
        menu_icon = "#e2e8f0"
        menu_nav_link = "#e2e8f0"
        menu_nav_sel_bg = "rgba(0, 242, 254, 0.15)"
    else:
        bg_color = "#f8fafc"
        text_color = "#0f172a"
        sidebar_bg = "#ffffff"
        sidebar_border = "#e2e8f0"
        accent = "#0ea5e9"
        accent_gradient = "linear-gradient(90deg, #0ea5e9 0%, #0284c7 100%)"
        card_bg = "#ffffff"
        card_border = "#e2e8f0"
        card_shadow = "rgba(0, 0, 0, 0.05)"
        card_hover_shadow = "rgba(14, 165, 233, 0.15)"
        text_muted = "#64748b"
        text_darker = "#334155"
        
        menu_icon = "#475569"
        menu_nav_link = "#475569"
        menu_nav_sel_bg = "rgba(14, 165, 233, 0.1)"

    st.markdown(f"<p style='color: {accent}; font-size: 0.85rem; font-weight: bold; letter-spacing: 1px; margin-bottom: 5px; margin-top: 15px;'>MENU</p>", unsafe_allow_html=True)
    
    page = option_menu(
        menu_title=None,
        options=["Home", "About Sign Language", "Live Translator", "Interactive Quiz", "Text-to-Sign Converter", "Live Class"],
        icons=["house-door", "book", "camera-video", "controller", "fonts", "people"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": menu_icon, "font-size": "1.1rem"}, 
            "nav-link": {"font-size": "0.95rem", "text-align": "left", "margin":"5px 0", "color": menu_nav_link, "--hover-color": "rgba(150,150,150,0.1)", "border-radius": "8px"},
            "nav-link-selected": {"background-color": menu_nav_sel_bg, "color": accent, "font-weight": "600", "border-left": f"4px solid {accent}"},
        }
    )
    
    st.markdown(f"""
    <div class="college-footer">
        <h4>COLLEGE PROJECT 🎓</h4>
        <p>Developer: <b>Bharat Singh</b></p>
        <p>Subject: <b>Machine Learning / AI</b></p>
    </div>
    """, unsafe_allow_html=True)


# --- Apply Theme CSS ---
theme_css = f"""
<style>
    .stApp {{ background-color: {bg_color}; color: {text_color}; }}
    [data-testid="stSidebar"] {{ background-color: {sidebar_bg}; border-right: 1px solid {sidebar_border}; }}
    #MainMenu {{ visibility: hidden; }}
    header[data-testid="stHeader"] {{ background: transparent; }}
    .stDeployButton {{ display:none; }}
    
    .main-title {{ text-align: center; font-size: 3.5rem; font-weight: 800; background: {accent_gradient}; -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 10px; text-shadow: 0 0 20px {card_hover_shadow}; }}
    .sub-title {{ text-align: center; font-size: 1.2rem; color: {text_muted}; margin-bottom: 40px; }}
    
    .info-card {{ background: {card_bg}; border: 1px solid {card_border}; border-radius: 16px; padding: 25px; box-shadow: 0 10px 30px {card_shadow}; backdrop-filter: blur(10px); transition: transform 0.3s ease, box-shadow 0.3s ease; height: 100%; }}
    .info-card:hover {{ transform: translateY(-5px); box-shadow: 0 10px 30px {card_hover_shadow}; border: 1px solid {accent}; }}
    .info-card h3 {{ color: {accent} !important; margin-top: 0; font-size: 1.5rem; display: flex; align-items: center; gap: 10px; }}
    
    .feature-card {{ background: {card_bg}; border-radius: 12px; padding: 20px; border: 1px solid {card_border}; height: 100%; min-height: 160px; display: flex; flex-direction: column; justify-content: flex-start; }}
    .feature-icon {{ font-size: 2rem; margin-bottom: 15px; color: {accent}; }}
    .feature-title {{ font-weight: 700; color: {text_color}; font-size: 1.1rem; margin-bottom: 8px; }}
    .feature-desc {{ color: {text_muted}; font-size: 0.9rem; line-height: 1.4; }}
    
    .sidebar-logo-container {{ display: flex; align-items: center; gap: 15px; padding: 10px 0 20px 0; margin-bottom: 10px; border-bottom: 1px solid {sidebar_border}; }}
    .sidebar-logo-icon {{ font-size: 2.5rem; }}
    .sidebar-title {{ font-size: 1.5rem; font-weight: 800; color: {accent}; margin: 0; line-height: 1.2; }}
    .sidebar-subtitle {{ font-size: 0.8rem; color: {text_muted}; margin: 0; }}
    
    .college-footer {{ margin-top: 50px; padding-top: 20px; border-top: 1px solid {sidebar_border}; }}
    .college-footer h4 {{ color: {accent} !important; font-size: 1rem; margin-bottom: 10px; }}
    .college-footer p {{ color: {text_muted}; font-size: 0.85rem; margin: 5px 0; }}
</style>
"""
st.markdown(theme_css, unsafe_allow_html=True)

# --- Load Model ---
@st.cache_resource
def load_model():
    with open('./model.p', 'rb') as f:
        model_dict = pickle.load(f)
    return model_dict['model']

try:
    model = load_model()
except FileNotFoundError:
    model = None

# --- Page Content ---
if page == "Home":
    st.markdown("<h1 class='main-title'>Sign Language Recognition AI 🤟</h1>", unsafe_allow_html=True)
    st.markdown(f"<p class='sub-title'>Breaking communication barriers using Machine Learning and Computer Vision.</p>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        st.markdown(f"""
        <div class="info-card">
            <h3>🎯 Project Objective</h3>
            <p style="color: {text_darker}; font-size: 1.05rem; line-height: 1.6;">
            The goal of this project is to create a real-time translator that can understand hand gestures (Sign Language) and convert them into readable text. This helps bridge the communication gap between the deaf community and the general public.
            </p>
            <br>
            <h4 style="color: {accent}; margin-top: 10px;">⚙️ Technology Stack</h4>
            <ul style="color: {text_darker}; font-size: 1rem; line-height: 1.6;">
                <li><b>Python:</b> Core programming language.</li>
                <li><b>OpenCV & MediaPipe:</b> Vision & Hand Landmark detection.</li>
                <li><b>Scikit-Learn:</b> Random Forest ML model.</li>
                <li><b>Streamlit:</b> Interactive web application.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        lottie_ai = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_fcfjwiyb.json")
        if lottie_ai:
            st_lottie(lottie_ai, height=450, key="home_animation")
            
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # 4 Feature Cards Row
    f_col1, f_col2, f_col3, f_col4 = st.columns(4)
    
    with f_col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">⚡</div>
            <div class="feature-title">Real-time</div>
            <div class="feature-desc">Instant gesture recognition and translation.</div>
        </div>
        """, unsafe_allow_html=True)
        
    with f_col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <div class="feature-title">Accurate</div>
            <div class="feature-desc">High accuracy using advanced ML models.</div>
        </div>
        """, unsafe_allow_html=True)
        
    with f_col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">👥</div>
            <div class="feature-title">Accessible</div>
            <div class="feature-desc">Making communication easy for everyone.</div>
        </div>
        """, unsafe_allow_html=True)
        
    with f_col4:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">💛</div>
            <div class="feature-title">Inclusive</div>
            <div class="feature-desc">Bridging the gap and building inclusivity.</div>
        </div>
        """, unsafe_allow_html=True)

elif page == "About Sign Language":
    st.markdown("<h1 class='main-title'>About Sign Language</h1>", unsafe_allow_html=True)
    st.write("Sign languages are fully-fledged natural languages with their own grammar and lexicon. They are the primary means of communication for many deaf and hard-of-hearing individuals.")
    
    st.markdown("""
    <div class="info-card">
        <h3>Did You Know?</h3>
        <ul>
            <li>There are over <b>300 different sign languages</b> used around the world today.</li>
            <li>American Sign Language (ASL) is one of the most widely used.</li>
            <li>Sign language uses not only hand shapes but also facial expressions and body language.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("The Alphabet (ASL)")
    st.write("Our current model is trained to recognize the standard ASL alphabet using static hand gestures.")
    st.image("asl_alphabet_chart.png", caption="ASL Alphabet Chart", use_container_width=True)

    st.markdown("---")
    st.subheader("Sign Language Gallery 📸")
    
    col_img1, col_img2 = st.columns(2)
    with col_img1:
        st.image("asl_line_art_1.png", caption="ASL Gesture 1", use_container_width=True)
        st.image("asl_line_art_3.png", caption="ASL Gesture 3", use_container_width=True)
    with col_img2:
        st.image("asl_line_art_2.png", caption="ASL Gesture 2", use_container_width=True)
        st.image("asl_line_art_4.png", caption="ASL Gesture 4", use_container_width=True)

elif page == "Live Translator":
    st.markdown("<h1 class='main-title'>Live Translator 📹</h1>", unsafe_allow_html=True)
    st.write("Turn on your webcam and show ASL alphabet signs. The AI will translate them in real-time!")
    
    if model is None:
        st.error("Error: model.p not found! Please train the model using train_model.py first.")
        st.stop()
        
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles

    hands = mp_hands.Hands(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)

    if 'built_word' not in st.session_state:
        st.session_state['built_word'] = ""

    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown(f"""
        <div class="info-card" style="margin-bottom: 20px;">
            <h3>Instructions</h3>
            <ol>
                <li>Click <b>START</b> to use your camera.</li>
                <li>Allow browser camera permissions.</li>
                <li>Hold a sign to append it to the word.</li>
                <li>Drop hand briefly to type the same letter again.</li>
                <li>Drop hand for 1 second to add a Space.</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
        
    class LiveTranslatorProcessor(VideoTransformerBase):
        def __init__(self):
            self.mp_hands = mp.solutions.hands
            self.hands = self.mp_hands.Hands(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)
            self.mp_drawing = mp.solutions.drawing_utils
            self.mp_drawing_styles = mp.solutions.drawing_styles
            
            self.built_word = ""
            self.last_prediction = None
            self.consistent_frames = 0
            self.last_added_letter = None
            self.frames_no_hand = 0

        def transform(self, frame):
            img = frame.to_ndarray(format="bgr24")
            H, W, _ = img.shape
            
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = self.hands.process(img_rgb)
            current_prediction = "-"
            
            if results.multi_hand_landmarks:
                self.frames_no_hand = 0
                hand_landmarks = results.multi_hand_landmarks[0]
                
                self.mp_drawing.draw_landmarks(
                    img, 
                    hand_landmarks, 
                    self.mp_hands.HAND_CONNECTIONS, 
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                    self.mp_drawing_styles.get_default_hand_connections_style())

                data_aux = []
                x_ = []
                y_ = []
                for i in range(len(hand_landmarks.landmark)):
                    x_.append(hand_landmarks.landmark[i].x)
                    y_.append(hand_landmarks.landmark[i].y)

                for i in range(len(hand_landmarks.landmark)):
                    data_aux.append(hand_landmarks.landmark[i].x - min(x_))
                    data_aux.append(hand_landmarks.landmark[i].y - min(y_))

                x1 = int(min(x_) * W) - 10
                y1 = int(min(y_) * H) - 10
                x2 = int(max(x_) * W) - 10
                y2 = int(max(y_) * H) - 10

                if len(data_aux) == 42:
                    try:
                        prediction = model.predict([np.asarray(data_aux)])
                        current_prediction = str(prediction[0])

                        if current_prediction == self.last_prediction:
                            self.consistent_frames += 1
                        else:
                            self.last_prediction = current_prediction
                            self.consistent_frames = 1
                            
                        if self.consistent_frames == 15:
                            if current_prediction != self.last_added_letter:
                                self.built_word += current_prediction
                                self.last_added_letter = current_prediction

                        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 3)
                        cv2.putText(img, current_prediction, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                    except Exception as e:
                        pass
            else:
                self.frames_no_hand += 1
                if self.frames_no_hand == 30: 
                    if len(self.built_word) > 0 and self.built_word[-1] != " ":
                        self.built_word += " "
                if self.frames_no_hand > 10:
                    self.last_added_letter = None
            
            cv2.rectangle(img, (0, 0), (W, 80), (0, 0, 0), -1)
            cv2.putText(img, f"Predict: {current_prediction}", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            cv2.putText(img, f"Word: {self.built_word}", (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            
            return img

    with col2:
        webrtc_streamer(
            key="live_translator", 
            video_processor_factory=LiveTranslatorProcessor, 
            rtc_configuration=RTC_CONFIGURATION, 
            media_stream_constraints={"video": True, "audio": False}
        )

elif page == "Interactive Quiz":
    st.markdown("<h1 class='main-title'>Interactive Quiz 🎮</h1>", unsafe_allow_html=True)
    st.write("Show the sign for the letter displayed on the screen.")
    
    if 'quiz_letter' not in st.session_state:
        import random
        st.session_state['quiz_letter'] = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        st.session_state['quiz_score'] = 0
        
    st.markdown(f"<h2 style='text-align: center; color: {accent};'>Score: {st.session_state['quiz_score']}</h2>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='text-align: center; font-size: 8rem; color: #ffcc00; text-shadow: 0 0 20px rgba(255, 204, 0, 0.4);'>{st.session_state['quiz_letter']}</h1>", unsafe_allow_html=True)
    
    colA, colB = st.columns(2)
    with colA:
        if st.button("Skip Letter", use_container_width=True):
            import random
            st.session_state['quiz_letter'] = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
            st.rerun()
    with colB:
        if st.button("Reset Score", use_container_width=True, type="primary"):
            st.session_state['quiz_score'] = 0
            st.rerun()
        
    run_quiz = st.checkbox('🔴 Start Quiz Webcam')
    FRAME_WINDOW_QUIZ = st.empty()
    
    if run_quiz:
        if model is None:
            st.error("Error: model.p not found! Please train the model using train_model.py first.")
            st.stop()
            
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)
        mp_drawing = mp.solutions.drawing_utils
        mp_drawing_styles = mp.solutions.drawing_styles
        
        consistent_frames = 0
        
        try:
            while run_quiz:
                ret, frame = cap.read()
                if not ret: break
                
                H, W, _ = frame.shape
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = hands.process(frame_rgb)
                
                if results.multi_hand_landmarks:
                    hand_landmarks = results.multi_hand_landmarks[0]
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS, mp_drawing_styles.get_default_hand_landmarks_style(), mp_drawing_styles.get_default_hand_connections_style())
                    
                    data_aux = []
                    x_ = []
                    y_ = []
                    for i in range(len(hand_landmarks.landmark)):
                        x_.append(hand_landmarks.landmark[i].x)
                        y_.append(hand_landmarks.landmark[i].y)
                    for i in range(len(hand_landmarks.landmark)):
                        data_aux.append(hand_landmarks.landmark[i].x - min(x_))
                        data_aux.append(hand_landmarks.landmark[i].y - min(y_))
                        
                    if len(data_aux) == 42:
                        try:
                            prediction = str(model.predict([np.asarray(data_aux)])[0])
                            x1 = int(min(x_) * W) - 10
                            y1 = int(min(y_) * H) - 10
                            
                            rect_color = (254, 242, 0) if dark_mode else (200, 100, 0)
                            cv2.putText(frame, prediction, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, rect_color, 2, cv2.LINE_AA)
                            
                            if prediction == st.session_state['quiz_letter']:
                                consistent_frames += 1
                                if consistent_frames > 15:
                                    break
                            else:
                                consistent_frames = 0
                        except:
                            pass
                            
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                FRAME_WINDOW_QUIZ.image(frame, use_container_width=True)
        finally:
            cap.release()
            
        if consistent_frames > 15:
            st.session_state['quiz_score'] += 1
            import random
            st.session_state['quiz_letter'] = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
            st.success("Correct!")
            st.rerun()

elif page == "Text-to-Sign Converter":
    st.markdown("<h1 class='main-title'>Text-to-Sign Converter 🔠</h1>", unsafe_allow_html=True)
    st.write("Type a word and see how to sign it using the ASL alphabet!")
    
    text_input = st.text_input("Enter a word:", "HELLO").upper()
    text_input = "".join([c for c in text_input if c.isalpha()])
    
    if text_input:
        cols = st.columns(min(len(text_input), 8))
        
        for i, char in enumerate(text_input):
            col_idx = i % 8
            if i > 0 and col_idx == 0:
                cols = st.columns(min(len(text_input) - i, 8))
            
            with cols[col_idx]:
                url = f"https://www.lifeprint.com/asl101/fingerspelling/abc-gifs/{char.lower()}.gif"
                st.image(url, caption=char, use_container_width=True)

elif page == "Live Class":
    st.markdown("<h1 class='main-title'>Live Sign Language Class 🧑‍🏫</h1>", unsafe_allow_html=True)
    st.write("Join the live interactive class directly from here without leaving the website!")
    
    st.markdown(f"""
    <div class="info-card" style="margin-bottom: 20px;">
        <h3>How it works (Ye Kaise Kaam Karega?):</h3>
        <ul>
            <li><b>Teacher Ke Liye:</b> Ek Room Name set karein (jaise 'LearnASL_Today') aur 'Join Class' dabayein. Aap automatically class start kar denge.</li>
            <li><b>Students Ke Liye:</b> Teacher ne jo Room Name diya hai, same wahi naam yahan daalein aur 'Join Class' dabayein.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    room_name = st.text_input("Enter Class Room Name:", "SignLanguage101")
    
    if st.button("Join Class", type="primary"):
        import streamlit.components.v1 as components
        
        html_code = f"""
        <iframe allow="camera; microphone; display-capture; autoplay; clipboard-write" 
                src="https://meet.jit.si/{room_name}" 
                style="height: 700px; width: 100%; border: 0px; border-radius: 16px; box-shadow: 0 10px 30px {card_hover_shadow}; border: 1px solid {card_border};">
        </iframe>
        """
        components.html(html_code, height=700)
