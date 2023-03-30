from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.core.window import Window
from kivy.uix.label import Label
from functools import partial

from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.storage.jsonstore import JsonStore
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup

from kivy.factory import Factory

kv = '''
#:import hex kivy.utils.get_color_from_hex
#:import Button kivy.uix.button.Button
#:import Factory kivy.factory.Factory
MDBoxLayout:
    orientation: "vertical"
    MDTopAppBar:
        Image:
            source: "logo.png"
            size_hint: None, None
            size: 80, 80
            pos_hint: {"center_x": .5}

    MDBottomNavigation:
        MDBottomNavigationItem:
            id: screen1
            name: 'screen 1'
            text: 'Workouts'
            icon: 'weight-lifter'
            #Excersises:
            BoxLayout:
                orientation: 'vertical'
                Button:
                    id: edit_button
                    text: 'Edit'
                    pos_hint: {'center_x': .9, 'center_y': .9}
                    size_hint: .2, .1
                    on_release: app.visibility_handler([addExercise_button, exercise_name_input]), app.edit_button_handler()
                ScrollView:
                    id: exercise_scroll
                    BoxLayout:
                        id: exercise_box
                        orientation: 'vertical'
                        size_hint_y: None
                        height: self.minimum_height
                TextInput:
                    id: exercise_name_input
                    size_hint_y: None
                    size: 100, 50
                Button:
                    id: addExercise_button
                    text: 'add'
                    on_release: app.add_new_widget(exercise_name_input.text)
                    size_hint_y: None
                    size: 100, 50
        MDBottomNavigationItem:
            name: 'screen 2'
            text: 'Progress'
            icon: 'chart-line'
            MDLabel:
                text: 'Progress'
                halign: 'center'
        MDBottomNavigationItem:
            name: 'screen 3'
            text: 'Settings'
            icon: 'cog-outline'
            MDLabel:
                text: 'Settings'
                halign: 'center'
        MDBottomNavigationItem:
            name: 'screen 4'
            text: 'Tools'
            icon: 'tools'
            MDLabel:
                text: 'Tools'
                halign: 'center'
<ExercisePopup@Popup>:
    auto_dismiss: True
    size_hint: .8, .8
    pos_hint: {'center_x': .5, 'center_y': .52}
    title: 'Popup'
    BoxLayout:
        orientation: 'vertical'
        ScrollView:
            id: popup_scroll
            BoxLayout:
                id: exercise_info_box
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height
        Button:
            on_release: app.add_new_widget_popup_scroll()
        Button:
            size_hint_y: 0.1
            text: 'Dismiss'
            font_size: 24
            on_release: root.dismiss()
'''

