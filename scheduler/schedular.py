import schedule
import time
import subprocess
import os

def run_daily_job():
    # Ana klasörün yolu
    base_path = os.path.dirname(os.path.abspath(__file__))
    # 'main' klasörünün yolu
    main_path = os.path.join(base_path, '..', 'main')  # '..' ile bir üst dizine çıkıyoruz
    
    # 'producer.py' ve 'consumer.py' dosyalarını çalıştırma
    subprocess.run(["python", os.path.join(main_path, 'kafkaProducer.py')])
    subprocess.run(["python", os.path.join(main_path, 'kafkaConsumer.py')])


# Günlük işlemi her gün belirli bir saatte çalıştırmak için
schedule.every().day.at("10:05").do(run_daily_job)  # Örnek saat: 08:00

# Schedule'ın çalışması için bir döngü başlat
while True:
    schedule.run_pending()
    time.sleep(60)  # Her döngüde 60 saniye bekleyerek çalışmasını sağla