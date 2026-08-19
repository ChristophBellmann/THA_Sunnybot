import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.graphics.texture import Texture
from kivy.uix.camera import Camera
import os
import numpy as np
from datetime import datetime
from jnius import autoclass
from transceiver import UDPTransceiver
from spotcam import SpotCam
import cv2  # Import cv2 module

kivy.require('2.0.0')


class MyRoot(BoxLayout):
    display_emotion = ObjectProperty(None)
    display_direction = ObjectProperty(None)
    image_display = ObjectProperty(None)
    camera_display = ObjectProperty(None)
    current_camera_index = 0
    happyness_threshold = 50  # Default happyness threshold

    def __init__(self, **kwargs):
        super(MyRoot, self).__init__(**kwargs)
        self.emotion_popup = None  # init popup
        self.cv_text_popup = None  # init cv text popup
        self.acquire_wake_lock()
        # Create folder and text file during initialization
        self.create_folder_click()  # init folder
        self.create_textfile_click()  # init send data file
        self.create_processing_file()  # init processing data file
        self.udp_transceiver = UDPTransceiver()  # Init UDP transceiver
        self.spot_cam = SpotCam()  # Init SpotCam
        Window.bind(on_resize=self.on_orientation)  # Register the orientation change event
        Clock.schedule_interval(self.update, 1)  # Schedule the update method to run every second

    def acquire_wake_lock(self):
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        activity = PythonActivity.mActivity
        Context = autoclass('android.content.Context')
        PowerManager = autoclass('android.os.PowerManager')
        power_manager = activity.getSystemService(Context.POWER_SERVICE)
        self.wake_lock = power_manager.newWakeLock(PowerManager.FULL_WAKE_LOCK, 'MyApp::MyWakelockTag')
        self.wake_lock.acquire()

    def get_internal_storage_path(self):
        return App.get_running_app().user_data_dir

    def create_folder_click(self):
        folder_path = os.path.join(self.get_internal_storage_path(), "SunSeeker")
        try:
            os.makedirs(folder_path, exist_ok=True)
            print(f"Folder created at: {folder_path}")
        except Exception as e:
            print(f"Failed to create folder: {e}")
        self.folder_path = folder_path

    def create_textfile_click(self):
        file_path = os.path.join(self.folder_path, "send_packages.txt")
        try:
            with open(file_path, "w") as file:
                file.write("Timestamp, Velocity, Alpha\n")
            print(f"File created at: {file_path}")
        except Exception as e:
            print(f"Failed to create file: {e}")

    def create_processing_file(self):
        file_path = os.path.join(self.folder_path, "processing.txt")
        try:
            with open(file_path, "w") as file:
                file.write("Timestamp, Brightness, Location, Height, Width, Area, Direction\n")
            print(f"Processing file created at: {file_path}")
        except Exception as e:
            print(f"Failed to create processing file: {e}")

    def show_textfile_click(self):
        file_path = os.path.join(self.folder_path, "send_packages.txt")
        try:
            with open(file_path, "r") as file:
                content = file.read()
            print(f"File content: {content}")
            self.show_scrollable_popup(content, "Transmission File Content")
        except Exception as e:
            print(f"Failed to read file: {e}")

    def show_processing_file_click(self):
        file_path = os.path.join(self.folder_path, "processing.txt")
        try:
            with open(file_path, "r") as file:
                content = file.read()
            print(f"File content: {content}")
            self.show_scrollable_popup(content, "Processing File Content")
        except Exception as e:
            print(f"Failed to read file: {e}")

    def show_scrollable_popup(self, content, title):
        layout = GridLayout(cols=1, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        label = Label(text=content, font_size=32, text_size=(800, None), size_hint_y=None)
        label.bind(texture_size=label.setter('size'))
        layout.add_widget(label)
        scroll_view = ScrollView(size_hint=(1, 1))
        scroll_view.add_widget(layout)
        popup = Popup(title=title, content=scroll_view, size_hint=(0.8, 0.8))
        popup.open()

    def show_popup(self, content, title):
        layout = GridLayout(cols=1, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        label = Label(text=content, font_size=32, text_size=(800, None), size_hint_y=None)
        label.bind(texture_size=label.setter('size'))
        layout.add_widget(label)
        scroll_view = ScrollView(size_hint=(1, 1))
        scroll_view.add_widget(layout)
        popup = Popup(title=title, content=scroll_view, size_hint=(0.8, 0.8))
        popup.open()

    def set_emotionnumber(self, relative_brightness):
        if relative_brightness > self.happyness_threshold:
            emotion = f':) {relative_brightness:.2f}%'
        else:
            emotion = f':( {relative_brightness:.2f}%'
        self.display_emotion.text = emotion
        if self.emotion_popup:
            self.emotion_popup.content.text = emotion

    def set_directionnumber(self, normalized_center_x):
        if normalized_center_x > 30:
            direction = f'→ {normalized_center_x:.2f}'
        elif 10 < normalized_center_x <= 30:
            direction = f'↗ {normalized_center_x:.2f}'
        elif -30 <= normalized_center_x < -10:
            direction = f'↖ {normalized_center_x:.2f}'
        elif normalized_center_x < -30:
            direction = f'← {normalized_center_x:.2f}'
        else:
            direction = f'↑ {normalized_center_x:.2f}'
        self.display_direction.text = direction

    def save_transmission_data(self, relative_brightness, normalized_center_x):
        if relative_brightness < self.happyness_threshold:
            return

        max_brightness = self.get_max_brightness()
        velocity = self.map_brightness_to_velocity(relative_brightness, max_brightness)
        alpha = self.map_alpha(normalized_center_x)  # Map alpha before sending

        file_path = os.path.join(self.folder_path, "send_packages.txt")
        try:
            with open(file_path, "a") as file:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]  # ms, want to have 3 digits
                data = f"{timestamp},V={velocity:.3f} Alpha={alpha}"
                file.write(f"{data}\n")
            print(f"Line added to file at: {file_path}")
            self.send_velocity_and_alpha(velocity, alpha)
        except Exception as e:
            print(f"Failed to add line to file: {e}")

    def send_velocity_and_alpha(self, velocity, alpha):
        data = f"V={velocity:.3f} Alpha={alpha}"
        self.udp_transceiver.send_data(data)

    def get_max_brightness(self):
        file_path = os.path.join(self.folder_path, "processing.txt")
        try:
            with open(file_path, "r") as file:
                lines = file.readlines()[1:]  # Skip header
                brightness_values = [min(float(line.split(",")[1].strip('% ')), 100) for line in lines]
            return max(brightness_values) if brightness_values else 100
        except Exception as e:
            print(f"Failed to get max brightness: {e}")
            return 100

    def map_brightness_to_velocity(self, brightness, max_brightness):
        if max_brightness == 0:
            return 0.0  # Avoid division by zero

        velocity = (brightness / max_brightness) * 0.175
        return velocity

    def map_alpha(self, normalized_center_x):
        if normalized_center_x >= 0:
            alpha = (normalized_center_x / 100) * 90
        else:
            alpha = 360 + (normalized_center_x / 100) * 90
        return int(alpha)

    def on_orientation(self, instance, width, height):
        if width > height:
            self.orientation = 'horizontal'
        else:
            self.orientation = 'vertical'

    def update(self, dt):
        try:
            texture = self.camera_display.texture  # Capture the camera feed
            if texture:
                frame = np.frombuffer(texture.pixels, np.uint8).reshape(texture.height, texture.width, 4)
                frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)
                bright_percentage, location_text, height_text, width_text, area_text, direction_text, normalized_center_x = self.spot_cam.process_image(frame)  # overlay text and process to find bright area
                relative_brightness = self.calculate_relative_brightness(bright_percentage)  # Calculate relative brightness
                self.set_emotionnumber(relative_brightness)  # Update the emotion based on the relative brightness
                self.set_directionnumber(normalized_center_x)  # Update the direction based on normalized_center_x
                processed_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
                h, w = processed_frame.shape[:2]
                buf1 = processed_frame.tostring()
                image_texture = Texture.create(size=(w, h), colorfmt='rgba')
                image_texture.blit_buffer(buf1, colorfmt='rgba', bufferfmt='ubyte')
                self.image_display.texture = image_texture
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                self.save_processing_data(timestamp, bright_percentage, location_text, height_text, width_text, area_text, direction_text)
                self.save_transmission_data(relative_brightness, normalized_center_x)

                # Update CV text popup content
                cv_text = (f'Brightness: {bright_percentage:.2f}%\n'
                           f'{location_text}\n'
                           f'Height: {height_text}\n'
                           f'Width: {width_text}\n'
                           f'Area: {area_text}\n'
                           f'Direction: {direction_text}')
                if self.cv_text_popup:
                    self.cv_text_popup.content.text = cv_text
        except Exception as e:
            print(f"Error capturing or displaying image: {e}")

    def save_processing_data(self, timestamp, bright_percentage, location, height, width, area, direction):
        file_path = os.path.join(self.folder_path, "processing.txt")
        try:
            with open(file_path, "a") as file:
                data = f"{timestamp}, {bright_percentage:.2f}%, {location}, {height}, {width}, {area}, {direction}\n"
                file.write(data)
            print(f"Processing data saved to file at: {file_path}")
        except Exception as e:
            print(f"Failed to save processing data to file: {e}")

    def calculate_relative_brightness(self, current_brightness):
        file_path = os.path.join(self.folder_path, "processing.txt")
        try:
            with open(file_path, "r") as file:
                lines = file.readlines()[1:]  # Skip header
                brightness_values = [float(line.split(",")[1].strip('% ')) for line in lines]

            if not brightness_values:
                return current_brightness

            min_brightness = min(brightness_values)
            max_brightness = max(brightness_values)

            if max_brightness == min_brightness:
                return 100  # Avoid division by zero

            relative_brightness = ((current_brightness - min_brightness) / (max_brightness - min_brightness)) * 100
            return relative_brightness

        except Exception as e:
            print(f"Failed to calculate relative brightness: {e}")
            return current_brightness

    def show_fullscreen_emotion(self):
        content = Label(text=self.display_emotion.text, font_name='UniFont', font_size=200)
        self.emotion_popup = Popup(title='', content=content, size_hint=(1, 1))
        content.bind(on_touch_down=self.emotion_popup.dismiss)
        self.emotion_popup.open()

    def show_cv_text_popup(self):
        if not self.cv_text_popup:
            content = Label(text='', font_name='UniFont', font_size=64)
            self.cv_text_popup = Popup(title='', content=content, size_hint=(1, 1))
            content.bind(on_touch_down=self.cv_text_popup.dismiss)
        self.cv_text_popup.open()

    def switch_camera(self):
        self.current_camera_index = (self.current_camera_index + 1) % 2
        self.camera_display.play = False
        self.camera_display.index = self.current_camera_index
        self.camera_display.play = True


class SunseekerApp(App):
    def build(self):
        LabelBase.register(name='UniFont', fn_regular='unifont-15.0.01.ttf')
        return MyRoot()


if __name__ == '__main__':
    SunseekerApp().run()
