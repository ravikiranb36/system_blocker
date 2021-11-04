import time
from tkinter import *
from pynput import mouse, keyboard
import keyboard as kb
from tkinter import messagebox
from threading import Thread

KEY = "1234"


class App(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.mouse_disable = True
        self.mouse_controller = mouse.Controller()
        self.block_keyboard()
        Thread(target=self.mouse_state).start()
        self.create_window()
        self.keyboard_listener = keyboard.Listener(
            on_press=self.on_key_press,
            on_release=self.on_key_release)
        self.keyboard_listener.start()
        # self.mouse_listener = mouse.Listener(
        #     on_move=self.on_mouse_move,
        #     on_click=self.on_mouse_click,
        #     on_scroll=self.on_mouse_scroll)
        # self.mouse_listener.start()
        self.attributes('-fullscreen', True)

    def on_mouse_move(self, x, y):
        print(x, y)
        self.mouse_controller.position = (0, 0)

    def on_mouse_click(self, x, y, button, pressed):
        pass

    def on_mouse_scroll(self, x, y, dx, dy):
        pass

    def mouse_state(self):
        while self.mouse_disable:
            self.mouse_controller.position = (0, 0)
            time.sleep(0.01)

    def create_window(self):
        # global background_image
        background_image = PhotoImage("427852.jpg")
        background_label = Label(self, image=background_image)
        background_label.image = background_image
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        # background_label.image=background_image
        Label(self, text="License Key").place(x=30, y=30)
        self.licence_key_in = Entry(self)
        self.licence_key_in.place(x=100, y=30)
        # self.bind("<KeyPress>", self.pressed_keys)

    @staticmethod
    def block_keyboard():
        for i in range(150):
            kb.block_key(i)

    @staticmethod
    def deblock_keyboard():
        for i in range(150):
            kb.unblock_key(i)

    def on_key_press(self, key):
        self.licence_key_in.focus_force()
        try:
            if kb.is_pressed("Win+d"):
                self.keyboard_listener.stop()
                # self.keyboard_listener.join()
                self.deblock_keyboard()
                kb.press_and_release("win+r")
                self.block_keyboard()
                self.keyboard_listener = keyboard.Listener(
                    on_press=self.on_key_press,
                    on_release=self.on_key_release)
                self.keyboard_listener.start()
                return
            key = key.char
            if key.isprintable():
                self.licence_key_in.insert(END, key)
        except AttributeError as e:
            if key == keyboard.Key.enter:
                if self.licence_key_in.get() == KEY:
                    self.mouse_disable = False
                    messagebox.showinfo("Success", "You have successfully verified")
                    self.deblock_keyboard()
                    self.destroy()
                else:
                    messagebox.showerror("Failure", "You have not entered valid license key")
            elif key == keyboard.Key.backspace:
                text = self.licence_key_in.get()
                self.licence_key_in.delete(len(text) - 1, END)
        except Exception as e:
            print(f"Error: {e}")

    @staticmethod
    def on_key_release(key):
        pass


if __name__ == "__main__":
    app = App()
    app.mainloop()
