import os
import winreg

def add_adb_to_path():
    adb_path = os.path.normpath("C:/Android/sdk/platform-tools")  # normalisasi path

    try:
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Environment",
            0,
            winreg.KEY_SET_VALUE | winreg.KEY_QUERY_VALUE
        ) as key:

            try:
                current_path, reg_type = winreg.QueryValueEx(key, "Path")
            except FileNotFoundError:
                current_path = ""
                reg_type = winreg.REG_EXPAND_SZ  # fallback jika PATH belum ada

            # Cek apakah path sudah ada (case-insensitive, Windows style)
            paths = current_path.split(os.pathsep)
            if not any(os.path.normcase(adb_path) == os.path.normcase(p.strip()) for p in paths):
                new_path = current_path + os.pathsep + adb_path if current_path else adb_path
                winreg.SetValueEx(key, "Path", 0, reg_type, new_path)
                print("✅ ADB path added to user PATH.")
            else:
                print("ℹ️ ADB path already in PATH.")
    except Exception as e:
        print(f"⚠️ Failed to update PATH: {e}")
