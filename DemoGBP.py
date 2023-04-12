# Nice icons:
# human-edit


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
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.button import MDRectangleFlatIconButton
from kivymd.uix.pickers import MDDatePicker

from datetime import date

from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition


kv = """
#:import hex kivy.utils.get_color_from_hex
#:import Button kivy.uix.button.Button
#:import Factory kivy.factory.Factory
ScreenManager:
    Screen:
        name: 'MainScreen'
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
                    name: 'MainScreen'
                    text: 'Workouts'
                    icon: 'weight-lifter'
                    #Excersises:
                    MDBoxLayout:
                        orientation: 'vertical'
                        GridLayout:
                            cols: 4
                            size_hint_y: 0.1
                            MDIconButton:
                                id: sort_AZ_asc_button
                                opacity: 0
                                disabled: True
                                icon: 'sort-alphabetical-ascending'
                                theme_icon_color: "Custom"
                                icon_color: app.theme_cls.primary_color
                                pos_hint: {'center_x': .9, 'center_y': .9}
                                size_hint: .2, .1
                                on_release: app.sort_exercises("AZ_asc")
                            MDIconButton:
                                id: sort_AZ_des_button
                                opacity: 0
                                disabled: True
                                icon: 'sort-alphabetical-descending'
                                theme_icon_color: "Custom"
                                icon_color: app.theme_cls.primary_color
                                pos_hint: {'center_x': .9, 'center_y': .9}
                                size_hint: .2, .1
                                on_release: app.sort_exercises("AZ_des")
                            MDIconButton:
                                id: sort_filler_button
                                icon: 'filter'
                                theme_icon_color: "Custom"
                                icon_color: app.theme_cls.primary_color
                                pos_hint: {'center_x': .9, 'center_y': .9}
                                size_hint: .2, .1
                                on_release: app.visibility_handler([sort_AZ_asc_button, sort_AZ_des_button])
                            MDIconButton:
                                id: edit_button
                                icon: 'circle-edit-outline'
                                theme_icon_color: "Custom"
                                icon_color: app.theme_cls.primary_color
                                pos_hint: {'center_x': .9, 'center_y': .9}
                                size_hint: .2, .1
                                on_release: app.visibility_handler([addExercise_button, exercise_name_input]), app.edit_button_handler()
                        ScrollView:
                            id: exercise_scroll
                            MDBoxLayout:
                                id: exercise_box
                                orientation: 'vertical'
                                size_hint_y: None
                                height: self.minimum_height
                        GridLayout:
                            cols: 2
                            size_hint_y: 0.15
                            MDTextField:
                                hint_text: "Add your exercise"
                                id: exercise_name_input
                                size_hint_y: None
                            MDIconButton:
                                id: addExercise_button
                                icon: 'plus-circle-outline'
                                icon_color: app.theme_cls.primary_color
                                on_release: app.add_new_widget(exercise_name_input.text)
                                size_hint_y: None
                MDBottomNavigationItem:
                    name: 'Encyclopedia'
                    text: 'Encyclopedia'
                    icon: 'book-open-page-variant'
                    MDLabel:
                        text: 'Encyclopedia'
                        halign: 'center'
                MDBottomNavigationItem:
                    name: 'Progress'
                    text: 'Progress'
                    icon: 'chart-line'
                    MDLabel:
                        text: 'Progress'
                        halign: 'center'
                MDBottomNavigationItem:
                    name: 'Settings'
                    text: 'Settings'
                    icon: 'cog-outline'
                    MDLabel:
                        text: 'Settings'
                        halign: 'center'
                MDBottomNavigationItem:
                    name: 'Tools'
                    text: 'Tools'
                    icon: 'tools'
                    MDLabel:
                        text: 'Tools'
                        halign: 'center'
    Screen:
        name: 'ExerciseScreen'
        MDBoxLayout:
            orientation: "vertical"

            MDTopAppBar:
                id: exercise_screen_top_app_bar_title
                title: ""
            GridLayout:
                cols: 4
                size_hint_y: 0.1
                MDIconButton:
                    id: calendarAscendingButton
                    opacity: 0
                    disabled: True
                    icon: 'sort-calendar-ascending'
                    theme_icon_color: "Custom"
                    icon_color: app.theme_cls.primary_color
                    pos_hint: {'center_x': .9, 'center_y': .9}
                    size_hint: .2, .1
                MDIconButton:
                    id: calendarDescendingButton
                    opacity: 0
                    disabled: True
                    icon: 'sort-calendar-descending'
                    theme_icon_color: "Custom"
                    icon_color: app.theme_cls.primary_color
                    pos_hint: {'center_x': .9, 'center_y': .9}
                    size_hint: .2, .1
                MDIconButton:
                    id: sort_filler_button
                    icon: 'filter'
                    theme_icon_color: "Custom"
                    icon_color: app.theme_cls.primary_color
                    pos_hint: {'center_x': .9, 'center_y': .9}
                    size_hint: .2, .1
                    on_release: app.visibility_handler([calendarAscendingButton, calendarDescendingButton])
                MDIconButton:
                    id: edit_button_exercise_screen
                    icon: 'circle-edit-outline'
                    theme_icon_color: "Custom"
                    icon_color: app.theme_cls.primary_color
                    pos_hint: {'center_x': .9, 'center_y': .9}
                    size_hint: .2, .1
                    on_release: app.visibility_handler([addExercise_button, exercise_name_input]), app.edit_button_handler_exercise_screen()
            ScrollView:
                id: exercise_screen_scroll
                MDBoxLayout:
                    id: exercise_screen_box
                    orientation: 'vertical'
                    size_hint_y: None
                    height: self.minimum_height
            
            GridLayout:
                cols: 7
                size_hint_y: 0.15
                MDLabel:
                    size_hint_x: 0.2
                    MDIconButton:
                        icon: 'arrow-left'
                        on_release: app.screen_change("MainScreen",reset=True,returnBtn=False)
                MDRaisedButton:
                    text: "Date"
                    on_release: app.show_date_picker()
                MDTextField:
                    size_hint_x: 0.6
                    hint_text: "Nmber of reps"
                    id: exercise_reps_input_exercise_screen
                    size_hint_y: None
                    input_filter: 'int'
                MDLabel:
                    size_hint_x: 0.1
                MDTextField:
                    size_hint_x: 0.6
                    hint_text: "Nmber of sets"
                    id: exercise_sets_input_exercise_screen
                    size_hint_y: None
                    input_filter: 'int'
                MDSwitch:
                    id: exercise_dirty_exercise_screen
                    
                MDIconButton:
                    id: addExercise_button_exercise_screen
                    icon: 'plus-circle-outline'
                    icon_color: app.theme_cls.primary_color
                    on_release: app.add_new_widget_exercise_screen(exercise_screen_top_app_bar_title.title,exercise_reps_input_exercise_screen.text,exercise_sets_input_exercise_screen.text,exercise_dirty_exercise_screen.active)
                    size_hint_y: None
                
                   
                    
"""


class DemoGPBApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # global variables
        self.activeExerciseList = [[], []]
        self.activeExerciseScreenList = []
        self.date = str(date.today())

        # Flags
        self.flagIsHidenEdit_uix = False
        self.flagEdit_button = True

    def build(self, *args):

        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepOrange"
        Window.size = (480, 800)

        self.countExercisess = 0
        self.countPopup = 0

        self.countExercisessScreen = 0

        return Builder.load_string(kv)

    def on_start(self, *args):
        self.countExercisess = 0
        store = JsonStore("save.json")
        # Load all the exercises
        for item in store.find(name="Exercice"):
            self.add_new_widget((item[1]).get("text"), mode="load")
            self.countExercisess += 1

        self.countExercisessScreen = 0
        store = JsonStore("exercises.json")
        # Load all the exercises
        for item in store.find(name="Exercice"):
            self.countExercisessScreen += 1

        # On start hide the edit section
        partial(
            self.hide_me,
            [self.root.ids.exercise_name_input, self.root.ids.addExercise_button],
        )()

        for widget in self.activeExerciseList[0]:
            widget.children[0].on_release = partial(
                partial(
                    self.screen_change,
                    "ExerciseScreen",
                    widget.children[1].text,
                    "right",
                ),
                partial(self.load_exercises_screen, widget.children[1].text),
            )

        self.sort_exercises("AZ_asc")

    def visibility_handler(self, widgets, *args):
        if self.flagIsHidenEdit_uix:
            self.hide_me(widgets)
        else:
            self.show_me(widgets)

        self.flagIsHidenEdit_uix = not self.flagIsHidenEdit_uix

    def hide_me(self, widgets, *args):
        if type(widgets) != list:
            widgets = [widgets]
        for widget in widgets:
            widget.opacity = 0
            widget.disabled = True

    def show_me(self, widgets, *args):
        if type(widgets) != list:
            widgets = [widgets]
        for widget in widgets:
            widget.opacity = 1
            widget.disabled = False

    def sort_exercises(self, mode, *args):

        self.activeExerciseList[1] = list()
        for exercise in self.activeExerciseList[0]:
            self.activeExerciseList[1].append(exercise.children[1].text.lower())

        tupleResult = list(zip(self.activeExerciseList[0], self.activeExerciseList[1]))

        if mode == "AZ_asc":
            activeExerciseSortTempList = sorted(tupleResult, key=lambda x: x[1])
        elif mode == "AZ_des":
            activeExerciseSortTempList = sorted(
                tupleResult, key=lambda x: x[1], reverse=True
            )

        self.activeExerciseList = list(zip(*activeExerciseSortTempList))
        self.activeExerciseList[0] = list(self.activeExerciseList[0])
        self.reload_exercises()

    def reload_exercises(self, *args):
        self.root.ids.exercise_box.clear_widgets()
        for exercise in self.activeExerciseList[0]:
            self.root.ids.exercise_box.add_widget(exercise)

    def add_new_widget(self, text, mode="add", *args):

        if text == "":
            return

        store = JsonStore("save.json")
        vp_height = self.root.ids.exercise_scroll.viewport_size[1]
        sv_height = self.root.ids.exercise_scroll.height

        # add a new widget (must have preset height)
        boxlayout = MDBoxLayout(
            orientation="horizontal", size_hint=(1, None), height=50
        )
        boxlayout.add_widget(
            MDLabel(
                text=text,
                size_hint=(1, None),
                height=50,
                valign="center",
                halign="center",
            )
        )
        removeAndInfo_button = MDIconButton(
            icon="information-outline",
            theme_icon_color="Custom",
            icon_color=self.theme_cls.primary_color,
            size_hint=(0.25, None),
            height=50,
        )
        boxlayout.add_widget(removeAndInfo_button)

        if mode != "reload":
            self.activeExerciseList[0].append(boxlayout)

        self.root.ids.exercise_box.add_widget(boxlayout)

        if mode != "load" and mode != "reload":
            store.put(name="Exercice", text=text, key=self.countExercisess)
            self.countExercisess += 1

        # On adding new element, show remove button
        if mode != "load":
            for widget in self.activeExerciseList[0]:
                widget.children[0].icon = "delete"
                widget.children[0].on_release = partial(self.remove_widget, widget)

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

    def remove_widget(self, widgetsToRemove, *args):

        store = JsonStore("save.json")
        if type(widgetsToRemove) != list:
            widgetsToRemove = [widgetsToRemove]

        for widgetToRemove in widgetsToRemove:
            try:
                self.root.ids.exercise_box.remove_widget(widgetToRemove)
                self.countExercisess -= 1
                store.delete(str(self.countExercisess))
                self.activeExerciseList[0].remove(widgetToRemove)
                self.activeExerciseList[1].remove(widgetToRemove.children[1].text)
            except:
                pass

        return super().on_start()

    def edit_button_handler(self, *args):
        # On start hide the edit section
        if self.flagEdit_button:

            for widget in self.activeExerciseList[0]:
                # Change to delete button
                widget.children[0].icon = "delete"
                widget.children[0].on_release = partial(self.remove_widget, widget)

            self.root.ids.edit_button.icon = "check-circle-outline"

        else:

            for widget in self.activeExerciseList[0]:
                # Change to delete button
                widget.children[0].icon = "information-outline"
                widget.children[0].on_release = partial(
                    partial(
                        self.screen_change,
                        "ExerciseScreen",
                        widget.children[1].text,
                        "right",
                    ),
                    partial(self.load_exercises_screen, widget.children[1].text),
                )

            self.root.ids.edit_button.icon = "circle-edit-outline"

        self.flagEdit_button = not self.flagEdit_button

        return super().on_start()

    def screen_change(
        self,
        current,
        infoTitle="",
        direction="left",
        reset=False,
        returnBtn=True,
        *args
    ):
        if reset:
            self.root.ids.exercise_screen_box.clear_widgets()

        store = JsonStore("exercises.json")
        for item in store.find(name="Exercice"):
            if item[1].get("title") == infoTitle:
                self.add_new_widget_exercise_screen(
                    infoTitle,
                    (item[1]).get("reps"),
                    (item[1]).get("sets"),
                    (item[1]).get("dirty"),
                    (item[1]).get("date"),
                    "load",
                )

        self.root.transition = SlideTransition(direction=direction, duration=0.25)
        self.root.current = current
        self.root.ids.exercise_screen_top_app_bar_title.title = infoTitle
        # if(returnBtn):
        # self.add_new_widget_exercise_screen(infoTitle)

    def add_new_widget_exercise_screen(
        self, title, reps, sets, dirty, date="" , mode="add", *args
    ):
        if(reps == "" or sets == "" or dirty == ""):
            return
        
        store = JsonStore("exercises.json")
        vp_height = self.root.ids.exercise_screen_scroll.viewport_size[1]
        sv_height = self.root.ids.exercise_screen_scroll.height

        gridlayout = MDGridLayout(
            cols=4, rows=1, size_hint=(1, None), height=50, _md_bg_color="#2f2f2f"
        )
        if(mode == "add"):
            gridlayout.add_widget(
                MDLabel(
                    text=str(self.date),
                    size_hint=(1, None),
                    height=50,
                    valign="center",
                    halign="center",
                )
            )
        else:
            gridlayout.add_widget(
                MDLabel(
                    text=str(date),
                    size_hint=(1, None),
                    height=50,
                    valign="center",
                    halign="center",
                )
            )
        gridlayout.add_widget(
            MDLabel(
                text="Reps: " + str(reps),
                size_hint=(1, None),
                height=50,
                valign="center",
                halign="center",
            )
        )
        gridlayout.add_widget(
            MDLabel(
                text="Sets: " + str(sets),
                size_hint=(1, None),
                height=50,
                valign="center",
                halign="center",
            )
        )
        if dirty:
            gridlayout.add_widget(
                MDLabel(
                    text="Dirty",
                    size_hint=(1, None),
                    height=50,
                    valign="center",
                    halign="center",
                )
            )
        else:
            gridlayout.add_widget(
                MDLabel(
                    text="Clean",
                    size_hint=(1, None),
                    height=50,
                    valign="center",
                    halign="center",
                )
            )

        if mode != "reload":
            # self.activeExerciseScreenList[0].append(boxLayaout)
            self.activeExerciseScreenList.append(gridlayout)

        self.root.ids.exercise_screen_box.add_widget(gridlayout)

        if mode != "load" and mode != "reload":
            store.put(
                name="Exercice",
                reps=reps,
                sets=sets,
                dirty=dirty,
                title=title,
                date = self.date,
                key=self.countExercisessScreen,
            )
            self.countExercisessScreen += 1

        if vp_height > sv_height:
            scroll = self.root.ids.exercise_screen_scroll.scroll_y
            bottom = scroll * (vp_height - sv_height)

            Clock.schedule_once(partial(self.adjust_scroll_screen, bottom), -1)

    def adjust_scroll_screen(self, bottom, *args):
        vp_height = self.root.ids.exercise_screen_scroll.viewport_size[1]
        sv_height = self.root.ids.exercise_screen_scroll.height
        self.root.ids.exercise_screen_scroll.scroll_y = bottom / (vp_height - sv_height)

    def load_exercises_screen(self, *args):
        store = JsonStore("exercises.json")
        # Load all the exercises
        for item in store.find(name="Exercice"):
            self.add_new_widget_exercise_screen((item[1]).get("text"), mode="load")
            self.countExercisessScreen += 1

    def edit_button_handler_exercise_screen(self, *args):
        # On start hide the edit section
        if self.flagEdit_button:

            for widget in self.activeExerciseList[0]:
                # Change to delete button
                widget.children[0].icon = "delete"
                widget.children[0].on_release = partial(self.remove_widget, widget)

            self.root.ids.edit_button.icon = "check-circle-outline"

        else:

            for widget in self.activeExerciseList[0]:
                # Change to delete button
                widget.children[0].icon = "information-outline"
                widget.children[0].on_release = partial(
                    partial(
                        self.screen_change,
                        "ExerciseScreen",
                        widget.children[1].text,
                        "right",
                    ),
                    partial(self.load_exercises_screen, widget.children[1].text),
                )

            self.root.ids.edit_button.icon = "circle-edit-outline"

        self.flagEdit_button = not self.flagEdit_button

    def on_save(self, instance, value, date_range):
            '''
            Events called when the "OK" dialog box button is clicked.

            :type instance: <kivymd.uix.picker.MDDatePicker object>;

            :param value: selected date;
            :type value: <class 'datetime.date'>;

            :param date_range: list of 'datetime.date' objects in the selected range;
            :type date_range: <class 'list'>;
            '''
            print(instance, value, date_range)
            self.date = str(value)
    
    def on_cancel(self, instance, value):
        '''Events called when the "CANCEL" dialog box button is clicked.'''

    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()


if __name__ == "__main__":
    DemoGPBApp().run()