class DemoGPBApp(MDApp):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.activeExerciseList = []
        
        #Flags
        self.flagIsHidenEdit_uix = False
        self.flagEdit_button = True
        
    def build(self, *args):
                    
        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepOrange"
        Window.size = (480, 800)
        
        self.count = 0
        
        return Builder.load_string(kv)
    
    def visibility_handler(self, widgets, *args):
        if(self.flagIsHidenEdit_uix):
            self.hide_me(widgets)
        else:
            self.show_me(widgets)
        
        self.flagIsHidenEdit_uix = not self.flagIsHidenEdit_uix
           
    
    def hide_me(self, widgets, *args):
        if(type(widgets) != list):
            widgets = [widgets]
        for widget in widgets:
            widget.opacity = 0
            widget.disabled = True
    
    def show_me(self, widgets, *args):
        if(type(widgets) != list):
            widgets = [widgets]
        for widget in widgets:
            widget.opacity = 1
            widget.disabled = False

    
    def add_new_widget(self, text,mode="add",*args):
        
        if(text == ""):
            return
            
        store = JsonStore('save.json')
        vp_height = self.root.ids.exercise_scroll.viewport_size[1]
        sv_height = self.root.ids.exercise_scroll.height


        # add a new widget (must have preset height)
        boxlayout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=50)
        boxlayout.add_widget(Label(text= text, size_hint=(1, None), height=50))
        removeAndInfo_button = Button(text="Info", size_hint=(0.25, None), height=50, disabled=False, opacity=1)
        boxlayout.add_widget(removeAndInfo_button)

        self.infoPopupHandler(boxlayout)

        if(mode != "reload"):
            self.activeExerciseList.append(boxlayout)
        
        self.root.ids.exercise_box.add_widget(boxlayout)
        
        if(mode != "load" and mode != "reload"):
            store.put(name='Exercice',text=text, key=self.count)
            self.count += 1

        #On adding new element, show remove button
        if(mode != "load"):
            for widget in self.activeExerciseList:
                widget.children[0].text = "Delete"
                widget.children[0].on_release=partial(self.remove_widget, widget)
        
        if vp_height > sv_height:  # otherwise there is no scrolling
            # calculate y value of bottom of scrollview in the viewport
            scroll = self.root.ids.exercise_scroll.scroll_y
            bottom = scroll * (vp_height - sv_height)

            # use Clock.schedule_once because we need updated viewport height
            # this assumes that new widgets are added at the bottom
            # so the current bottom must increase by the widget height to maintain position
            Clock.schedule_once(partial(self.adjust_scroll, bottom), -1)

    def adjust_scroll(self, bottom, *args):
        vp_height = self.root.ids.exercise_scroll.viewport_size[1]
        sv_height = self.root.ids.exercise_scroll.height
        self.root.ids.exercise_scroll.scroll_y = bottom / (vp_height - sv_height)
    
    def getId(self, id, *args):
        print(id)
    
    def remove_widget(self,widgetsToRemove, *args):
                  

        store = JsonStore('save.json')
        if type(widgetsToRemove) != list:
            widgetsToRemove = [widgetsToRemove]
        
        
        for widgetToRemove in widgetsToRemove:
            try:
                self.root.ids.exercise_box.remove_widget(widgetToRemove)
                self.count -= 1
                store.delete(str(self.count))
            except:
                pass
    
    def on_start(self, *args):
        self.count = 0
        store = JsonStore('save.json')
        for item in store.find(name='Exercice'):
            self.add_new_widget((item[1]).get('text'), mode='load')
            self.count += 1
        
        #On start hide the edit section
        partial(self.hide_me, [self.root.ids.exercise_name_input, self.root.ids.addExercise_button])()
        
        return super().on_start()
    
    def edit_button_handler(self, *args):
        #On start hide the edit section
        if(self.flagEdit_button):
            
            for widget in self.activeExerciseList:
                #Change to delete button
                widget.children[0].text = "Delete"
                widget.children[0].on_release=partial(self.remove_widget, widget)
                            
            self.root.ids.edit_button.text = "Done"
        
        else:
            
            for widget in self.activeExerciseList:
                #Change to delete button
                widget.children[0].text = "Info"
                self.infoPopupHandler(widget)
            
            self.root.ids.edit_button.text = "Edit"
            
        self.flagEdit_button = not self.flagEdit_button
        
        return super().on_start()

    def infoPopupHandler(self,widget,*args):
        widget.children[0].on_release=Factory.ExercisePopup(
            title=widget.children[1].text,
            ).open

    def testAdding(self, *args):
        print("test")
        
    def add_new_widget_popup_scroll(self, *args):
        
        store = JsonStore('popUpContent.json')
    
        
        vp_height = self.root.parent.children[0].ids.popup_scroll.viewport_size[1]
        sv_height = self.root.parent.children[0].ids.popup_scroll.height
        
        boxlayout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=50)
        boxlayout.add_widget(Label(text= "test", size_hint=(1, None), height=50))
        
        self.root.parent.children[0].ids.exercise_info_box.add_widget(boxlayout)
        
        if vp_height > sv_height:  # otherwise there is no scrolling
            # calculate y value of bottom of scrollview in the viewport
            scroll = self.root.parent.children[0].ids.popup_scroll.scroll_y
            bottom = scroll * (vp_height - sv_height)

            # use Clock.schedule_once because we need updated viewport height
            # this assumes that new widgets are added at the bottom
            # so the current bottom must increase by the widget height to maintain position
            Clock.schedule_once(self.adjust_scroll_popup_scroll, bottom)

    def adjust_scroll_popup_scroll(self, bottom, *args):
        try:
            vp_height = self.root.parent.children[0].ids.popup_scroll.viewport_size[1]
            sv_height = self.root.parent.children[0].ids.popup_scroll.height
            self.root.parent.children[0].ids.popup_scroll.scroll_y = bottom / (vp_height - sv_height)
        except:
            print("error")
    
if __name__ == '__main__':
    DemoGPBApp().run()
