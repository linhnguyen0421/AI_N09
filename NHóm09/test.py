import cv2
import mediapipe as mp
import pyautogui

#pip install pyuac
#pip install pypiwin32

#from pyuac import main_requires_admin

# Initialize MediaPipe hand detection
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Initialize PyAutoGUI for mouse control
pyautogui.FAILSAFE = False

# Set the screen dimensions
screen_width, screen_height = pyautogui.size()
#@main_requires_admin
def detect_and_control():
    cap = cv2.VideoCapture(0)
# ye
    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        if not ret:
            break

        # Detect hands hon ca yeu duc phuc
        results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Get the coordinates of the landmarks
                landmark_list = []
                for landmark in hand_landmarks.landmark:
                    landmark_list.append((int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0])))

                # Determine the state of the hand
                state = "Idle"
                if len(landmark_list) >= 4:
                    # Check if three fingers are raised
                    if landmark_list[4][1] < landmark_list[2][1] and landmark_list[8][1] < landmark_list[7][1] and landmark_list[12][1] < landmark_list[11][1] and landmark_list[16][1] < landmark_list[15][1] and landmark_list[20][1] < landmark_list[19][1]:
                        # Control the mouse cursor
                        x = int(landmark_list[8][0] * screen_width / frame.shape[1])
                        y = int(landmark_list[8][1] * screen_height / frame.shape[0])
                        pyautogui.moveTo(x * 1.5, y * 1.5)
                        state = "Cursor Control"
                    # Check if the index finger is bent
                    elif landmark_list[8][1] > landmark_list[7][1]:
                        # Left click
                        pyautogui.click()
                        state = "Left Click"
                        cv2.waitKey(250)
                    # Check if the index and middle fingers are bent
                    elif landmark_list[12][1] > landmark_list[11][1]:
                        # Right click
                        pyautogui.rightClick()
                        state = "Right Click"
                        cv2.waitKey(500)

                    elif landmark_list[4][1] > landmark_list[3][1]:
                        pyautogui.hotkey('ctrl + win + o')
                        state = "On-screen keyboards"
                        cv2.waitKey(500)

                print(state)

                # Draw the hand landmarks
                mp_drawing = mp.solutions.drawing_utils
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        cv2.imshow("Hand Gesture Controlled Mouse", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    detect_and_control()