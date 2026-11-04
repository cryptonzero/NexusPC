import sys
import os

# Fix für PyInstaller --noconsole (MUSS vor import speedtest stehen!)
if sys.stdout is None:
    sys.stdout = open(os.devnull, "w")
if sys.stderr is None:
    sys.stderr = open(os.devnull, "w")

import customtkinter
import speedtest
import threading
import subprocess
import socket
from PyLibreHardwareMonitor import Computer

hardware_monitor = Computer(IsCpuEnabled=True, IsGpuEnabled=True)

# darkmode
customtkinter.set_appearance_mode("dark")

# app definition, fenster öffnen
app = customtkinter.CTk()

app.title("NEXUS PC")
app.geometry("1000x650")

# linke sidebar
sidebar = customtkinter.CTkFrame(app,width=200,height=650,fg_color="#333333")
sidebar.pack(side="left")

title = customtkinter.CTkLabel(
    sidebar,
    text="NEXUS",
    font=("Arial", 22, "bold"),
    text_color="#0060FF"
)
title.place(x=10, y=10)

divider = customtkinter.CTkFrame(sidebar,width=180,height=2,fg_color="#0060FF")
divider.place(x=10,y=50)

dashboard_btn = customtkinter.CTkButton(sidebar,width=180,height=35,corner_radius=20,text="Dashboard",fg_color="#0060FF",text_color="#333333")
dashboard_btn.place(x=10,y=60)

internet_btn = customtkinter.CTkButton(sidebar,width=180,height=35,corner_radius=20,text="Internet Speed",fg_color="#0060FF",text_color="#333333")
internet_btn.place(x=10,y=105)

cpu_btn = customtkinter.CTkButton(sidebar,width=180,height=35,corner_radius=20,text="CPU Temperature",fg_color="#0060FF",text_color="#333333")
cpu_btn.place(x=10,y=150)

gpu_btn = customtkinter.CTkButton(sidebar,width=180,height=35,corner_radius=20,text="GPU Temperature",fg_color="#0060FF",text_color="#333333")
gpu_btn.place(x=10,y=195)

ip_btn = customtkinter.CTkButton(sidebar,width=180,height=35,text="My IP",corner_radius=20,fg_color="#0060FF",text_color="#333333")
ip_btn.place(x=10,y=240)

# Frontend
main_content = customtkinter.CTkFrame(app, width=800, height=650, fg_color="#171717")
main_content.place(x=200,y=0)

dashboard_title = customtkinter.CTkLabel(
    main_content,
    text="Dashboard",
    font=("Arial", 28, "bold"),
    text_color="#FFFFFF"
)
dashboard_title.place(x=30, y=25)

welcome_text = customtkinter.CTkLabel(
    main_content,
    text="Welcome back! Here's your PC overview.",
    font=("Arial",13),
    text_color="#888888"
)
welcome_text.place(x=30,y=65)

# Internetspeed UI
speed_card = customtkinter.CTkFrame(main_content,width=300,height=150,fg_color="#252525")
speed_card.place(x=30,y=120)

speed_title = customtkinter.CTkLabel(
    speed_card,
    text="📶 Internet Speed",
    font=("Arial",16,"bold"),
    text_color="white"
)
speed_title.place(x=15,y=15)

speed_value = customtkinter.CTkLabel(
    speed_card,
    text="-- Mbps",
    font=("Arial",28,"bold"),
    text_color="#26C98A",
)
speed_value.place(x=15,y=50)

speed_description = customtkinter.CTkLabel(
    speed_card,
    text="Download Speed",
    font=("Arial",12),
    text_color="#888888",
)
speed_description.place(x=15,y=90)


def start_speedtest():
    speed_btn.configure(
        text="Test läuft...",
        state="disabled"
    )
    detail_speed_btn.configure(
        text="Test läuft...",
        state="disabled"
    )

    threading.Thread(
        target=run_speedtest,
        daemon=True
    ).start()


