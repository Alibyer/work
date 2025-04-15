import ntplib
from time import ctime
import subprocess
import sys
import os

NTP_SERVER = 'pool.ntp.org'

def sync_time():
    try:
        client = ntplib.NTPClient()
        response = client.request(NTP_SERVER, version=3)
        ntp_time = ctime(response.tx_time)
        print(f"[INFO] Время с сервера {NTP_SERVER}: {ntp_time}")

        # Установка времени в систему (требует root)
        formatted_time = response.tx_time
        subprocess.run(['sudo', 'date', '-s', f'@{int(formatted_time)}'], check=True)
        print("[SUCCESS] Системное время синхронизировано.")
    except Exception as e:
        print(f"[ERROR] Не удалось синхронизировать время: {e}")

if __name__ == '__main__':
    if os.geteuid() != 0:
        print("[ERROR] Пожалуйста, запустите скрипт от имени root (sudo).")
        sys.exit(1)

    sync_time()
