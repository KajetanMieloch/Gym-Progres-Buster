import threading
import sqlite3 as lite
from kivy.app import App
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen

from kivy.uix.boxlayout import BoxLayout

Window.size = {300,600}

class CustomWidget(BoxLayout):
    
    def remove(self):
        self.parent.remove_widget(self)
    
    def update_label(self):
        self.ids.label1.text = "Hello World"

class Start(Screen):
    
    def __init__(self, **kwargs):
        super(Start, self).__init__(**kwargs)
    
    def add_text_inputs(self):
        customWidget = CustomWidget()
        self.ids.container.add_widget(customWidget)
        
class DynamiclyApp(App):
    
    def build(self):
        return Start()

if __name__ == '__main__':
    DynamiclyApp().run()