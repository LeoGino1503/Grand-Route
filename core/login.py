from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
import requests
import os

# -------------------------
# LOGIN SCREEN
# -------------------------
class LoginScreen(Screen):
    def __init__(self, API_LOGIN_URL, **kwargs):
        super().__init__(**kwargs)
        self.API_LOGIN_URL = API_LOGIN_URL
        self.username_input = TextInput(
            hint_text="Username",
            size_hint=(0.4, 0.08),
            pos_hint={"center_x": 0.5, "center_y": 0.6}
        )
        self.password_input = TextInput(
            hint_text="Password",
            password=True,
            size_hint=(0.4, 0.08),
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        self.message_label = Label(
            text="",
            color=(1,0,0,1),
            pos_hint={"center_x": 0.5, "center_y": 0.45}
        )
        login_btn = Button(
            text="Login",
            size_hint=(0.2, 0.08),
            pos_hint={"center_x": 0.5, "center_y": 0.35}
        )
        login_btn.bind(on_release=self.try_login)

        self.add_widget(self.username_input)
        self.add_widget(self.password_input)
        self.add_widget(self.message_label)
        self.add_widget(login_btn)

    def try_login(self, instance):
        username = self.username_input.text
        password = self.password_input.text

        try:
            response = requests.post(self.API_LOGIN_URL, json={
                "username": username,
                "password": password
            })
            if response.status_code == 200:
                data = response.json()
                # Chuyển sang màn hình game
                self.manager.get_screen("game").setup_player(data)
                self.manager.current = "game"
            else:
                self.message_label.text = response.json().get("detail", "Login failed")
        except Exception as e:
            self.message_label.text = str(e)