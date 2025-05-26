import os
import sys
import urllib.request
import zipfile
import shutil
import winreg

sdk_root = "C:\\Android\\sdk"
ZIP_FILE = "commandlinetools.zip"  # We will bundle this ZIP file in the EXE
def install_android_sdk():
    tools_path = os.path.join(sdk_root, "cmdline-tools", "latest")

    print("Extracting SDK tools...")
    extract_files()
    extract_temp = os.path.join(sdk_root, "cmdline-tools", "temp")

    os.makedirs(tools_path, exist_ok=True)
    for item in os.listdir(os.path.join(extract_temp, "cmdline-tools")):
        shutil.move(
            os.path.join(extract_temp, "cmdline-tools", item),
            os.path.join(tools_path, item)
        )
    shutil.rmtree(extract_temp)

    platform_tools = os.path.join(sdk_root, "platform-tools")
    platform_tools = os.path.join(sdk_root, "platform-tools")
    os.makedirs(platform_tools, exist_ok=True)

    # Add platform-tools to user's PATH if not already there
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment", 0, winreg.KEY_SET_VALUE | winreg.KEY_QUERY_VALUE) as key:
            try:
                current_path, _ = winreg.QueryValueEx(key, "Path")
            except FileNotFoundError:
                current_path = ""

            if platform_tools not in current_path:
                new_path = current_path + os.pathsep + platform_tools
                winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_path)
                print("✅ platform-tools added to user PATH.")
            else:
                print("ℹ️ platform-tools already in user PATH.")
    except Exception as e:
        print(f"⚠️ Failed to update PATH: {e}")
        return e

    print("Android SDK tools installed.")

def extract_files():
    if not os.path.exists(sdk_root):
        os.makedirs(sdk_root)
    zip_path = get_resource_path(ZIP_FILE)
    extract_zip(zip_path, sdk_root)

def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def extract_zip(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