def run_speedtest():
    try:
        st = speedtest.Speedtest()
        st.get_best_server()

        download = st.download() / 1_000_000
        upload = st.upload() / 1_000_000
        ping = st.results.ping

        app.after(0, lambda: detail_ping.configure(
            text=f"{ping:.0f} ms"
        ))

        app.after(0, lambda: detail_download.configure(
            text=f"{download:.2f} Mbps"
        ))

        app.after(0, lambda: detail_upload.configure(
            text=f"{upload:.2f} Mbps"
        ))

        # Dashboard ebenfalls aktualisieren
        app.after(0, lambda: speed_value.configure(
            text=f"{download:.2f} Mbps"
        ))

        app.after(0, lambda: upload_value.configure(
            text=f"{upload:.2f} Mbps"
        ))

        app.after(0, lambda: speed_btn.configure(
            text="Start Speed Test",
            state="normal"
        ))

        app.after(0, lambda: detail_speed_btn.configure(
            text="Start Speed Test",
            state="normal"
        ))

        print(f"Download: {download:.2f} Mbps")
        print(f"Upload: {upload:.2f} Mbps")

    except Exception as e:
        print("Fehler beim Speedtest:", e)

        app.after(0, lambda: speed_btn.configure(
            text="Erneut versuchen",
            state="normal"
        ))
        app.after(0, lambda: detail_speed_btn.configure(
            text="Erneut versuchen",
            state="normal"
        ))


# Upload Speed UI
upload_card = customtkinter.CTkFrame(
    main_content,
    width=300,
    height=150,
    fg_color="#252525"
)
upload_card.place(x=350, y=120)

upload_title = customtkinter.CTkLabel(
    upload_card,
    text="📤 Upload Speed",
    font=("Arial", 16, "bold"),
    text_color="white"
)
upload_title.place(x=15, y=15)

upload_value = customtkinter.CTkLabel(
    upload_card,
    text="-- Mbps",
    font=("Arial", 28, "bold"),
    text_color="#26C98A"
)
upload_value.place(x=15, y=50)

upload_description = customtkinter.CTkLabel(
    upload_card,
    text="Upload Speed",
    font=("Arial", 12),
    text_color="#888888"
)
upload_description.place(x=15, y=90)

speed_btn = customtkinter.CTkButton(
    speed_card,
    text="Start Speed Test",
    width=160,
    height=25,
    fg_color="#0060FF",
    command=start_speedtest
)
speed_btn.place(x=15,y=120)


# CPU Temperature UI
cpu_card = customtkinter.CTkFrame(main_content,width=300,height=150,fg_color="#252525")
cpu_card.place(x=30,y=290)

cpu_title = customtkinter.CTkLabel(
    cpu_card,
    text="🌡️ CPU Temperature",
    font=("Arial",16,"bold"),
    text_color="white"
)
cpu_title.place(x=15,y=15)

cpu_value = customtkinter.CTkLabel(
    cpu_card,
    text="-- °C",
    font=("Arial",28,"bold"),
    text_color="#26C98A"
)
cpu_value.place(x=15,y=50)

cpu_description = customtkinter.CTkLabel(
    cpu_card,
    text="CPU sensor: LibreHardwareMonitor",
    font=("Arial",12),
    text_color="#888888"
)
cpu_description.place(x=15,y=90)


# Gemeinsame Temperaturabfrage
def read_temperature(device):
    temperatures = []
    sensor_groups = hardware_monitor.cpu if device == "CPU" else hardware_monitor.gpu

    for hardware_name, sensors in sensor_groups.items():
        print(f"[{device}] Gerät: {hardware_name}")
        for name, raw_value in sensors.get("Temperature", {}).items():
            if raw_value is None:
                print(f"[{device}] {name}: Kein Messwert")
                continue

            value = float(raw_value)
            if 0 < value < 120:
                temperatures.append((name, value))
                print(f"[{device}] {name}: {value:.1f} °C")

    if not temperatures:
        return None

    # Bevorzugte Sensoren
    if device == "CPU":
        priorities = ["Package", "Tctl", "Tdie", "Average", "Core"]
    else:
        priorities = ["GPU Core", "Core", "GPU"]

    for keyword in priorities:
        for name, value in temperatures:
            if keyword.lower() in name.lower():
                return value

    return temperatures[0][1]


def run_cpu_temp():
    print("[CPU] Abfrage gestartet...")

    try:
        temp_c = read_temperature("CPU")

        if temp_c is not None:
            print(f"[CPU] Temperatur: {temp_c:.1f} °C")

            app.after(
                0,
                lambda t=temp_c: cpu_value.configure(
                    text=f"{t:.1f} °C"
                )
            )
        else:
            print("[CPU] Kein Temperatursensor verfügbar.")

            app.after(
                0,
                lambda: cpu_value.configure(
                    text="Kein Sensor"
                )
            )

    except Exception as e:
        print("[CPU] Fehler:", e)

        app.after(
            0,
            lambda: cpu_value.configure(text="Fehler")
        )


