import RPi.GPIO as GPIO
import time

# 设置GPIO模式为BCM
GPIO.setmode(GPIO.BCM)

# 定义GPIO 4作为输出
GPIO.setup(4, GPIO.OUT)

try:
    while True:
        # 使GPIO 4高电平（LED亮）
        GPIO.output(4, GPIO.HIGH)
        print("Feeding the dog...")
        time.sleep(10)  # 等待1秒让LED亮着
        # 使GPIO 4低电平（LED熄灭）
        GPIO.output(4, GPIO.LOW)
        time.sleep(10)  # 再等待9秒，总共10秒

except KeyboardInterrupt:
    # 当按下Ctrl+C时，清理GPIO设置
    GPIO.cleanup()

