import RPi.GPIO as GPIO
import time
from datetime import datetime, time as dtime

# 设置GPIO模式为BCM
GPIO.setmode(GPIO.BCM)

# 定义风扇和指示灯连接的GPIO引脚
FAN_PIN = 18
INDICATOR_PIN = 17

# 设置GPIO引脚为输出模式
GPIO.setup(FAN_PIN, GPIO.OUT)
GPIO.setup(INDICATOR_PIN, GPIO.OUT)

# 初始化PWM对象，频率为25KHz
fan = GPIO.PWM(FAN_PIN, 250)

fan.start(0)  # 初始占空比为0

def get_cpu_temp():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            temp = float(f.read()) / 1000.0
        return temp
    except Exception as e:
        print(f"Error reading temperature: {e}")
        return None

def is_night_time():
    current_time = datetime.now().time()
    night_start = dtime(22, 0)  # 晚上10点
    morning_end = dtime(7, 0)  # 早上7点
    return night_start <= current_time or current_time <= morning_end

try:
    current_duty_cycle = 0
    last_log_time = time.time()  # 记录上一次日志的时间
    while True:
        temp = get_cpu_temp()
        if temp is None:
            continue

        # 获取当前时间
        current_time = datetime.now().strftime("%Y%m%d_%H:%M:%S")
        
        # 根据是否为夜间调整风扇速度
        if is_night_time():
            if 35 <= temp <= 38:  # 温度在18°C到35°C之间时，占空比固定为8%
                duty_cycle = 8
            else:
                duty_cycle = min(20, max(0, min(int((temp - 35) * 100 / 35), 100)))
        else:
            if 35 <= temp <= 38:  # 温度在18°C到35°C之间时，占空比固定为8%
                duty_cycle =8
            else:
                duty_cycle = max(1.5, min(int((temp - 35) * 100 / 35), 100))

        fan.ChangeDutyCycle(duty_cycle)

        # 控制指示灯状态
        if temp > 30:
            GPIO.output(INDICATOR_PIN, GPIO.HIGH)
        else:
            GPIO.output(INDICATOR_PIN, GPIO.LOW)

        # 打印当前时间、CPU温度和风扇占空比
        print(f"{current_time} - Current CPU Temp: {temp}°C, Fan Duty Cycle: {duty_cycle}%")
        # 检查是否已经超过一分钟，如果是，则记录日志
        if time.time() - last_log_time >= 60 and temp >= 38:
            with open('/var/log/fan_temp.txt', 'a') as log_file:
                log_file.write(f"{current_time} - Current CPU Temp: {temp}°C, Fan Duty Cycle: {duty_cycle}%\n")
            last_log_time = time.time()  # 更新上一次日志的时间
        time.sleep(5)  # 每5秒检查一次温度

except KeyboardInterrupt:
    pass

finally:
    fan.stop()
    GPIO.cleanup()
    print("Fan control stopped.")