cpu_refresh_btn = customtkinter.CTkButton(
    cpu_card,
    text="Refresh",
    width=160,
    height=25,
    fg_color="#0060FF",
    command=lambda: threading.Thread(
        target=run_cpu_temp,
        daemon=True
    ).start()
)
cpu_refresh_btn.place(x=15,y=120)


# GPU Temperature UI
gpu_card = customtkinter.CTkFrame(main_content,width=300,height=150,fg_color="#252525")
gpu_card.place(x=350,y=290)

gpu_title = customtkinter.CTkLabel(
    gpu_card,
    text="🌡️GPU Temperature",
    font=("Arial",16,"bold"),
    text_color="white"
)
gpu_title.place(x=15,y=15)

gpu_value = customtkinter.CTkLabel(
    gpu_card,
    text="-- °C",
    font=("Arial",28,"bold"),
    text_color="#26C98A"
)
gpu_value.place(x=15,y=50)

gpu_description = customtkinter.CTkLabel(
    gpu_card,
    text="GPU sensor: LibreHardwareMonitor",
    font=("Arial",12),
    text_color="#888888"
)
gpu_description.place(x=15,y=90)


def run_gpu_temp():
    print("[GPU] Abfrage gestartet...")

    try:
        temp_c = read_temperature("GPU")

        if temp_c is not None:
            print(f"[GPU] Temperatur: {temp_c:.1f} °C")

            app.after(
                0,
                lambda t=temp_c: gpu_value.configure(
                    text=f"{t:.1f} °C"
                )
            )
        else:
            print("[GPU] Kein GPU-Temperatursensor verfügbar.")

            app.after(
                0,
                lambda: gpu_value.configure(
                    text="Kein Sensor"
                )
            )

    except Exception as e:
        print("[GPU] Fehler:", e)

        app.after(
            0,
            lambda: gpu_value.configure(text="Fehler")
        )


gpu_refresh_btn = customtkinter.CTkButton(
    gpu_card,
    text="Refresh",
    width=160,
    height=25,
    fg_color="#0060FF",
    command=lambda: threading.Thread(
        target=run_gpu_temp,
        daemon=True
    ).start()
)
gpu_refresh_btn.place(x=15,y=120)


# Hardware-Kompatibilitätsinfo
hardware_info = customtkinter.CTkLabel(
    main_content,
    text="Temperaturmessung: Funktioniert wahrscheinlich mit den meisten AMD-, Intel- und NVIDIA-Prozessoren und Grafikkarten. Voraussetzung: verfügbare Sensorschnittstelle.",
    font=("Arial", 11),
    text_color="#888888",
    wraplength=730,
    justify="left"
)

hardware_info.place(x=30, y=100)

# MyIP UI

IP_card = customtkinter.CTkFrame(
    main_content,
    width=620,
    height=100,
    fg_color="#252525"
)
IP_card.place(x=30, y=460)


IP_description = customtkinter.CTkLabel(
    IP_card,
    text="🌐 My IP Address",
    font=("Arial", 16, "bold"),
    text_color="white"
)
IP_description.place(x=15, y=12)


IP_value = customtkinter.CTkLabel(
    IP_card,
    text="Loading...",
    font=("Arial", 20, "bold"),
    text_color="#26C98A"
)
IP_value.place(x=15, y=45)


def get_my_ip():
    try:
        import urllib.request

        with urllib.request.urlopen(
            "https://api.ipify.org",
            timeout=10
        ) as response:
            ip = response.read().decode("utf-8").strip()

        app.after(
            0,
            lambda: IP_value.configure(text=ip)
        )
        app.after(
            0,
            lambda: detail_ip_value.configure(text=ip)
        )

    except Exception as e:
        print("[IP] Fehler:", e)

        app.after(
            0,
            lambda: IP_value.configure(text="Verbindung fehlgeschlagen")
        )
        app.after(
            0,
            lambda: detail_ip_value.configure(text="Verbindung fehlgeschlagen")
        )


def refresh_ip():
    IP_value.configure(text="Loading...")
    detail_ip_value.configure(text="Loading...")

    threading.Thread(
        target=get_my_ip,
        daemon=True
    ).start()


