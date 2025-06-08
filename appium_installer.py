import os
import shutil
import subprocess

def install_appium():
    npm_path = shutil.which("npm")
    if not npm_path:
        print("❌ NPM not found in PATH. Please install Node.js first.")
        raise FileNotFoundError("NPM not found in PATH.")

    print(f"✅ NPM found at: {npm_path}")

    try:
        subprocess.check_call([npm_path, "install", "-g", "appium"])
        print("✅ Appium installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install Appium: {e}")
        raise e


def install_flutter_driver():
    try:
        appium_path = shutil.which("appium")
        if appium_path is None:
            raise FileNotFoundError("Appium not found in PATH after install.")

        print(f"\nFound Appium at: {appium_path}")
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

        print("✅ appium-flutter-driver installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Subprocess error:\n{e.stderr}")
        raise e
    except FileNotFoundError as e:
        print(f"❌ FileNotFoundError: {e}")
        raise e


def patch_env_path():
    """
    Patch the PATH so Appium installed by npm is recognized immediately.
    """
    try:
        if os.name == "nt":
            npm_global_bin = os.path.expandvars(r"%APPDATA%\npm")
        else:
            npm_path = shutil.which("npm")
            if npm_path:
                npm_global_bin = subprocess.check_output([npm_path, "bin", "-g"], text=True).strip()
            else:
                print("⚠️ Cannot determine npm global bin path.")
                return

        if npm_global_bin and npm_global_bin not in os.environ["PATH"]:
            os.environ["PATH"] += os.pathsep + npm_global_bin
            print(f"✅ PATH updated with: {npm_global_bin}")
    except Exception as e:
        print(f"⚠️ Failed to patch PATH: {e}")