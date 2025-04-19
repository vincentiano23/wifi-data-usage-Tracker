import psutil

def get_wifi_usage():
    counters = psutil.net_io_counters(pernic=True)
    wifi_data = counters.get("Wi-Fi") or counters.get("WiFi")  # Adjust based on your system

    if wifi_data:
        return wifi_data.bytes_sent, wifi_data.bytes_recv
    else:
        return 0, 0