IP_refresh_btn = customtkinter.CTkButton(
    IP_card,
    text="Refresh",
    width=110,
    height=30,
    fg_color="#0060FF",
    command=refresh_ip
)
IP_refresh_btn.place(x=490, y=35)


# Internet Speed Seite
internet_frame = customtkinter.CTkFrame(app, width=800, height=650, fg_color="#171717")

internet_page_title = customtkinter.CTkLabel(
    internet_frame,
    text="Internet Speed",
    font=("Arial", 28, "bold"),
    text_color="#FFFFFF"
)
internet_page_title.place(x=30, y=25)

internet_sub = customtkinter.CTkLabel(
    internet_frame,
    text="Check your Download, Upload and Ping.",
    font=("Arial", 13),
    text_color="#888888"
)
internet_sub.place(x=30, y=65)

dl_detail_card = customtkinter.CTkFrame(internet_frame, width=230, height=150, fg_color="#252525")
dl_detail_card.place(x=30, y=120)

dl_detail_title = customtkinter.CTkLabel(dl_detail_card, text="📶 Download", font=("Arial", 16, "bold"), text_color="white")
dl_detail_title.place(x=15, y=15)

detail_download = customtkinter.CTkLabel(dl_detail_card, text="-- Mbps", font=("Arial", 26, "bold"), text_color="#26C98A")
detail_download.place(x=15, y=55)

dl_detail_desc = customtkinter.CTkLabel(dl_detail_card, text="Download Speed", font=("Arial", 12), text_color="#888888")
dl_detail_desc.place(x=15, y=100)

ul_detail_card = customtkinter.CTkFrame(internet_frame, width=230, height=150, fg_color="#252525")
ul_detail_card.place(x=280, y=120)

ul_detail_title = customtkinter.CTkLabel(ul_detail_card, text="📤 Upload", font=("Arial", 16, "bold"), text_color="white")
ul_detail_title.place(x=15, y=15)

detail_upload = customtkinter.CTkLabel(ul_detail_card, text="-- Mbps", font=("Arial", 26, "bold"), text_color="#26C98A")
detail_upload.place(x=15, y=55)

ul_detail_desc = customtkinter.CTkLabel(ul_detail_card, text="Upload Speed", font=("Arial", 12), text_color="#888888")
ul_detail_desc.place(x=15, y=100)

ping_detail_card = customtkinter.CTkFrame(internet_frame, width=230, height=150, fg_color="#252525")
ping_detail_card.place(x=530, y=120)

ping_detail_title = customtkinter.CTkLabel(ping_detail_card, text="⚡ Ping", font=("Arial", 16, "bold"), text_color="white")
ping_detail_title.place(x=15, y=15)

detail_ping = customtkinter.CTkLabel(ping_detail_card, text="-- ms", font=("Arial", 26, "bold"), text_color="#26C98A")
detail_ping.place(x=15, y=55)

ping_detail_desc = customtkinter.CTkLabel(ping_detail_card, text="Ping", font=("Arial", 12), text_color="#888888")
ping_detail_desc.place(x=15, y=100)

detail_speed_btn = customtkinter.CTkButton(
    internet_frame,
    text="Start Speed Test",
    width=180,
    height=35,
    fg_color="#0060FF",
    command=start_speedtest
)
detail_speed_btn.place(x=30, y=300)


# Min/Max Speicher und Warnfarben
cpu_min = None
cpu_max = None
gpu_min = None
gpu_max = None

def get_temp_color(temp):
    if temp < 70:
        return "#26C98A"
    elif temp < 85:
        return "#FFA500"
    else:
        return "#FF4444"


