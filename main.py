from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.properties import StringProperty

# Головний екран
class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        greeting_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=('30sp'), spacing=10)
        
        self.greeting_label = Label(text="Введіть ваше ім'я:", size_hint=(0.3, 1))
        greeting_layout.add_widget(self.greeting_label)
        
        self.name_input = TextInput(size_hint=(0.4, 1))
        greeting_layout.add_widget(self.name_input)
        
        greet_button = Button(text="Привітати", size_hint=(0.3, 1))
        greet_button.bind(on_release=self.show_greeting)
        greeting_layout.add_widget(greet_button)
        
        layout.add_widget(greeting_layout)
        
        main_label = Label(text="Головний екран", size_hint=(1, 0.5))
        layout.add_widget(main_label)
        
        btn = Button(text="Перейти до вибору екрана", size_hint=(0.6, 0.2), pos_hint={'center_x': 0.5})
        btn.bind(on_release=self.switch_to_choose_screen)
        layout.add_widget(btn)
        
        self.add_widget(layout)

    def show_greeting(self, instance):
        name = self.name_input.text.strip()
        if name:
            self.greeting_label.text = f"Привіт, {name}!"
        else:
            self.greeting_label.text = "Будь ласка, введіть ім'я."

    def switch_to_choose_screen(self, instance):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = "choose_screen"

# Екран вибору
class ChooseScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        label = Label(text="Виберіть екран для переходу", size_hint=(1, 0.8))
        layout.add_widget(label)
        
        btn_main = Button(text="Повернутися на головний екран", size_hint=(0.6, 0.2), pos_hint={'center_x': 0.5})
        btn_main.bind(on_release=self.switch_to_main_screen)
        layout.add_widget(btn_main)
        
        btn_quiz = Button(text="Перейти на екран вікторини", size_hint=(0.6, 0.2), pos_hint={'center_x': 0.5})
        btn_quiz.bind(on_release=self.switch_to_quiz_screen)
        layout.add_widget(btn_quiz)
        
        self.add_widget(layout)

    def switch_to_main_screen(self, instance):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "main"

    def switch_to_quiz_screen(self, instance):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = "quiz"

# Екран вікторини
class QuizScreen(Screen):
    question_text = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.questions = [
            {"question": "Що таке Python?", "answers": ["Мова програмування", "Рептилія", "Інструмент для дизайну"], "correct": 0},
            {"question": "Яка остання версія Python?", "answers": ["2.7", "3.10", "3.9"], "correct": 1},
            {"question": "Який оператор використовується для піднесення до степеня?", "answers": ["^", "**", "%%"], "correct": 1}
        ]
        self.current_question = 0
        self.score = 0  # Лічильник правильних відповідей
        
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.question_label = Label(size_hint=(1, 0.2))
        self.layout.add_widget(self.question_label)
        
        self.answer_buttons = []
        for i in range(3):
            btn = ToggleButton(group="answers", size_hint=(0.6, 0.2), pos_hint={'center_x': 0.5})
            btn.bind(on_release=self.check_answer)
            self.answer_buttons.append(btn)
            self.layout.add_widget(btn)
        
        self.next_button = Button(text="Наступне запитання", size_hint=(0.6, 0.2), pos_hint={'center_x': 0.5})
        self.next_button.bind(on_release=self.next_question)
        self.layout.add_widget(self.next_button)
        
        self.add_widget(self.layout)
        self.show_question()

    def show_question(self):
        for btn in self.answer_buttons:
            btn.background_color = (1, 1, 1, 1)
            btn.state = 'normal'
        question_data = self.questions[self.current_question]
        self.question_label.text = question_data["question"]
        for i, answer in enumerate(question_data["answers"]):
            self.answer_buttons[i].text = answer

    def check_answer(self, instance):
        selected_answer = self.answer_buttons.index(instance)
        if selected_answer == self.questions[self.current_question]["correct"]:
            instance.background_color = (0, 1, 0, 1)
            self.score += 1
        else:
            instance.background_color = (1, 0, 0, 1)

    def next_question(self, instance):
        if self.current_question < len(self.questions) - 1:
            self.current_question += 1
            self.show_question()
        else:
            self.show_final_score()

    def show_final_score(self):
        self.question_label.text = f"Вікторина завершена! Ваш рахунок: {self.score} із {len(self.questions)}"
        for btn in self.answer_buttons:
            btn.disabled = True
        self.next_button.disabled = True

# Основний клас додатку
class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name="main"))
        sm.add_widget(ChooseScreen(name="choose_screen"))
        sm.add_widget(QuizScreen(name="quiz"))
        return sm

MyApp().run()
