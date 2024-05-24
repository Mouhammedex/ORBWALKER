import os, sys
try:
    import requests, ssl, time, random, string, threading, cv2, numpy as np, pyautogui, keyboard, win32gui, win32ui, warnings, win32con, mss, bettercam
    from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QSlider, QLineEdit, QCheckBox, QGroupBox, QHBoxLayout, QFormLayout, QRadioButton)
    from PyQt5.QtCore import Qt
    from win32api import *
except Exception as e:
    try:
        print(f"Error: {e}")
        os.system("pip install requests opencv-python numpy pyautogui keyboard warnings mss bettercam PyQt5")
    except:pass

warnings.filterwarnings("ignore", message="Unverified HTTPS request")

class MADORBWALKER:
    def __init__(self, url, ssl_context):
        self.url = url
        self.ssl_context = ssl_context
        self.WID, self.HIG = pyautogui.size()
        self.WIDD, self.HIGG = int(self.HIG * 0.051), int(self.WID * 0.08)
        self.running = False
        self.scale = 1
        self.scale_enabled = True
        self.status = "Status: Stopped"
        self.combokey1 = ''
        self.combokey2 = ''
        self.combokey1_enabled = False
        self.combokey2_enabled = False
        self.stop_flag = threading.Event()
        self.res_width = 1920
        self.res_height = 1080
        self.selected_detector = 1
        self.offset_x = 60
        self.offset_y1 = 125
        self.key='space'
    def IMG_DETECTOR3(self):
        enemy_img = cv2.imread("image.jpg", cv2.IMREAD_COLOR)
        camera = bettercam.create(output_color="BGR", region=(0, 0, self.res_width, self.res_height))
        try:
            frame = camera.grab()
            screenshot_np = np.array(frame, dtype=np.uint8)
            result = cv2.matchTemplate(screenshot_np, enemy_img, cv2.TM_CCORR_NORMED)
            threshold = 0.95
            yloc, xloc = np.where(result >= threshold)
            self.coordinates = []
            for x, y in zip(xloc, yloc):
                self.coordinates.append([x, y])
            self.cursor_pos = GetCursorPos()
            nearest_coord = min(self.coordinates, key=lambda c: np.linalg.norm(np.array(c) - np.array(self.cursor_pos)))
            return [nearest_coord[0] + self.offset_x, nearest_coord[1] + self.offset_y1]
        except:
            pass

    def IMG_DETECTOR2(self):
        monitor = {'top': 0, 'left': 0, 'width': self.res_width, 'height': self.res_height}
        enemy_img_path = "image.jpg"
        enemy_img = cv2.imread(enemy_img_path, cv2.IMREAD_COLOR)
        try:
            with mss.mss() as sct:
                img = sct.grab(monitor)
                screenshot_np = np.array(img, dtype=np.uint8)
                image = cv2.cvtColor(screenshot_np, cv2.COLOR_BGRA2BGR)
                result = cv2.matchTemplate(image, enemy_img, cv2.TM_CCORR_NORMED)
                threshold = 0.95
                yloc, xloc = np.where(result >= threshold)
                self.coordinates = []
                for x, y in zip(xloc, yloc):
                    self.coordinates.append([x, y])
                self.cursor_pos = GetCursorPos()
                nearest_coord = min(self.coordinates, key=lambda c: np.linalg.norm(np.array(c) - np.array(self.cursor_pos)))
                return [nearest_coord[0] + self.offset_x, nearest_coord[1] + self.offset_y1]
        except:
            pass

    def IMG_DETECTOR(self):
        try:
            w, h = self.res_width, self.res_height
            hwnd = win32gui.FindWindow(None, 'Discord:mohaxx1')
            wDC = win32gui.GetWindowDC(hwnd)
            dcObj = win32ui.CreateDCFromHandle(wDC)
            cDC = dcObj.CreateCompatibleDC()
            dataBitMap = win32ui.CreateBitmap()
            dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
            cDC.SelectObject(dataBitMap)
            cDC.BitBlt((0, 0), (w, h), dcObj, (0, 0), win32con.SRCCOPY)
            signedIntsArray = dataBitMap.GetBitmapBits(True)
            img = np.frombuffer(signedIntsArray, dtype='uint8')
            img.shape = (h, w, 4)
            dcObj.DeleteDC()
            cDC.DeleteDC()
            win32gui.ReleaseDC(hwnd, wDC)
            win32gui.DeleteObject(dataBitMap.GetHandle())
            img = img[..., :3]
            img = np.array(img)
            enemy_img = cv2.imread("image.jpg", cv2.IMREAD_UNCHANGED)
            result = cv2.matchTemplate(img, enemy_img, cv2.TM_CCORR_NORMED)
            yloc, xloc = np.where(result >= 0.95)
            mouse_x, mouse_y = win32gui.GetCursorPos()
            min_distance = float('inf')
            nearest_coord = None
            for x, y in zip(xloc, yloc):
                distance = np.sqrt((x - mouse_x) ** 2 + (y - mouse_y) ** 2)
                if distance < min_distance:
                    min_distance = distance
                    nearest_coord = [x + self.offset_x, y + self.offset_y1]
            return nearest_coord
        except Exception as e:
            print("Error getting nearest coordinates:", e)
            return None

    def arena_Mode_Attack_speed(self):
        try:
            data = requests.get('https://127.0.0.1:2999/liveclientdata/allgamedata', verify=False)
            return data.json()['activePlayer']['championStats']['attackSpeed']
        except Exception as e:
            print(f"arena_Mode_Attack_speed : {e}")

    def RiftListner(self):
        os.system('cls')
        while not self.stop_flag.is_set():
            self.AttackSpeedFromApi = self.arena_Mode_Attack_speed()
            self.xyz = self.get_selected_detector()()
            os.system(f"title {random.choice(string.ascii_letters)}")
            try:
                if keyboard.is_pressed(self.key):
                    self.KittingAA()
                else:
                    keyboard.unhook_all_hotkeys()
            except Exception as e:
                print(f"RiftListner : {e}")

    def KittingAA(self):
        attack = 0.737 / (self.AttackSpeedFromApi * self.scale) * 0.40
        move = 1 / (self.AttackSpeedFromApi * self.scale) * 0.595
        if self.combokey1_enabled:
            keyboard.press(self.combokey1)
            keyboard.release(self.combokey1)
        if self.combokey2_enabled:
            keyboard.press(self.combokey2)
            keyboard.release(self.combokey2)
        keyboard.press('`')
        keyboard.release('`')
        start_x, start_y = pyautogui.position()
        pyautogui.PAUSE = 0.01
        SetCursorPos(self.xyz)
        pyautogui.mouseDown(button='right')
        pyautogui.mouseUp(button='right')
        time.sleep(0.0000001)
        pyautogui.moveTo(start_x, start_y, _pause=False)
        pyautogui.moveTo(start_x, start_y, _pause=False)
        time.sleep(attack)
        start_time = time.time()
        while time.time() - start_time <= move:
            pyautogui.mouseDown(button='right')
            pyautogui.mouseUp(button='right')
            time.sleep(0.025)
            if time.time() - start_time >= move:
                keyboard.send('space', do_press=False, do_release=True)
                break
        keyboard.unhook_all_hotkeys()

    def start(self):
        if not self.running:
            self.running = True
            self.status = "Status: Running"
            status_label.setText(self.status)
            self.stop_flag.clear()
            self.listener_thread = threading.Thread(target=self.RiftListner)
            self.listener_thread.start()

    def stop(self):
        if self.running:
            self.running = False
            self.stop_flag.set()
            self.listener_thread.join()
            self.status = "Status: Stopped"
            status_label.setText(self.status)

    def toggle_scale_adjustment(self):
        self.scale_enabled = not self.scale_enabled
        print("Scale adjustment:", "Enabled" if self.scale_enabled else "Disabled")

    def update_scale(self, val):
        if self.scale_enabled:
            self.scale = max(0.50, min(float(val) / 100.0, 2.5))
            scale_label.setText(f"Attack Range : {self.scale:.2f}")

    def update_combokey1_state(self, state):
        self.combokey1_enabled = state == Qt.Checked
        combokey1_input.setVisible(self.combokey1_enabled)

    def update_combokey2_state(self, state):
        self.combokey2_enabled = state == Qt.Checked
        combokey2_input.setVisible(self.combokey2_enabled)

    def update_combokey1(self, text):
        self.combokey1 = text

    def update_combokey2(self, text):
        self.combokey2 = text

    def update_resolution_width(self, text):
        try:
            self.res_width = int(text)
        except ValueError:
            pass

    def update_resolution_height(self, text):
        try:
            self.res_height = int(text)
        except ValueError:
            pass

    def update_selected_detector(self, value):
        self.selected_detector = int(value)

    def get_selected_detector(self):
        if self.selected_detector == 1:
            return self.IMG_DETECTOR
        elif self.selected_detector == 2:
            return self.IMG_DETECTOR2
        elif self.selected_detector == 3:
            return self.IMG_DETECTOR3
        else:
            raise ValueError("Invalid detector selected")

    def update_offset_x(self, text):
        try:
            self.offset_x = int(text)
        except ValueError:
            pass

    def update_offset_y1(self, text):
        try:
            self.offset_y1 = int(text)
        except ValueError:
            pass

    def update_key(self, text):
        try:
            self.key = (text)
        except ValueError:
            pass