# Erweiterte Sensorabfrage für die Detailseiten
def read_hardware_details(device):
    data = {
        "name": "Unbekanntes Gerät",
        "temp": None,
        "hotspot": None,
        "load": None,
        "power": None,
        "clock": None,
        "fan": None,
        "vram": None
    }

    temps = []
    clocks = []
    sensor_groups = hardware_monitor.cpu if device == "CPU" else hardware_monitor.gpu

    for hardware_name, sensors in sensor_groups.items():
        data["name"] = hardware_name
        for sensor_type, values in sensors.items():
            for s_name, raw_value in values.items():
                if raw_value is None:
                    continue
                val = float(raw_value)

                if sensor_type == "Temperature":
                    if 0 < val < 120:
                        temps.append((s_name, val))
                        if device == "GPU" and "Hot Spot" in s_name:
                            data["hotspot"] = val
                elif sensor_type == "Load":
                    if device == "CPU":
                        if "Total" in s_name or data["load"] is None:
                            data["load"] = val
                    elif "Core" in s_name or data["load"] is None:
                        data["load"] = val
                elif sensor_type == "Power":
                    if device == "CPU":
                        if "Package" in s_name or data["power"] is None:
                            data["power"] = val
                    elif data["power"] is None or "Package" in s_name:
                        data["power"] = val
                elif sensor_type == "Clock":
                    if device == "CPU" and "Core" in s_name:
                        clocks.append(val)
                    elif device == "GPU" and "Core" in s_name:
                        data["clock"] = val
                elif device == "GPU" and sensor_type == "Fan":
                    if data["fan"] is None:
                        data["fan"] = val
                elif device == "GPU" and sensor_type == "SmallData":
                    if "Memory Used" in s_name:
                        data["vram"] = val

    if temps:
        if device == "CPU":
            priorities = ["Package", "Tctl", "Tdie", "Average", "Core"]
        else:
            priorities = ["GPU Core", "Core", "GPU"]

        for keyword in priorities:
            for name, value in temps:
                if keyword.lower() in name.lower():
                    data["temp"] = value
                    break
            if data["temp"] is not None:
                break

        if data["temp"] is None:
            data["temp"] = temps[0][1]

    if device == "CPU" and clocks:
        data["clock"] = sum(clocks) / len(clocks)

    return data


# CPU Temperature Seite
cpu_frame = customtkinter.CTkFrame(app, width=800, height=650, fg_color="#171717")

cpu_page_title = customtkinter.CTkLabel(
    cpu_frame,
    text="CPU Temperature",
    font=("Arial", 28, "bold"),
    text_color="#FFFFFF"
)
cpu_page_title.place(x=30, y=25)

cpu_name_label = customtkinter.CTkLabel(
    cpu_frame,
    text="Processor: Click Refresh to load",
    font=("Arial", 13),
    text_color="#888888"
)
cpu_name_label.place(x=30, y=65)

cpu_auto_switch = customtkinter.CTkSwitch(
    cpu_frame,
    text="Auto-Refresh (2s)",
    font=("Arial", 13),
    text_color="white",
    progress_color="#0060FF"
)
cpu_auto_switch.place(x=580, y=35)

# CPU Temp Detail Card
cpu_detail_card = customtkinter.CTkFrame(cpu_frame, width=350, height=150, fg_color="#252525")
cpu_detail_card.place(x=30, y=120)

cpu_detail_title = customtkinter.CTkLabel(cpu_detail_card, text="🌡️ Temperature", font=("Arial", 16, "bold"), text_color="white")
cpu_detail_title.place(x=15, y=15)

detail_cpu_value = customtkinter.CTkLabel(cpu_detail_card, text="-- °C", font=("Arial", 28, "bold"), text_color="#26C98A")
detail_cpu_value.place(x=15, y=50)

cpu_minmax_label = customtkinter.CTkLabel(cpu_detail_card, text="Min: -- °C  |  Max: -- °C", font=("Arial", 12), text_color="#888888")
cpu_minmax_label.place(x=15, y=95)

# CPU Load Card
cpu_load_card = customtkinter.CTkFrame(cpu_frame, width=350, height=150, fg_color="#252525")
cpu_load_card.place(x=400, y=120)

cpu_load_title = customtkinter.CTkLabel(cpu_load_card, text="⚡ CPU Load", font=("Arial", 16, "bold"), text_color="white")
cpu_load_title.place(x=15, y=15)

cpu_load_value = customtkinter.CTkLabel(cpu_load_card, text="-- %", font=("Arial", 28, "bold"), text_color="#26C98A")
cpu_load_value.place(x=15, y=50)

cpu_load_bar = customtkinter.CTkProgressBar(cpu_load_card, width=310, height=10, progress_color="#0060FF")
cpu_load_bar.set(0)
cpu_load_bar.place(x=15, y=105)

# CPU Power Card
cpu_power_card = customtkinter.CTkFrame(cpu_frame, width=350, height=150, fg_color="#252525")
cpu_power_card.place(x=30, y=290)

