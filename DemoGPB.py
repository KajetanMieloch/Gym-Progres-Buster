from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.core.window import Window
from kivy.uix.label import Label

from kivy.uix.screenmanager import ScreenManager, Screen

sm = ScreenManager()

class MainScreen(MDScreen):
    pass

class Exercises(MDScreen):
    pass


class DemoGPBApp(MDApp):
    def build(self):
        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepOrange"
        sm.add_widget(MainScreen(name='login'))
        Window.size = (480, 800)
        return sm

if __name__ == '__main__':
    DemoGPBApp().run()