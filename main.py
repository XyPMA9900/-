from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
import json, os, random

SAVE_FILE = "save.json"

# ================== DATA ==================
data = {
    "balance": 0,
    "auto1": 0,
    "auto2": 0,
    "auto3": 0,
    "luck": 1.0,
    "rebirths": 0
}

def load():
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r") as f:
                data.update(json.load(f))
        except:
            pass

def save():
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)

# ================== MENU ==================
class Menu(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        box = BoxLayout(orientation="vertical", padding=30, spacing=15)

        self.cat = Label(
            text=" /\\_/\\\n( o.o )\n > ^ < ",
            font_size=28,
            size_hint=(1, 0.35)
        )

        box.add_widget(Label(text="КотоКликер", font_size=32))
        box.add_widget(self.cat)

        for name, target in [
            ("ИГРАТЬ", "game"),
            ("МАГАЗИН", "shop"),
            ("КАЗИНО", "casino"),
            ("ПЕРЕРОЖДЕНИЕ", "rebirth"),
            ("ВЫХОД", "exit")
        ]:
            btn = Button(text=name, size_hint=(1, 0.15))
            btn.bind(on_press=lambda x, t=target: self.go(t))
            box.add_widget(btn)

        self.add_widget(box)

    def go(self, target):
        if target == "exit":
            App.get_running_app().stop()
        else:
            self.manager.current = target

# ================== GAME ==================
class Game(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        box = BoxLayout(orientation="vertical", padding=25, spacing=15)

        self.lbl = Label(font_size=22)
        self.cat = Label(
            text=" /\\_/\\\n( o.o )\n > ^ < ",
            font_size=34,
            size_hint=(1, 0.45)
        )

        btn = Button(text="КЛИК", size_hint=(1, 0.2))
        back = Button(text="НАЗАД", size_hint=(1, 0.15))

        btn.bind(on_press=self.click)
        back.bind(on_press=lambda x: setattr(self.manager, "current", "menu"))

        box.add_widget(self.lbl)
        box.add_widget(self.cat)
        box.add_widget(btn)
        box.add_widget(back)

        self.add_widget(box)
        self.update()
        Clock.schedule_interval(self.auto, 1)

    def update(self):
        self.lbl.text = f"Баланс: {data['balance']}"

    def click(self, _):
        data["balance"] += 1
        save()
        self.update()

    def auto(self, dt):
        gain = (
            data["auto1"] * 1 +
            data["auto2"] * 5 +
            data["auto3"] * 20
        )
        if gain:
            data["balance"] += gain
            save()
            self.update()

# ================== SHOP ==================
class Shop(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.box = BoxLayout(orientation="vertical", padding=25, spacing=15)
        self.add_widget(self.box)
        self.update()

    def update(self):
        self.box.clear_widgets()
        self.box.add_widget(Label(text=f"Баланс: {data['balance']}", font_size=20))

        if data["rebirths"] == 0:
            self.add_card("Автокликер I", "+1/сек", 50, "auto1")

        self.add_card("Автокликер II", "+5/сек", 150, "auto2")

        if data["rebirths"] >= 1:
            self.add_card("Автокликер III", "+20/сек", 500, "auto3")

        back = Button(text="НАЗАД", size_hint=(1, 0.15))
        back.bind(on_press=lambda x: setattr(self.manager, "current", "menu"))
        self.box.add_widget(back)

    def add_card(self, name, desc, price, key):
        btn = Button(
            text=f"{name}\n{desc}\nЦена: {price}",
            size_hint=(1, 0.22)
        )
        btn.bind(on_press=lambda x: self.buy(price, key))
        self.box.add_widget(btn)

    def buy(self, price, key):
        if data["balance"] >= price:
            data["balance"] -= price
            data[key] += 1
            save()
            self.update()

# ================== CASINO ==================
class Casino(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.bet = 10

        box = BoxLayout(orientation="vertical", padding=25, spacing=10)

        self.lbl = Label(font_size=20)
        self.res = Label(font_size=18)

        bet_box = BoxLayout(size_hint=(1, 0.25))
        for b in [10, 100, 1000, 5000, 10000, 100000, 1000000]:
            btn = Button(text=str(b))
            btn.bind(on_press=lambda x, v=b: self.set_bet(v))
            bet_box.add_widget(btn)

        spin = Button(text="КРУТИТЬ", size_hint=(1, 0.2))
        back = Button(text="НАЗАД", size_hint=(1, 0.15))

        spin.bind(on_press=self.spin)
        back.bind(on_press=lambda x: setattr(self.manager, "current", "menu"))

        box.add_widget(self.lbl)
        box.add_widget(bet_box)
        box.add_widget(self.res)
        box.add_widget(spin)
        box.add_widget(back)

        self.add_widget(box)
        self.update()

    def set_bet(self, v):
        self.bet = v
        self.update()

    def update(self):
        self.lbl.text = f"Баланс: {data['balance']} | Ставка: {self.bet}"

    def spin(self, _):
        if data["balance"] < self.bet:
            self.res.text = "Мало денег"
            return

        data["balance"] -= self.bet
        chance = int(65 / data["luck"])
        if random.randint(1, 100) > chance:
            win = self.bet * 3
            data["balance"] += win
            self.res.text = f"+{win}"
        else:
            self.res.text = "Проигрыш"

        save()
        self.update()

# ================== REBIRTH ==================
class Rebirth(Screen):
    PRICE = 1488

    def __init__(self, **kw):
        super().__init__(**kw)
        box = BoxLayout(orientation="vertical", padding=30, spacing=20)

        self.lbl = Label(font_size=18)
        self.btn = Button(text="ПЕРЕРОДИТЬСЯ", size_hint=(1, 0.2))
        back = Button(text="НАЗАД", size_hint=(1, 0.15))

        self.btn.bind(on_press=self.do)
        back.bind(on_press=lambda x: setattr(self.manager, "current", "menu"))

        box.add_widget(self.lbl)
        box.add_widget(self.btn)
        box.add_widget(back)

        self.add_widget(box)
        self.update()

    def update(self):
        if data["rebirths"] == 0:
            self.lbl.text = (
                "Перерождение I\n\n"
                f"Цена: {self.PRICE}\n\n"
                "×2 деньги\n"
                "×1.2 удача\n"
                "Удаляет автокликер I\n"
                "Открывает автокликер III"
            )
            self.btn.disabled = data["balance"] < self.PRICE
        else:
            self.lbl.text = "Перерождение уже сделано"
            self.btn.disabled = True

    def do(self, _):
        if data["rebirths"] > 0 or data["balance"] < self.PRICE:
            return

        data["balance"] -= self.PRICE
        data["balance"] *= 2
        data["luck"] *= 1.2
        data["auto1"] = 0
        data["auto2"] = 0
        data["auto3"] = 0
        data["rebirths"] = 1
        save()
        self.manager.current = "menu"

# ================== APP ==================
class CatClickerApp(App):
    def build(self):
        load()
        sm = ScreenManager()
        sm.add_widget(Menu(name="menu"))
        sm.add_widget(Game(name="game"))
        sm.add_widget(Shop(name="shop"))
        sm.add_widget(Casino(name="casino"))
        sm.add_widget(Rebirth(name="rebirth"))
        return sm

if __name__ == "__main__":
    CatClickerApp().run()