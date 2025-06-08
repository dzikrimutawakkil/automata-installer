import os
import sys
import zipfile
import winreg
import shutil

sdk_root = r"C:\Android\sdk"
zip_file_name = "commandlinetools.zip"

def install_android_sdk():
    extract_sdk_zip()
    set_android_env()
    print("✅ SDK installed and environment variables set.")

def extract_sdk_zip():
    os.makedirs(sdk_root, exist_ok=True)
    zip_path = get_resource_path(zip_file_name)
    print(f"📦 Extracting '{zip_path}' to '{sdk_root}'...")

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(sdk_root)

    # After extraction, fix cmdline-tools/latest folder
    fix_cmdline_tools_latest()

    print("✅ Extraction and structure setup completed.")

def fix_cmdline_tools_latest():
    cmdline_tools_path = os.path.join(sdk_root, "cmdline-tools")
    latest_path = os.path.join(cmdline_tools_path, "latest")

    if not os.path.isdir(cmdline_tools_path):
        print(f"⚠️ {cmdline_tools_path} does not exist after extraction.")
        return

    # Case 1: cmdline-tools contains 'bin' folder directly — need to move contents into latest/
    if os.path.isdir(os.path.join(cmdline_tools_path, "bin")):
        # Move all files/folders inside cmdline-tools into latest/
        if not os.path.exists(latest_path):
            os.makedirs(latest_path)
        for item in os.listdir(cmdline_tools_path):
            if item == "latest":
                continue
            src = os.path.join(cmdline_tools_path, item)
            dst = os.path.join(latest_path, item)
            print(f"Moving {src} -> {dst}")
            shutil.move(src, dst)
        print(f"✅ Moved cmdline-tools contents into 'latest' folder.")
        return

    # Case 2: cmdline-tools contains one subfolder (like cmdline-tools-9.0)
    subdirs = [d for d in os.listdir(cmdline_tools_path) if os.path.isdir(os.path.join(cmdline_tools_path, d))]
    if "latest" in subdirs:
        print("ℹ️ 'latest' directory already exists in cmdline-tools.")
        return

    if len(subdirs) == 1:
        extracted_dir = subdirs[0]
        extracted_dir_path = os.path.join(cmdline_tools_path, extracted_dir)
        # Rename or move to latest
        try:
            os.rename(extracted_dir_path, latest_path)
            print(f"✅ Renamed '{extracted_dir}' to 'latest' inside cmdline-tools.")
        except OSError:
            shutil.copytree(extracted_dir_path, latest_path)
            print(f"✅ Copied '{extracted_dir}' to 'latest' inside cmdline-tools.")
        return

    print("⚠️ Unexpected structure inside cmdline-tools, manual fix may be required.")
    print(f"Found directories: {subdirs}")


def set_android_env():
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment", 0,
                            winreg.KEY_READ | winreg.KEY_WRITE) as key:

            # Set ANDROID_HOME
            winreg.SetValueEx(key, "ANDROID_HOME", 0, winreg.REG_EXPAND_SZ, sdk_root)
            print(f"✅ ANDROID_HOME set to {sdk_root}")

            # Paths to add
            platform_path = os.path.join(sdk_root, "platform-tools")
            tools_path = os.path.join(sdk_root, "cmdline-tools", "latest", "bin")

            update_user_path(key, [platform_path, tools_path])

    except Exception as e:
        print(f"⚠️ Failed to set environment variables: {e}")

def update_user_path(reg_key, paths_to_add):
    try:
        current_path, reg_type = winreg.QueryValueEx(reg_key, "Path")
    except FileNotFoundError:
        current_path = ""
        reg_type = winreg.REG_EXPAND_SZ

    existing = current_path.split(os.pathsep) if current_path else []
    new_paths = []

    for path in paths_to_add:
        if os.path.isdir(path) and not any(os.path.normcase(path) == os.path.normcase(p.strip()) for p in existing):
            new_paths.append(path)

    if new_paths:
        full_path = current_path + os.pathsep + os.pathsep.join(new_paths) if current_path else os.pathsep.join(new_paths)
        winreg.SetValueEx(reg_key, "Path", 0, reg_type, full_path)
        for p in new_paths:
            print(f"✅ Added to PATH: {p}")
    else:
        print("ℹ️ All paths already in PATH.")

def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)