if __name__ == "__main__":
    URL = "https://127.0.0.1:2999/liveclientdata/allgamedata"
    SSL_CONTEXT = ssl.create_default_context()
    SSL_CONTEXT.check_hostname = False
    SSL_CONTEXT.verify_mode = ssl.CERT_NONE

    bot = MADORBWALKER  (URL, SSL_CONTEXT)

    app = QApplication([])
    window = QWidget()
    window.setWindowTitle(random.choice(string.ascii_letters))
    layout = QVBoxLayout()
    app.setStyleSheet("""
QWidget {
    background-color: #111;
    color: #ddd;
    font-family: Arial, sans-serif;
    font-size: 12px;
}
QGroupBox {
    background-color: #111;
    border: 1px solid #333;
    border-radius: 5px;
    margin-top: 5px;
    padding: 5px;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 3px;
    color: #bbb;
}
QPushButton {
    background-color: #222;
    border: none;
    color: #ddd;
    padding: 3px 8px;
    font-size: 12px;
    border-radius: 3px;
    margin-top: 3px;
}
QPushButton:hover {
    background-color: #333; /* Darker Gray */
}
QPushButton:pressed {
    background-color: #111; /* Black */
}
QLineEdit, QLabel {
    color: #eee;
}
QSlider::groove:horizontal {
    height: 5px;
    background: #555;
    border: 1px solid #666;
    border-radius: 3px;
}
QSlider::handle:horizontal {
    background: #888;
    border: 1px solid #777;
    width: 13px;
    margin: -3px 0;
    border-radius: 5px;
}
QSlider::handle:horizontal:hover {
    background: #999;
}
QLabel {
    margin: 3px 0;
}
""")

    status_label = QLabel(bot.status)
    status_labelx = QLabel("Credits : Mouhammed [Discord : @mohaxx1]")
    layout.addWidget(status_label)
    layout.addWidget(status_labelx)
    buttons_layout = QHBoxLayout()
    start_button = QPushButton("Start Bot")
    start_button.clicked.connect(bot.start)
    buttons_layout.addWidget(start_button)
    stop_button = QPushButton("Stop Bot")
    stop_button.clicked.connect(bot.stop)
    buttons_layout.addWidget(stop_button)
    layout.addLayout(buttons_layout)

    combokey1_group = QGroupBox("Combokey 1")
    combokey1_layout = QVBoxLayout()
    combokey1_checkbox = QCheckBox("Enable Combokey 1")
    combokey1_checkbox.stateChanged.connect(bot.update_combokey1_state)
    combokey1_layout.addWidget(combokey1_checkbox)
    combokey1_input = QLineEdit(bot.combokey1)
    combokey1_input.textChanged.connect(bot.update_combokey1)
    combokey1_input.setVisible(False)
    combokey1_layout.addWidget(combokey1_input)
    combokey1_group.setLayout(combokey1_layout)
    layout.addWidget(combokey1_group)

    combokey2_group = QGroupBox("Combokey 2")
    combokey2_layout = QVBoxLayout()
    combokey2_checkbox = QCheckBox("Enable Combokey 2")
    combokey2_checkbox.stateChanged.connect(bot.update_combokey2_state)
    combokey2_layout.addWidget(combokey2_checkbox)
    combokey2_input = QLineEdit(bot.combokey2)
    combokey2_input.textChanged.connect(bot.update_combokey2)
    combokey2_input.setVisible(False)
    combokey2_layout.addWidget(combokey2_input)
    combokey2_group.setLayout(combokey2_layout)
    layout.addWidget(combokey2_group)

    scale_group = QGroupBox("Scale Adjustment")
    scale_layout = QVBoxLayout()
    scale_label = QLabel("Adjust Scale")
    scale_layout.addWidget(scale_label)
    scale_slider = QSlider(Qt.Horizontal)
    scale_slider.setMinimum(50)
    scale_slider.setMaximum(250)
    scale_slider.setTickInterval(1)
    scale_slider.setTickPosition(QSlider.TicksBelow)
    scale_slider.valueChanged.connect(bot.update_scale)
    scale_layout.addWidget(scale_slider)
    scale_group.setLayout(scale_layout)
    layout.addWidget(scale_group)

    resolution_group = QGroupBox("Resolution Settings")
    resolution_layout = QFormLayout()
    res_width_input = QLineEdit(str(bot.res_width))
    res_width_input.textChanged.connect(bot.update_resolution_width)
    resolution_layout.addRow("Resolution Width:", res_width_input)
    res_height_input = QLineEdit(str(bot.res_height))
    res_height_input.textChanged.connect(bot.update_resolution_height)
    resolution_layout.addRow("Resolution Height:", res_height_input)
    resolution_group.setLayout(resolution_layout)
    layout.addWidget(resolution_group)

    detector_group = QGroupBox("Image Detector")
    detector_layout = QVBoxLayout()

    detector1_radio = QRadioButton("Detector 1 [MAX SCALE : 1.60-165]")
    detector1_radio.setChecked(True)
    detector1_radio.toggled.connect(lambda: bot.update_selected_detector(1))
    detector_layout.addWidget(detector1_radio)

    detector2_radio = QRadioButton("Detector 2 [MAX SCALE : 120-125]")
    detector2_radio.toggled.connect(lambda: bot.update_selected_detector(2))
    detector_layout.addWidget(detector2_radio)

    detector3_radio = QRadioButton("Detector 3 [MAX SCALE : 2.40]")
    detector3_radio.toggled.connect(lambda: bot.update_selected_detector(3))
    detector_layout.addWidget(detector3_radio)

    detector_group.setLayout(detector_layout)
    layout.addWidget(detector_group)

    offset_group = QGroupBox("Other")
    offset_layout = QFormLayout()
    offset_x_input = QLineEdit(str(bot.offset_x))
    offset_x_input.textChanged.connect(bot.update_offset_x)
    offset_layout.addRow("Offset X:", offset_x_input)
    offset_y1_input = QLineEdit(str(bot.offset_y1))
    offset_y1_input.textChanged.connect(bot.update_offset_y1)
    offset_layout.addRow("Offset Y:", offset_y1_input)
    key_input = QLineEdit(bot.key)  # This was changed to a text input
    key_input.textChanged.connect(bot.update_key)
    offset_layout.addRow("Key:", key_input)  # Updated label for clarity
    offset_group.setLayout(offset_layout)
    layout.addWidget(offset_group)

    window.setLayout(layout)
    window.show()
    app.exec_()
