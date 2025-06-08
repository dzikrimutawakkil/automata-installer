import os
import sys
import zipfile
import shutil
import winreg

def install_java():
    zip_name = "java-17.zip"
    install_dir = "C:\\Program Files\\Java"
    jdk_folder = os.path.join(install_dir, "jdk17.0.15_6")

    print("Extracting Java JDK...")
    zip_path = get_resource_path(zip_name)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(install_dir)

    java_bin_path = os.path.join(jdk_folder, "bin")
    java_exe = os.path.join(java_bin_path, "java.exe")

    if os.path.exists(java_exe):
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_SET_VALUE | winreg.KEY_QUERY_VALUE) as key:
                # Set JAVA_HOME
                winreg.SetValueEx(key, "JAVA_HOME", 0, winreg.REG_EXPAND_SZ, jdk_folder)
                print("✅ JAVA_HOME environment variable set.")

                # Update PATH
                try:
                    current_path, _ = winreg.QueryValueEx(key, "Path")
                except FileNotFoundError:
                    current_path = ""

                if java_bin_path not in current_path:
                    new_path = current_path + os.pathsep + java_bin_path
                    winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_path)
                    print("✅ Java added to user PATH.")
                else:
                    print("ℹ️ Java already in PATH.")
        except Exception as e:
            print(f"⚠️ Failed to update environment variables: {e}")
            return e

        return
        # broadcast_environment_change()
    else:
        print("❌ Failed to locate java.exe after extraction.")
        return


# Utility for PyInstaller-safe file access
def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)