cpu_power_title = customtkinter.CTkLabel(cpu_power_card, text="🔌 Power", font=("Arial", 16, "bold"), text_color="white")
cpu_power_title.place(x=15, y=15)

cpu_power_value = customtkinter.CTkLabel(cpu_power_card, text="-- W", font=("Arial", 28, "bold"), text_color="#26C98A")
cpu_power_value.place(x=15, y=50)

cpu_power_desc = customtkinter.CTkLabel(cpu_power_card, text="CPU Package Power", font=("Arial", 12), text_color="#888888")
cpu_power_desc.place(x=15, y=95)

# CPU Clock Card
cpu_clock_card = customtkinter.CTkFrame(cpu_frame, width=350, height=150, fg_color="#252525")
cpu_clock_card.place(x=400, y=290)

cpu_clock_title = customtkinter.CTkLabel(cpu_clock_card, text="⏱️ Clock Speed", font=("Arial", 16, "bold"), text_color="white")
cpu_clock_title.place(x=15, y=15)

cpu_clock_value = customtkinter.CTkLabel(cpu_clock_card, text="-- MHz", font=("Arial", 28, "bold"), text_color="#26C98A")
cpu_clock_value.place(x=15, y=50)

cpu_clock_desc = customtkinter.CTkLabel(cpu_clock_card, text="Average Core Clock", font=("Arial", 12), text_color="#888888")
cpu_clock_desc.place(x=15, y=95)


def run_cpu_details():
    global cpu_min, cpu_max
    try:
        info = read_hardware_details("CPU")

        app.after(0, lambda: cpu_name_label.configure(text=f"Processor: {info['name']}"))

        if info["temp"] is not None:
            t = info["temp"]
            if cpu_min is None or t < cpu_min:
                cpu_min = t
            if cpu_max is None or t > cpu_max:
                cpu_max = t

            color = get_temp_color(t)
            app.after(0, lambda: detail_cpu_value.configure(text=f"{t:.1f} °C", text_color=color))
            app.after(0, lambda: cpu_value.configure(text=f"{t:.1f} °C"))
            app.after(0, lambda: cpu_minmax_label.configure(text=f"Min: {cpu_min:.1f} °C  |  Max: {cpu_max:.1f} °C"))
        else:
            app.after(0, lambda: detail_cpu_value.configure(text="Kein Sensor"))

        if info["load"] is not None:
            l = info["load"]
            app.after(0, lambda: cpu_load_value.configure(text=f"{l:.1f} %"))
            app.after(0, lambda: cpu_load_bar.set(l / 100))

        if info["power"] is not None:
            p = info["power"]
            app.after(0, lambda: cpu_power_value.configure(text=f"{p:.1f} W"))

        if info["clock"] is not None:
            c = info["clock"]
            app.after(0, lambda: cpu_clock_value.configure(text=f"{c:.0f} MHz"))

    except Exception as e:
        print("[CPU Details] Fehler:", e)


detail_cpu_btn = customtkinter.CTkButton(
    cpu_frame,
    text="Refresh",
    width=180,
    height=35,
    fg_color="#0060FF",
    command=lambda: threading.Thread(target=run_cpu_details, daemon=True).start()
)
detail_cpu_btn.place(x=30, y=460)


# GPU Temperature Seite
gpu_frame = customtkinter.CTkFrame(app, width=800, height=650, fg_color="#171717")

gpu_page_title = customtkinter.CTkLabel(
    gpu_frame,
    text="GPU Temperature",
    font=("Arial", 28, "bold"),
    text_color="#FFFFFF"
)
gpu_page_title.place(x=30, y=25)

gpu_name_label = customtkinter.CTkLabel(
    gpu_frame,
    text="Graphics Card: Click Refresh to load",
    font=("Arial", 13),
    text_color="#888888"
)
gpu_name_label.place(x=30, y=65)

gpu_auto_switch = customtkinter.CTkSwitch(
    gpu_frame,
    text="Auto-Refresh (2s)",
    font=("Arial", 13),
    text_color="white",
    progress_color="#0060FF"
)
gpu_auto_switch.place(x=580, y=35)

# GPU Temp Detail Card
gpu_detail_card = customtkinter.CTkFrame(gpu_frame, width=350, height=150, fg_color="#252525")
gpu_detail_card.place(x=30, y=120)

