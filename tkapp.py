import tkinter as tk
from tkinter import ttk, messagebox
import json
import subprocess
import shlex
import argparse
import signal
import os
import webbrowser


class LauncherApp(tk.Tk):
    def __init__(self, config_file):
        super().__init__()
        self.config_file = config_file
        self.config_data = self.load_config()
        # Set window title from the JSON config, default to "TkApp"
        self.title(self.config_data.get("title", "TkApp"))
        # Load the icon from the file "icon.png" (or a path specified in the config)
        icon_path = self.config_data.get("icon", "icon.png")
        if os.path.exists(icon_path):
            try:
                icon_image = tk.PhotoImage(file=icon_path)
                self.iconphoto(True, icon_image)
            except Exception as e:
                print(f"Error loading icon: {e}")
        else:
            print(f"Icon file '{icon_path}' not found.")
        # Get categories from config; if not available, assume empty dict
        self.apps_by_category = self.config_data.get("categories", {})
        self.build_ui()

    def load_config(self):
        """
        Load the application configuration from a JSON file.
        The JSON file should be organized with keys "title", "about", "icon", "terminal", and "categories".
        The "about" text will be displayed in the mandatory About tab.
        The "terminal" key indicates the terminal emulator command to use for bash-type apps.
        """
        try:
            with open(self.config_file, "r") as f:
                config = json.load(f)
            return config
        except Exception as e:
            messagebox.showerror(
                "Configuration Error",
                f"Failed to load configuration file '{self.config_file}': {e}",
            )
            return {}

    def build_ui(self):
        """
        Build the UI using a Notebook widget to display each category as a separate tab.
        For each enabled application, create a button that launches the app.
        Always add an About tab that displays the about text from the configuration,
        along with a mandatory footer containing the GitHub link.
        """
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Create tabs for each category
        for category, apps in self.apps_by_category.items():
            frame = ttk.Frame(notebook)
            notebook.add(frame, text=category)
            row = 0
            for app in apps:
                if app.get("enabled", True):
                    btn_text = app.get("name", "Unnamed App")
                    btn = ttk.Button(
                        frame,
                        text=btn_text,
                        command=lambda app=app: self.launch_app(app),
                    )
                    btn.grid(row=row, column=0, padx=10, pady=5, sticky="ew")
                    row += 1

        # Always add an About tab
        about_frame = ttk.Frame(notebook)
        notebook.add(about_frame, text="About")
        about_text = self.config_data.get(
            "about",
            "TkApp Launcher\n\nA simple application launcher built with Tkinter.",
        )
        about_label = ttk.Label(
            about_frame, text=about_text, wraplength=400, justify="center"
        )
        about_label.pack(padx=10, pady=10, expand=True)
        footer_text = "Built with https://github.com/devfilipe/tkapp"
        footer_label = ttk.Label(
            about_frame,
            text=footer_text,
            foreground="blue",
            cursor="hand2",
            font=("Helvetica", 8),
        )
        footer_label.pack(side="bottom", pady=(0, 10))
        footer_label.bind(
            "<Button-1>", lambda e: self.open_link("https://github.com/devfilipe/tkapp")
        )

    def open_link(self, url):
        webbrowser.open(url)

    def launch_app(self, app):
        """
        Launch the selected application in a new process.
        The configuration should include:
          - 'path': the script or executable path.
          - 'args': (optional) command-line arguments.
          - 'type': either "python" (default) or "bash".
        For type "python", the launcher prepends "python" to the command.
        For type "bash", the launcher executes the command in a terminal emulator.
        The terminal emulator to use is defined in the config under "terminal" (default "x-terminal-emulator").
        """
        app_type = app.get("type", "python")
        path = app.get("path")
        args = app.get("args", "")
        if not path:
            messagebox.showerror("Error", "Application path not specified!")
            return

        if app_type == "python":
            command = ["python", path]
            if args:
                command.extend(shlex.split(args))
            try:
                subprocess.Popen(command)
            except Exception as e:
                messagebox.showerror(
                    "Error", f"Failed to launch Python application:\n{e}"
                )
        elif app_type == "bash":
            command_str = path + " " + args
            # Get the terminal emulator from the config; default to "x-terminal-emulator"
            terminal_emulator = self.config_data.get("terminal", "x-terminal-emulator")
            # Use '--' to terminate terminal options and then pass the command.
            terminal_command = [
                terminal_emulator,
                "--",
                "bash",
                "-c",
                f"{command_str}; exec bash",
            ]
            try:
                subprocess.Popen(terminal_command)
            except Exception as e:
                messagebox.showerror(
                    "Error", f"Failed to launch bash application:\n{e}"
                )
        else:
            messagebox.showerror("Error", f"Unknown application type: {app_type}")


def main():
    parser = argparse.ArgumentParser(description="Tkinter Launcher Application")
    parser.add_argument(
        "--config",
        "-c",
        type=str,
        default="tkapp.conf",
        help="Path to the JSON configuration file",
    )
    args = parser.parse_args()

    app = LauncherApp(config_file=args.config)
    signal.signal(signal.SIGINT, lambda signum, frame: app.destroy())
    app.mainloop()


if __name__ == "__main__":
    main()
