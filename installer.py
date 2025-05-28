import subprocess
import shutil
import os
import sys
import zipfile
import tkinter as tk
from tkinter import messagebox, ttk
import time
import ctypes
import winshell
from java_jdk_installer import install_java
from android_sdk_installer import install_android_sdk
from node_installer import install_nodejs
from python_installer import install_python
from adb_installer import add_adb_to_path
from build_tools_installer import install_android_components
from appium_installer import install_appium, install_flutter_driver

# Helper Functions
def get_resource_path(relative_path):
    """Get the absolute path to resource, works for dev and for PyInstaller bundle"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def run_as_admin():
    if not ctypes.windll.shell32.IsUserAnAdmin():
        # Relaunch as admin with a special flag
        params = " ".join(f'"{arg}"' for arg in sys.argv)
        if "--elevated" not in params:
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, f"{params} --elevated", None, 1)
            sys.exit()

run_as_admin()


INSTALL_DIR = r"C:\Program Files\AutoMata-Test"
ZIP_FILE = "AutoMata-Test Tools.zip"  # We will bundle this ZIP file in the EXE

# Helper Functions
def check_command(command):
    try:
        subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        return True
    except Exception:
        return False

def install_python_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def install_npm_package(package):
    subprocess.check_call(["npm", "install", "-g", package])

def extract_zip(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

def create_shortcut(target, shortcut_path, description):
    from win32com.client import Dispatch
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortcut(shortcut_path)
    shortcut.Targetpath = target
    shortcut.WorkingDirectory = os.path.dirname(target)
    shortcut.Description = description
    shortcut.save()

def elevate():
    if not ctypes.windll.shell32.IsUserAnAdmin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        sys.exit()

# GUI Progress Window
class InstallerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Automata Test Installer")
        self.root.geometry("500x150")
        self.progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(pady=30)
        self.label = tk.Label(root, text="Preparing installation...", font=("Arial", 12))
        self.label.pack()

        self.root.after(100, self.install_steps)

    def install_steps(self):
        steps = [
            ("Checking Python...", self.check_python),
            ("Checking Node.js...", self.check_node),
            ("Checking Java...", self.check_java),
            ("Checking Android SDK...", self.check_adb),
            ("Installing Appium...", self.check_appium_flutter_driver),
            # ("Installing Appium...", self.install_appium),
            # ("Installing Appium Flutter Driver...", self.install_flutter_driver),
            ("Installing Appium-Python-Client...", self.install_python_client),
            ("Extracting files...", self.extract_files),
            ("Creating Desktop Shortcut...", self.create_shortcut),
        ]

        total_steps = len(steps)

        for i, (text, func) in enumerate(steps, 1):
            self.label.config(text=text)
            self.root.update_idletasks()
            func()
            self.progress["value"] = (i / total_steps) * 100
            time.sleep(0.5)

        self.label.config(text="Installation Completed!")
        messagebox.showinfo("Success", "Setup Completed Successfully!")
        self.root.quit()

    def check_python(self):
        if not shutil.which("python"):
            answer = messagebox.askyesno("Python Not Found", "Python is not installed. Do you want to install it automatically?")
            if answer:
                try:
                    install_python()
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to install Python.\n\n{e}")
                    sys.exit()
            else:
                sys.exit()

    def check_node(self):
        if not shutil.which("node"):
            answer = messagebox.askyesno("Node.js Not Found", "Node.js is not installed. Do you want to install it automatically?")
            if answer:
                try:
                    install_nodejs()
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to install Node.js.\n\n{e}")
                    sys.exit()
            else:
                sys.exit()


    def check_java(self):
        if not shutil.which("java"):
            answer = messagebox.askyesno("java jdk Not Found", "java jdk is not installed. Do you want to install it automatically?")
            if answer:
                try:
                    install_java()
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to install java jdk.\n\n{e}")
                    sys.exit()
            else:
                sys.exit()

    def check_android_sdk():
        if not shutil.which("adb"):
            answer = messagebox.askyesno("Android SDK Not Found", "Android SDK (adb) is not installed or not in PATH. Do you want to install it automatically?")
            if answer:
                try:
                    install_android_sdk()
                    install_android_components()
                    add_adb_to_path()
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to install Android SDK.\n\n{e}")
                    sys.exit(1)
            else:
                sys.exit()

    def check_adb(self):
        if not shutil.which("adb"):
            messagebox.showerror("Error", "ADB tools not found! Install Android SDK manually first.")
            sys.exit()

    def check_appium_flutter_driver(self):
        if not shutil.which("appium"):
            answer = messagebox.askyesno(
                "Appium Not Found",
                "Appium is not installed or not in PATH. Do you want to install it automatically?"
            )
            if answer:
                try:
                    install_appium()
                    install_flutter_driver()
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to install Appium or Flutter driver.\n\n{e}")
                    sys.exit(1)
            else:
                sys.exit(1)

        try:
            appium_path = shutil.which("appium")
            result = subprocess.run(
                [appium_path, "plugin", "list", "--installed"],
                capture_output=True,
                text=True,
                check=True  # raises CalledProcessError if returncode != 0
            )
            output = result.stdout.lower().strip() if result.stdout else ""

            if "flutter" not in output:
                answer = messagebox.askyesno(
                    "Flutter Driver Not Found",
                    "appium-flutter-driver is not installed. Do you want to install it automatically?"
                )
                if answer:
                    try:
                        install_flutter_driver()
                    except Exception as e:
                        messagebox.showerror("Error", f"Failed to install Flutter driver.\n\n{e}")
                        sys.exit(1)
                else:
                    sys.exit(1)
            else:
                print("✅ appium-flutter-driver is installed.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to run Appium plugin list command.\n\n{e}")
            sys.exit(1)
        except FileNotFoundError:
            messagebox.showerror("Error", "Appium executable not found. Please install Appium and ensure it's in your PATH.")
            sys.exit(1)
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error while checking Appium plugins.\n\n{e}")
            sys.exit(1)


    # def install_appium(self):
    #     if not shutil.which("appium"):
    #         subprocess.check_call(["npm", "install", "-g", "appium"])

    # def install_flutter_driver(self):
    #     try:
    #         appium_path = shutil.which("appium")
    #         if appium_path is None:
    #             raise FileNotFoundError("Appium not found in PATH. Make sure it's installed via 'npm install -g appium' and PATH is set correctly.")

    #         print(f"\nFound appium at: {appium_path}")
            
    #         result = subprocess.run(
    #             [appium_path, "driver", "install", "--source=npm", "appium-flutter-driver"],
    #             capture_output=True,
    #             text=True
    #         )

    #         if result.returncode != 0:
    #             if "already installed" in result.stderr.lower():
    #                 print("Appium Flutter Driver is already installed. Skipping installation.")
    #                 return
    #             else:
    #                 raise subprocess.CalledProcessError(result.returncode, result.args, output=result.stdout, stderr=result.stderr)

    #     except subprocess.CalledProcessError as e:
    #         print(f"Subprocess error:\n{e.stderr}")
    #         messagebox.showerror("Error", f"Failed to install Appium Flutter Driver.\n\n{e.stderr}")
    #         sys.exit()
    #     except FileNotFoundError as e:
    #         print(f"FileNotFoundError: {e}")
    #         messagebox.showerror("Error", str(e))
    #         sys.exit()

    def install_python_client(self):
        install_python_package("Appium-Python-Client")

    def extract_files(self):
        if not os.path.exists(INSTALL_DIR):
            os.makedirs(INSTALL_DIR)
        
        # Path to the ZIP file inside the EXE (bundled by PyInstaller)
        zip_path = get_resource_path(ZIP_FILE)

        # Extract the ZIP file to the installation directory
        extract_zip(zip_path, INSTALL_DIR)

    def create_shortcut(self):
        try:
            from win32com.client import Dispatch
            desktop = winshell.desktop()
            path = os.path.join(desktop, "AutoMata-Test.lnk")
            target = INSTALL_DIR
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortcut(path)
            shortcut.Targetpath = target
            shortcut.WorkingDirectory = INSTALL_DIR
            shortcut.Description = "AutoMata-Test Tools"
            shortcut.IconLocation = r"%SystemRoot%\system32\SHELL32.dll,3"
            shortcut.save()
        except Exception as e:
            print(f"Shortcut creation failed: {e}")

if __name__ == "__main__":
    if "--elevated" not in sys.argv:
        run_as_admin()
    else:
        root = tk.Tk()
        app = InstallerGUI(root)
        root.mainloop()

