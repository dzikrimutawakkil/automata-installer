import os
import winreg

def add_adb_to_path():
    adb_path = os.path.join("C:\\Android\\sdk", "platform-tools")
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment", 0, winreg.KEY_SET_VALUE | winreg.KEY_QUERY_VALUE) as key:
            try:
                current_path, _ = winreg.QueryValueEx(key, "Path")
            except FileNotFoundError:
                current_path = ""

            if adb_path not in current_path:
                new_path = current_path + os.pathsep + adb_path
                winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_path)
                print("✅ ADB path added to user PATH.")
            else:
                print("ℹ️ ADB path already in PATH.")
    except Exception as e:
        print(f"⚠️ Failed to update PATH: {e}")
