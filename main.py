import threading
from flask import Flask
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget

# Import your Flask app
from app import app as flask_app  

# Function to run Flask in background thread
def run_flask():
    flask_app.run(host="127.0.0.1", port=5000)

class FlaskWrapper(App):
    def build(self):
        layout = BoxLayout(orientation="vertical")
        layout.add_widget(Label(text="Flask is running at http://127.0.0.1:5000"))
        layout.add_widget(Label(text="Open it in your browser!"))
        return layout

if __name__ == "__main__":
    # Run Flask server in background
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    # Run Kivy app
    FlaskWrapper().run()