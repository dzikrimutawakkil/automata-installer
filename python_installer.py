import urllib.request
import subprocess
import os
import shutil
import sys
import winreg
import time

def install_python():
    python_version = "3.11.8"
    python_url = f"https://www.python.org/ftp/python/{python_version}/python-{python_version}-amd64.exe"
    installer_path = os.path.join(os.getenv("TEMP"), "python_installer.exe")

    print("Downloading Python installer...")
    urllib.request.urlretrieve(python_url, installer_path)

    print("Running Python installer silently...")
    install_cmd = [
        installer_path,
        "/quiet",
        "InstallAllUsers=1",
        "PrependPath=1",
        "Include_test=0"
    ]
    subprocess.check_call(install_cmd)

    # Tunggu beberapa detik agar instalasi selesai
    time.sleep(5)

    # Cek apakah python sekarang ada di PATH
    if shutil.which("python") is None:
        print("Python is installed, but not in PATH. Attempting to update environment variable...")

        python_path = r"C:\Program Files\Python311"
        if os.path.exists(os.path.join(python_path, "python.exe")):
            os.environ["PATH"] += os.pathsep + python_path

            try:
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                    r"Environment", 0, winreg.KEY_SET_VALUE) as key:
                    current_path, _ = winreg.QueryValueEx(key, "Path")
                    if python_path not in current_path:
                        new_path = current_path + os.pathsep + python_path
                        winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_path)
                        print("Python path added to user environment variables.")
            except Exception as e:
                print("Failed to update registry:", e)
        else:
            print("Python installed, but executable not found. Please check installation.")
    else:
        print("Python successfully installed and available in PATH.")