gpu_detail_title = customtkinter.CTkLabel(gpu_detail_card, text="🌡️ Temperature", font=("Arial", 16, "bold"), text_color="white")
gpu_detail_title.place(x=15, y=15)

detail_gpu_value = customtkinter.CTkLabel(gpu_detail_card, text="-- °C", font=("Arial", 28, "bold"), text_color="#26C98A")
detail_gpu_value.place(x=15, y=50)

gpu_minmax_label = customtkinter.CTkLabel(gpu_detail_card, text="Min: -- °C | Max: -- °C | Hot Spot: -- °C", font=("Arial", 12), text_color="#888888")
gpu_minmax_label.place(x=15, y=95)

# GPU Load Card
gpu_load_card = customtkinter.CTkFrame(gpu_frame, width=350, height=150, fg_color="#252525")
gpu_load_card.place(x=400, y=120)

gpu_load_title = customtkinter.CTkLabel(gpu_load_card, text="⚡ GPU Load", font=("Arial", 16, "bold"), text_color="white")
gpu_load_title.place(x=15, y=15)

gpu_load_value = customtkinter.CTkLabel(gpu_load_card, text="-- %", font=("Arial", 28, "bold"), text_color="#26C98A")
gpu_load_value.place(x=15, y=50)

gpu_load_bar = customtkinter.CTkProgressBar(gpu_load_card, width=310, height=10, progress_color="#0060FF")
gpu_load_bar.set(0)
gpu_load_bar.place(x=15, y=105)

# GPU Power & Clock Card
gpu_power_card = customtkinter.CTkFrame(gpu_frame, width=350, height=150, fg_color="#252525")
gpu_power_card.place(x=30, y=290)

gpu_power_title = customtkinter.CTkLabel(gpu_power_card, text="🔌 Power & Clock", font=("Arial", 16, "bold"), text_color="white")
gpu_power_title.place(x=15, y=15)

gpu_power_value = customtkinter.CTkLabel(gpu_power_card, text="-- W  |  -- MHz", font=("Arial", 24, "bold"), text_color="#26C98A")
gpu_power_value.place(x=15, y=55)

gpu_power_desc = customtkinter.CTkLabel(gpu_power_card, text="GPU Power & Core Clock", font=("Arial", 12), text_color="#888888")
gpu_power_desc.place(x=15, y=95)

# GPU Fan & VRAM Card
gpu_fan_card = customtkinter.CTkFrame(gpu_frame, width=350, height=150, fg_color="#252525")
gpu_fan_card.place(x=400, y=290)

gpu_fan_title = customtkinter.CTkLabel(gpu_fan_card, text="🌀 Fan & VRAM", font=("Arial", 16, "bold"), text_color="white")
gpu_fan_title.place(x=15, y=15)

gpu_fan_value = customtkinter.CTkLabel(gpu_fan_card, text="-- RPM  |  -- MB", font=("Arial", 24, "bold"), text_color="#26C98A")
gpu_fan_value.place(x=15, y=55)

gpu_fan_desc = customtkinter.CTkLabel(gpu_fan_card, text="Fan Speed & Memory Used", font=("Arial", 12), text_color="#888888")
gpu_fan_desc.place(x=15, y=95)


def run_gpu_details():
    global gpu_min, gpu_max
    try:
        info = read_hardware_details("GPU")

        app.after(0, lambda: gpu_name_label.configure(text=f"Graphics Card: {info['name']}"))

        if info["temp"] is not None:
            t = info["temp"]
            if gpu_min is None or t < gpu_min:
                gpu_min = t
            if gpu_max is None or t > gpu_max:
                gpu_max = t

            hs_text = f"{info['hotspot']:.1f} °C" if info["hotspot"] is not None else "-- °C"
            color = get_temp_color(t)

            app.after(0, lambda: detail_gpu_value.configure(text=f"{t:.1f} °C", text_color=color))
            app.after(0, lambda: gpu_value.configure(text=f"{t:.1f} °C"))
            app.after(0, lambda: gpu_minmax_label.configure(text=f"Min: {gpu_min:.1f} °C | Max: {gpu_max:.1f} °C | Hot Spot: {hs_text}"))
        else:
            app.after(0, lambda: detail_gpu_value.configure(text="Kein Sensor"))

        if info["load"] is not None:
            l = info["load"]
            app.after(0, lambda: gpu_load_value.configure(text=f"{l:.1f} %"))
            app.after(0, lambda: gpu_load_bar.set(l / 100))

        p_text = f"{info['power']:.1f} W" if info["power"] is not None else "-- W"
        c_text = f"{info['clock']:.0f} MHz" if info["clock"] is not None else "-- MHz"
        app.after(0, lambda: gpu_power_value.configure(text=f"{p_text}  |  {c_text}"))

        f_text = f"{info['fan']:.0f} RPM" if info["fan"] is not None else "-- RPM"
        v_text = f"{info['vram']:.0f} MB" if info["vram"] is not None else "-- MB"
        app.after(0, lambda: gpu_fan_value.configure(text=f"{f_text}  |  {v_text}"))

    except Exception as e:
        print("[GPU Details] Fehler:", e)


