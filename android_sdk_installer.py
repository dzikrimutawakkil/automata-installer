import os
import sys
import urllib.request
import zipfile
import shutil
import winreg

sdk_root = r"C:\Android\sdk"
ZIP_FILE = "commandlinetools.zip"  # Bundled in EXE

def install_android_sdk():
    tools_base = os.path.join(sdk_root, "cmdline-tools")
    temp_extract = os.path.join(tools_base, "temp")
    tools_target = os.path.join(tools_base, "latest")

    print("📦 Extracting SDK tools...")
    extract_files()

    # Validasi struktur setelah ekstrak
    source_dir = os.path.join(temp_extract, "cmdline-tools")
    if not os.path.isdir(source_dir):
        print(f"❌ Folder not found: {source_dir}")
        return

    # Hapus folder 'latest' jika sudah ada
    if os.path.exists(tools_target):
        shutil.rmtree(tools_target)

    # Pindahkan seluruh cmdline-tools ke latest/
    shutil.move(source_dir, tools_target)

    shutil.rmtree(temp_extract, ignore_errors=True)

    # Buat folder platform-tools (jika belum ada)
    platform_tools = os.path.join(sdk_root, "platform-tools")
    os.makedirs(platform_tools, exist_ok=True)

    add_to_user_path(platform_tools)

    print("✅ Android SDK tools installed successfully.")

def extract_files():
    os.makedirs(sdk_root, exist_ok=True)
    zip_path = get_resource_path(ZIP_FILE)
    extract_zip(zip_path, os.path.join(sdk_root, "cmdline-tools", "temp"))

def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def extract_zip(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

def add_to_user_path(path_to_add):
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment", 0,
                            winreg.KEY_SET_VALUE | winreg.KEY_QUERY_VALUE) as key:
            try:
                current_path, reg_type = winreg.QueryValueEx(key, "Path")
            except FileNotFoundError:
                current_path = ""
                reg_type = winreg.REG_EXPAND_SZ

            paths = current_path.split(os.pathsep)
            if not any(os.path.normcase(path_to_add) == os.path.normcase(p.strip()) for p in paths):
                new_path = current_path + os.pathsep + path_to_add if current_path else path_to_add
                winreg.SetValueEx(key, "Path", 0, reg_type, new_path)
                print(f"✅ Added to PATH: {path_to_add}")
            else:
                print("ℹ️ Already in PATH.")
    except Exception as e:
        print(f"⚠️ Failed to update PATH: {e}")
