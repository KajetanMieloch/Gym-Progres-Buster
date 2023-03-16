#!/usr/bin/python

from kivy.config import Config
Config.set('graphics','resizable',0)

import kivy
kivy.require('1.8.0')

from kivy.app import App
from kivy.core.window import Window
from kivy.properties import ObjectProperty, StringProperty
from kivy.logger import Logger

from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button


class ButtonListItem(Button):
    wid = StringProperty('')
    image = StringProperty('')
    title = StringProperty('')
    label = StringProperty('')
    pass

    def click(button):
        global app
        app.clearSelection()
        button.background_color = (0,160,66,.9)
        Logger.info(button.title + ": wid=" + button.wid)

class ButtonList(GridLayout):
    pass

class SelectFruit(App):
    def build(self):
        Window.size = 400, (4 * 90)

        self.layout = ButtonList()
        self.layout.size = 400, (8 * 78)

        self.root = ScrollView(
                        size_hint=(None, None), 
                        size=Window.size,
                        scroll_type=['bars', 'content']
                    )
        self.root.add_widget(self.layout)

        ib = ButtonListItem(
                wid="0", 
                image="Icons/BP.jpg", 
                title="Bench Press", 
                label="Bench Press"
            )
        self.layout.add_widget(ib)

        ib = ButtonListItem(
                wid="1", 
                image="Icons/SQ.jpg", 
                title="Squat", 
                label="Squat"
            )
        self.layout.add_widget(ib)

        ib = ButtonListItem(
                wid="2", 
                image="Icons/DL.jpg", 
                title="Deadlift", 
                label="Deadlift"
            )
        self.layout.add_widget(ib)

        ib = ButtonListItem(
                wid="3", 
                image="Icons/CU.jpg", 
                title="Curling", 
                label="Curling"
            )
        self.layout.add_widget(ib)

        return self.root

    def clearSelection(self):
        for child in self.layout.children:
            child.background_color = (1,1,1,1)

if __name__ == "__main__":
    app = SelectFruit()
    app.run()