detail_gpu_btn = customtkinter.CTkButton(
    gpu_frame,
    text="Refresh",
    width=180,
    height=35,
    fg_color="#0060FF",
    command=lambda: threading.Thread(target=run_gpu_details, daemon=True).start()
)
detail_gpu_btn.place(x=30, y=460)


# Auto-Refresh Schleife
def auto_refresh_loop():
    if cpu_auto_switch.get() == 1:
        threading.Thread(target=run_cpu_details, daemon=True).start()
    if gpu_auto_switch.get() == 1:
        threading.Thread(target=run_gpu_details, daemon=True).start()

    app.after(2000, auto_refresh_loop)

auto_refresh_loop()


# My IP Seite
ip_frame = customtkinter.CTkFrame(app, width=800, height=650, fg_color="#171717")

ip_page_title = customtkinter.CTkLabel(
    ip_frame,
    text="My IP",
    font=("Arial", 28, "bold"),
    text_color="#FFFFFF"
)
ip_page_title.place(x=30, y=25)

ip_page_sub = customtkinter.CTkLabel(
    ip_frame,
    text="Your public and local IP addresses.",
    font=("Arial", 13),
    text_color="#888888"
)
ip_page_sub.place(x=30, y=65)

detail_ip_card = customtkinter.CTkFrame(ip_frame, width=620, height=130, fg_color="#252525")
detail_ip_card.place(x=30, y=120)

detail_ip_title = customtkinter.CTkLabel(
    detail_ip_card,
    text="🌐 My Public IP Address",
    font=("Arial", 16, "bold"),
    text_color="white"
)
detail_ip_title.place(x=15, y=15)

detail_ip_value = customtkinter.CTkLabel(
    detail_ip_card,
    text="Loading...",
    font=("Arial", 28, "bold"),
    text_color="#26C98A"
)
detail_ip_value.place(x=15, y=55)

detail_ip_btn = customtkinter.CTkButton(
    detail_ip_card,
    text="Refresh",
    width=110,
    height=30,
    fg_color="#0060FF",
    command=refresh_ip
)
detail_ip_btn.place(x=490, y=50)

local_ip_card = customtkinter.CTkFrame(ip_frame, width=620, height=120, fg_color="#252525")
local_ip_card.place(x=30, y=270)

local_host_label = customtkinter.CTkLabel(
    local_ip_card,
    text=f"💻 PC Name: {socket.gethostname()}",
    font=("Arial", 16, "bold"),
    text_color="white"
)
local_host_label.place(x=15, y=20)

try:
    local_ip = socket.gethostbyname(socket.gethostname())
except Exception:
    local_ip = "Nicht verfügbar"

local_ip_label = customtkinter.CTkLabel(
    local_ip_card,
    text=f"🏠 Local IP: {local_ip}",
    font=("Arial", 16, "bold"),
    text_color="#26C98A"
)
local_ip_label.place(x=15, y=65)


# Seiten wechseln
frames = [main_content, internet_frame, cpu_frame, gpu_frame, ip_frame]

def show_frame(frame):
    for f in frames:
        f.place_forget()
    frame.place(x=200, y=0)

dashboard_btn.configure(command=lambda: show_frame(main_content))
internet_btn.configure(command=lambda: show_frame(internet_frame))
cpu_btn.configure(command=lambda: show_frame(cpu_frame))
gpu_btn.configure(command=lambda: show_frame(gpu_frame))
ip_btn.configure(command=lambda: show_frame(ip_frame))


# IP automatisch beim Start laden
refresh_ip()

app.mainloop()