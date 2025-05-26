import os
import shutil
import subprocess

def install_appium():
    if not shutil.which("appium"):
        subprocess.check_call(["npm", "install", "-g", "appium"])

def install_flutter_driver():
    try:
        appium_path = shutil.which("appium")
        if appium_path is None:
            raise FileNotFoundError("Appium not found in PATH. Make sure it's installed via 'npm install -g appium' and PATH is set correctly.")

        print(f"\nFound appium at: {appium_path}")
        
        result = subprocess.run(
            [appium_path, "driver", "install", "--source=npm", "appium-flutter-driver"],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            if "already installed" in result.stderr.lower():
                print("Appium Flutter Driver is already installed. Skipping installation.")
                return
            else:
                raise subprocess.CalledProcessError(result.returncode, result.args, output=result.stdout, stderr=result.stderr)

    except subprocess.CalledProcessError as e:
        print(f"Subprocess error:\n{e.stderr}")
        return e

    except FileNotFoundError as e:
        print(f"FileNotFoundError: {e}")
        return e