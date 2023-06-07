from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.core.window import Window
from kivy.uix.label import Label
from functools import partial

import os.path

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
from random import randint

from datetime import date

from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition

from kivy.app import App
from matplotlib.figure import Figure
from kivy.uix.boxlayout import BoxLayout
import numpy as np
import matplotlib.pyplot as plt
from kivy.uix.image import Image

from datetime import datetime


class DemoGPBApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        #Global variables
        self.activeExerciseList = [[], []]
        self.activeExerciseScreenList = []
        self.date = str(date.today())
        
        self.dateAndPower = {}

        #Flags
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

        return Builder.load_file('main.kv')

    def on_start(self, *args):
        
        self.load_settings("height")
        self.load_settings("weight")
        
        self.countExercisess = 0
        store = JsonStore("save.json")
        #Load all the exercises
        for item in store.find(name="Exercice"):
            self.add_new_widget((item[1]).get("text"), mode="load")
            self.countExercisess += 1

        if(self.countExercisess == 0):
            self.add_new_widget("Deafult", mode="add")
        self.countExercisessScreen = 0        
        store = JsonStore("exercises.json")
        #Load all the exercises
        for item in store.find(name="Exercice"):
            self.countExercisessScreen += 1


        #On start hide the edit section
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

        if text == "" or text in self.activeExerciseList[1]:
            return

        store = JsonStore("save.json")
        vp_height = self.root.ids.exercise_scroll.viewport_size[1]
        sv_height = self.root.ids.exercise_scroll.height

        #Add a new widget (must have preset height)
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

        self.activeExerciseList[0].append(boxlayout)


        self.root.ids.exercise_box.add_widget(boxlayout)

        if mode != "load":
            store.put(name="Exercice", text=text, key=self.countExercisess)
            self.countExercisess += 1

        #On adding new element, show remove button

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
                for item in store.find(text=widgetToRemove.children[1].text):
                    store.delete(item[0])
                self.activeExerciseList[0].remove(widgetToRemove)
                self.activeExerciseList[1].remove(widgetToRemove.children[1].text)
            except:
                pass


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


    def reset_input(self, input,*args):
        if type(input) == list:
            for i in input:
                i.text = ""
        else:
            input.text = ""

    def screen_change(
        self,
        current,
        infoTitle="",
        direction="left",
        reset=False,
        returnBtn=True,
        exercise_enclopedia=False,
        *args
    ):
        if exercise_enclopedia:
            self.root.transition = SlideTransition(direction=direction, duration=0.25)
            self.root.current = current
            return
        
        if reset:
            self.root.ids.exercise_screen_box.clear_widgets()
            self.root.ids.exercise_notes_input_exercise_screen.text = "notes"

        store = JsonStore("exercises.json")
        for item in store.find(name="Exercice"):
            if item[1].get("title") == infoTitle:
                self.add_new_widget_exercise_screen(
                    infoTitle,
                    (item[1]).get("reps"),
                    (item[1]).get("sets"),
                    (item[1]).get("weight"),
                    str((item[1]).get("id")),
                    (item[1]).get("date"),
                    "load",
                )

        self.root.transition = SlideTransition(direction=direction, duration=0.25)
        self.root.current = current
        self.root.ids.exercise_screen_top_app_bar_title.title = infoTitle
        # if(returnBtn):
        # self.add_new_widget_exercise_screen(infoTitle)
        self.load_notes(infoTitle)


    def add_new_widget_exercise_screen(
        self, title, reps, sets, weight,idOfEx, date="" , mode="add", *args
    ):
        #here
        if(reps == "" or sets == "" or weight == ""):
            return
        
        store = JsonStore("exercises.json")
        vp_height = self.root.ids.exercise_screen_scroll.viewport_size[1]
        sv_height = self.root.ids.exercise_screen_scroll.height

        gridlayout = MDGridLayout(
            cols=5, rows=1, size_hint=(1, None), height=50, _md_bg_color="#2f2f2f", id=idOfEx
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
                text="Weight: " + str(weight),
                size_hint=(1, None),
                height=50,
                valign="center",
                halign="center",
            ))
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
        gridlayout.add_widget(
            MDIconButton(
                icon="delete",
                pos_hint={"center_x": 0.5, "center_y": 0.5},
                on_release=partial(self.remove_exercise, gridlayout),
            )
        )

        # self.activeExerciseScreenList[0].append(boxLayaout)
        self.activeExerciseScreenList.append(gridlayout)

        self.root.ids.exercise_screen_box.add_widget(gridlayout)

        if mode != "load":
            store.put(
                name="Exercice",
                weight=weight,
                reps=reps,
                sets=sets,
                title=title,
                date = self.date,
                key=self.countExercisessScreen,
                id=randint(1000, 10000000),
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

    def remove_exercise(self, widgetsToRemove, *args):

            print("remove_exercise")
            store = JsonStore("exercises.json")
            if type(widgetsToRemove) != list:
                widgetsToRemove = [widgetsToRemove]

            for widgetToRemove in widgetsToRemove:
                try:
                    self.root.ids.exercise_screen_box.remove_widget(widgetToRemove)
                    self.countExercisessScreen -= 1
                    print(widgetToRemove.id)
                    for item in store.find(id=int(widgetToRemove.id)):
                        print(item)
                        store.delete(item[0])
                    self.activeExerciseList[0].remove(widgetToRemove)
                    self.activeExerciseList[1].remove(widgetToRemove.children[1].text)
                except:
                    pass

    def save_notes(self,notes,title, *args):
        if notes == "notes":
            return
        item = None
        store = JsonStore("notes.json")
        for item in store.find(title=title):
            item = item[0]
        if item != None:
            store.delete(item)
            
        if title !="":
            store.put(
                name="Notes",
                title=title,
                notes=notes,
                key=randint(1000, 10000000),
            )
    
    def load_notes(self,title, *args):
        store = JsonStore("notes.json")
        for item in store.find(title=title):
            itemNewText = (item[1]).get("notes")
            self.root.ids.exercise_notes_input_exercise_screen.text = itemNewText


    def progress_load_widgets(self, *args):
      
        self.root.ids.progress_box.clear_widgets()

        store = JsonStore("save.json")
        vp_height = self.root.ids.progress_scroll.viewport_size[1]
        sv_height = self.root.ids.progress_scroll.height

        rows = 1

        for item in store.find(name="Exercice"):
            title = item[1].get("text")
            gridlayout = MDGridLayout(
                size_hint=(1, None), height=50, cols=1, rows=2, spacing=5
            )

            print("Wygenerowano",title + ".png")
            self.root.ids.progress_box.rows = rows
            self.show_graph(title)
            image = Image(source=title+".png", size_hint=(1, None), height=300)
            if os.path.exists(title + ".png"):
                gridlayout.add_widget(
                    MDLabel(
                        text=title,
                        size_hint=(1, None),
                        height=50,
                        valign="center",
                        halign="center",
                    )
                )
                gridlayout.add_widget(image)
                self.root.ids.progress_box.add_widget(gridlayout)
                rows += 1

        rows += 1
        self.root.ids.progress_box.rows = rows
        self.root.ids.progress_box.add_widget(MDLabel(text=""))

        if vp_height > sv_height:  # otherwise there is no scrolling
            # calculate y value of bottom of scrollview in the viewport
            scroll = self.root.ids.progress_scroll.scroll_y
            bottom = scroll * (vp_height - sv_height)

            # use Clock.schedule_once because we need updated viewport height
            # this assumes that new widgets are added at the bottom
            # so the current bottom must increase by the widget height to maintain position
            Clock.schedule_once(partial(self.progress_adjust_scroll, bottom), -1)

    def progress_adjust_scroll(self, bottom, *args):
        vp_height = self.root.ids.progress_scroll.viewport_size[1]
        sv_height = self.root.ids.progress_scroll.height
        self.root.ids.progress_scroll.scroll_y = bottom / (vp_height - sv_height)




    def save_settings(self,title, value, *args):
        if value == "":
            return
        item = None
        store = JsonStore("settings.json")
        for item in store.find(title=title):
            item = item[0]
        if item != None:
            store.delete(item)
            
        if title !="":
            store.put(
                name="Settings",
                title=title,
                value=value,
                key=randint(1000, 10000000),
            )
    
    def load_settings(self,title, *args):
        store = JsonStore("settings.json")
        for item in store.find(title=title):
            val = (item[1]).get("value")
            if title == "height":
                self.root.ids.height_input.text = val
            if title == "weight":
                self.root.ids.weight_input.text = val

    def calculate_one_rep_max(self,weight,reps,ret=False, *args):
        if weight == "" or reps == "":
            return
        weight = float(weight)
        reps = int(reps)
        orm = weight/(1.0278-(0.0278*reps))
        if ret:
            return orm
        self.root.ids.result_calc_input.text = str(int(orm))

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

    def calculate_power(self,date,weight, reps, sets, *args):
        
        try:
            if int(sets) < 5:
                self.dateAndPower[date] += round(self.calculate_one_rep_max(weight, reps, True) * float((sets+"."+sets)),2)
            else:
                self.dateAndPower[date] += round(self.calculate_one_rep_max(weight, reps, True) * float((sets+"."+"5")),2)
        except:
            if int(sets) < 5:
                self.dateAndPower[date] = round(self.calculate_one_rep_max(weight, reps, True) * float((sets+"."+sets)),2)
            else:
                self.dateAndPower[date] = round(self.calculate_one_rep_max(weight, reps, True) * float((sets+"."+"5")),2)
        
    def sortDateStrArr(self, dates):
       return sorted(dates, key=lambda date: datetime.strptime(date, "%Y-%m-%d"))
    
    def show_graph(self, title, *args):
        
        store = JsonStore("exercises.json")
        
        for item in store.find(title=title):
            self.calculate_power(item[1].get("date"),item[1].get("weight"), item[1].get("reps"), item[1].get("sets"))
        
        firstDate = 0
        
        xArray = []
      
        #TODO https://stackoverflow.com/questions/3100985/plot-with-custom-text-for-x-axis-points

        #Posortować po czasie, i dać wartości do X, zaczynając od 0
        for r in self.sortDateStrArr(list(self.dateAndPower.keys())):
            if firstDate == 0:
                xArray.append(0)
                prevDate = datetime.fromisoformat(r).timestamp()
                firstDate = 1
                continue
            xArray.append(int((datetime.fromisoformat(r).timestamp() - prevDate)/100))

        yArray = []
        
        for i in self.sortDateStrArr(list(self.dateAndPower.keys())):
            yArray.append(self.dateAndPower[i])
        
        if len(xArray) == 0:
            return
        
        x = np.array(xArray)
        y = np.array(yArray)


        x_smooth = np.linspace(x.min(), x.max(), 200)
        y_smooth = np.interp(x_smooth, x, y)


        #calculation of simple regression coefficients
        slope, intercept = np.polyfit(x, y, 1)

        xPredGen = np.linspace(x.max(), x.max()+6000, 1500)

        # generowanie points of prediction
        x_pred = np.array(xPredGen)
        y_pred = slope * x_pred + intercept

        #drawing of a vicress
        plt.scatter(x, y, color='blue')
        plt.plot(x_pred, y_pred, color='blue', linestyle='dashed')
        plt.plot(x_smooth, y_smooth, color='blue')
        plt.title(title)
        plt.ylabel('Power')
        plt.xlabel('Date')
        
        my_xticks = self.sortDateStrArr(list(self.dateAndPower.keys()))
        plt.xticks(x, my_xticks,rotation=45)
        
        plt.subplots_adjust(bottom=0.20)
        
        plt.savefig(title+".png")
        plt.clf()
        self.dateAndPower = {}
    
    def test(self, text, *args):
        print(text)

if __name__ == "__main__":
    DemoGPBApp().run()
