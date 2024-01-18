import psutil
import speedtest
import platform
import socket
import subprocess
import wmi
from screeninfo import get_monitors
from uuid import getnode as get_mac
import pygetwindow as gw
import ctypes
def get_screen_size():
    try:
        primary_monitor = get_monitors()[0]  # Get the primary monitor
        dpi = ctypes.windll.user32.GetDpiForSystem()
        width, height = primary_monitor.width/dpi, primary_monitor.height/dpi
        return f"{width}x{height}"
    except Exception as e:
        return "Not available"
def get_installed_software():
    installed_software = subprocess.check_output(['wmic', 'product', 'get', 'name']).decode('utf-8').split('\n')[1:-1]
    return installed_software

def get_internet_speed():
    st = speedtest.Speedtest()
    download_speed = st.download() / 1_000_000  # Convert to Mbps
    upload_speed = st.upload() / 1_000_000  # Convert to Mbps
    return download_speed, upload_speed

def get_screen_resolution():
    monitors = get_monitors()
    resolutions = [(monitor.width, monitor.height) for monitor in monitors]
    return resolutions

def get_cpu_info():
    cpu_info = {}
    cpu_info['model'] = platform.processor()
    cpu_info['cores'] = psutil.cpu_count(logical=False)
    cpu_info['threads'] = psutil.cpu_count(logical=True)
    return cpu_info

def get_gpu_info():
    try:
        w = wmi.WMI()
        gpu_info = w.Win32_VideoController()[0].name
        return gpu_info
    except Exception as e:
        return None

def get_ram_size():
    ram_info = psutil.virtual_memory()
    ram_size_gb = ram_info.total / (1024**3)  # Convert to GB
    return ram_size_gb



def get_network_info():
    mac_address = ':'.join(['{:02x}'.format((int(i, 16) + 2) % 256) for i in hex(get_mac())[-12:]])
    public_ip = socket.gethostbyname(socket.gethostname())
    return mac_address, public_ip

def get_windows_version():
    return platform.platform()

if __name__ == "__main__":
    print("Installed Software:", get_installed_software())
    download_speed, upload_speed = get_internet_speed()
    print(f"Internet Speed: Download: {download_speed:.2f} Mbps, Upload: {upload_speed:.2f} Mbps")
    print("Screen Resolution:", get_screen_resolution())
    print("CPU Info:", get_cpu_info())
    gpu_info = get_gpu_info()
    print("GPU Info:", gpu_info if gpu_info else "Not available")
    print("RAM Size:", get_ram_size(), "GB")
    print("Screen Size in width X height inches :", get_screen_size())
    mac_address, public_ip = get_network_info()
    print("Wifi/Ethernet MAC Address:", mac_address)
    print("Public IP Address:", public_ip)
    print("Windows Version:", get_windows_version())
