#coded by Shashank
import machine
import math
import time


dac_pin = 25  # Adjust according to your ESP32 board
dac = machine.DAC(machine.Pin(dac_pin))

# Define parameters for the sine wave
sampling_freq = 10000  # Sampling frequency (Hz)
frequency = 100  # Frequency of the sine wave (Hz)
amplitude = 127  # Amplitude of the sine wave (0 - 255)
phase = 0  # Phase of the sine wave

# Define a function to generate a sine wave using a DAC for a specific duration
def generate_sine_wave(duration_sec):
    time_step = 1 / sampling_freq 

    start_time = time.time()

    while (time.time() - start_time) < duration_sec:  # Run for the specified duration
        for i in range(sampling_freq):
            sample = int(amplitude * math.sin(2 * math.pi * frequency * i * time_step + phase)) + 127
            dac.write(sample)
            time.sleep(time_step)

# SoftI2C setup for RTC on ESP32
i2c = machine.SoftI2C(scl=machine.Pin(22), sda=machine.Pin(21))
rtc_address = 0x68 


rtc_time = bytearray([0x00, 0x40, 0x18, 0x04, 0x06, 0x01, 0x24])
i2c.writeto_mem(rtc_address, 0, rtc_time)
print("RTC time set manually to:", rtc_time)

led = machine.Pin(2, machine.Pin.OUT)

def bcd_to_decimal(bcd):
    return (bcd >> 4) * 10 + (bcd & 0x0F)

while True:
    data = i2c.readfrom_mem(rtc_address, 0, 7)
    hour = bcd_to_decimal(data[2] & 0x3F)
    minute = bcd_to_decimal(data[1])

    print("RTC time set manually to:", hour, minute)

    if hour == 18 and minute >= 41 and minute <= 48:
        led.on()
        generate_sine_wave(10)  # Generate sine wave for 10 seconds
        led.off()

    time.sleep(30)
