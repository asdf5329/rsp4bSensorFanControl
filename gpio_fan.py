import RPi.GPIO as GPIO
import sys
import time

GPIO.cleanup()
# 设置GPIO模式为BCM
GPIO.setmode(GPIO.BCM)

# 定义GPIO17为输出
GPIO.setup(17, GPIO.OUT)

# 根据传入的参数决定是否将GPIO17设置为高电平
if len(sys.argv) > 1 and sys.argv[1] == "1":
    # 将GPIO17设置为高电平（使能）
    GPIO.output(17, GPIO.HIGH)
    print("GPIO17 set to HIGH.")
else:
    # 将GPIO17设置为低电平（禁用）
    GPIO.output(17, GPIO.LOW)
    print("GPIO17 set to LOW.")

# 等待一段时间
#time.sleep(5)

# 清理GPIO状态
#GPIO.cleanup()
print("GPIO cleanup completed.")

