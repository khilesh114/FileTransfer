from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
import threading
import http.server
import socketserver
import os

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        # Log messages to the log screen in the app
        log_message = "%s - - [%s] %s\n" % (self.client_address[0], self.log_date_time_string(), format % args)
        App.get_running_app().log_screen_widget.update_log(log_message)
        super().log_message(format, *args)

    def do_GET(self):
        # Handle GET requests
        super().do_GET()
        self.log_message("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))

    def do_POST(self):
        # Handle POST requests
        content_length = int(self.headers['Content-Length'])  # Get the size of data
        post_data = self.rfile.read(content_length)  # Get the data
        self.log_message("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                         str(self.path), str(self.headers), post_data.decode('utf-8'))
        super().do_POST()

class MainScreen(FloatLayout):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        field_width = 320  # Width of input fields in pixels
        field_height = 50  # Height of input fields in pixels

        # Input for IP Address
        self.ip_input = TextInput(
            hint_text='Enter IP Address',
            background_color=(0, 1, 0, 1),
            size_hint=(None, None),
            width=field_width,
            height=field_height,
            pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )
        # Input for Port
        self.port_input = TextInput(
            hint_text='Enter Port',
            input_filter='int',
            background_color=(1, 0, 1, 1),
            size_hint=(None, None),
            width=field_width,
            height=field_height,
            pos_hint={'center_x': 0.5, 'center_y': 0.6}
        )
        # Input for Directory to Serve
        self.directory_input = TextInput(
            text='/sdcard/',
            hint_text='Enter Directory to Serve',
            size_hint=(None, None),
            width=field_width,
            height=field_height,
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        # Button to start the server
        self.start_button = Button(
            text='Start HTTP Server',
            size_hint=(None, None),
            width=field_width,
            height=field_height,
            pos_hint={'center_x': 0.5, 'center_y': 0.4}
        )
        self.start_button.bind(on_press=self.start_server)

        # Adding all widgets to the screen
        self.add_widget(Label(
            text='IP Address',
            size_hint=(None, None),
            height=field_height,
            pos_hint={'center_x': 0.5, 'center_y': 0.75}
        ))
        self.add_widget(self.ip_input)
        self.add_widget(Label(
            text='Port',
            size_hint=(None, None),
            height=field_height,
            pos_hint={'center_x': 0.5, 'center_y': 0.65}
        ))
        self.add_widget(self.port_input)
        self.add_widget(Label(
            text='Directory:',
            size_hint=(None, None),
            height=field_height,
            pos_hint={'center_x': 0.5, 'center_y': 0.55}
        ))
        self.add_widget(self.directory_input)
        self.add_widget(self.start_button)

    def start_server(self, instance):
        host_ip = self.ip_input.text.strip()
        port = self.port_input.text.strip()
        directory = self.directory_input.text.strip()

        # Check if inputs are valid
        if not host_ip or not port or not directory:
            App.get_running_app().log_screen_widget.update_log("IP Address, Port, and Directory must be provided!")
            App.get_running_app().screen_manager.current = 'log'
            return

        # Verify the directory exists
        if not os.path.isdir(directory):
            App.get_running_app().log_screen_widget.update_log("The specified directory does not exist!")
            App.get_running_app().screen_manager.current = 'log'
            return

        # Start the HTTP server in a new thread
        threading.Thread(target=self.run_http_server, args=(host_ip, int(port), directory), daemon=True).start()
        App.get_running_app().screen_manager.current = 'log'

    def run_http_server(self, host_ip, port, directory):
        try:
            handler = CustomHTTPRequestHandler
            os.chdir(directory)  # Change the current working directory to the specified directory l
            with socketserver.TCPServer((host_ip, port), handler) as httpd:
                log_message = f"Serving {directory} at {host_ip}:{port}"
                App.get_running_app().log_screen_widget.update_log(log_message)
                httpd.serve_forever()
        except Exception as e:
            error_message = f"Error: {e}"
            App.get_running_app().log_screen_widget.update_log(error_message)

class LogScreen(FloatLayout):
    def __init__(self, **kwargs):
        super(LogScreen, self).__init__(**kwargs)
        self.log_label = Label(
            text='',
            valign='top',
            halign='left',
            size_hint=(1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.log_label.bind(size=self.update_text_width)
        self.add_widget(self.log_label)

    def update_log(self, message):
        self.log_label.text += message + '\n'

    def update_text_width(self, *args):
        self.log_label.text_size = (self.log_label.width, None)

class MyKivyApp(App):
    def build(self):
        self.screen_manager = ScreenManager()

        self.main_screen = Screen(name='main')
        self.main_screen.add_widget(MainScreen())
        self.screen_manager.add_widget(self.main_screen)

        self.log_screen = Screen(name='log')
        self.log_screen_widget = LogScreen()
        self.log_screen.add_widget(self.log_screen_widget)
        self.screen_manager.add_widget(self.log_screen)

        return self.screen_manager

if __name__ == "__main__":
    MyKivyApp().run()
