import threading
import time
import os
from .server import HTTPServer

class Reloader:

    def __init__(self, app: HTTPServer, reload: bool = True):
        self.app = app
        self.reload = reload
        self.thread = None

    def __call__(self, *args, **kwargs):
        if self.reload:
            self.app.reload()
        return self.app(*args, **kwargs)
    
    def run_reloader_thread(self):
        self.thread = threading.Thread(target=self.reloader, daemon=True)
        self.thread.start()

    def reloader(self):
        """Watches for changes in Python files and restarts the server."""
        file_mod_times = {}
        while True:
            restart_needed = False
            for dirpath, _, filenames in os.walk('.'):
                for filename in filenames:
                    if filename.endswith('.py'):
                        filepath = os.path.join(dirpath, filename)
                        mod_time = os.path.getmtime(filepath)
                        if filepath not in file_mod_times:
                            file_mod_times[filepath] = mod_time
                        elif file_mod_times[filepath] != mod_time:
                            print(f"Detected change in {filepath}, restarting server...")
                            file_mod_times[filepath] = mod_time
                            restart_needed = True
            
            if restart_needed:
                self.restart_server()
            time.sleep(1)  # Check every second

    def restart_server(self):
        """Restarts the server."""
        print("We have detected changes in the files, restarting the server...")
        self.app.close()  # Assuming this cleanly shuts down the server
        self.app.serve_forever()  # Assuming this starts the server

    