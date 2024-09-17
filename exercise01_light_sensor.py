import machine
import time

# Set up the ADC for the photocell (connected to GP28, which is ADC2)
adc = machine.ADC(28)

# Set up the LED for PWM control (connected to GP15 for example)
led = machine.PWM(machine.Pin(15))
led.freq(1000)  # Set PWM frequency for smooth LED control

# Initialize min and max brightness values
min_bright = None
max_bright = None

# Function to map the ADC value to a range of 0 to 100 (percentage)
def map_adc_to_duty(adc_value, min_val, max_val):
    # Clip duty cycle values to the range 0-1
    return max(0, min(1, (adc_value - min_val) / (max_val - min_val)))

# Calibration phase to find min_bright and max_bright
print("Starting calibration...")
calibration_time = 10  # Set a 10-second calibration period
start_time = time.time()

while time.time() - start_time < calibration_time:
    adc_value = adc.read_u16()  # Read the ADC value (0-65535)

    # Set min_bright and max_bright during calibration
    if min_bright is None or adc_value < min_bright:
        min_bright = adc_value
    if max_bright is None or adc_value > max_bright:
        max_bright = adc_value

    print(f"Calibrating... ADC: {adc_value}, Min: {min_bright}, Max: {max_bright}")
    time.sleep(0.5)

print("Calibration done.")
print(f"Final Min Bright: {min_bright}, Max Bright: {max_bright}")

# Main loop to adjust LED brightness based on light sensor
while True:
    adc_value = adc.read_u16()  # Read the photocell ADC value
    duty_cycle = map_adc_to_duty(adc_value, min_bright, max_bright)  # Calculate duty cycle

    # Scale duty cycle to a PWM value (0 to 65535)
    pwm_value = int(duty_cycle * 65535)
    led.duty_u16(pwm_value)

    print(f"ADC: {adc_value}, Duty Cycle: {duty_cycle:.2f}, PWM: {pwm_value}")
    time.sleep(0.1)  # Short delay between readings
