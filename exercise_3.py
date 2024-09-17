import machine
import time
import random
import urequests  

# Number of flashes
N = 10
on_ms = 500  # LED on dur in milliseconds


database_api_url = "https://miniproject-8794a-default-rtdb.firebaseio.com/response-times.json"

def random_time_interval(tmin: float, tmax: float) -> float:
    #Return a random time interval between tmin and tmax
    return random.uniform(tmin, tmax)

def compute_stats(times):
    #Compute the min, max, and ave response times
    valid_times = [t for t in times if t is not None]  # filters out none values
    if not valid_times:
        return None, None, None  

    avg_time = sum(valid_times) / len(valid_times)
    min_time = min(valid_times)
    max_time = max(valid_times)

    return min_time, max_time, avg_time

#Upload response data to Firebase using a PUT request
def upload_to_cloud(data):
    try:
        response = urequests.put(database_api_url, json=data)
        
        if response.status_code == 200:
            print("The data was uploaded successfully to Firebase")
        else:
            print(f"It failed to upload the data: {response.status_code}")
    except Exception as e:
        print(f"There was an error during cloud upload: {e}")

#Run the LED flashing game and measure response times
def game(N, led, button):
    times = []

    for i in range(N):
        time.sleep(random_time_interval(0.5, 3.0))  # random delay between flashes
        led.high()
        start_time = time.ticks_ms()  #starting the timer when LED turns on
        response_time = None
        
        while time.ticks_diff(time.ticks_ms(), start_time) < on_ms:
            if button.value() == 0:  # Button pressed
                response_time = time.ticks_diff(time.ticks_ms(), start_time)
                break
        
        led.low()  
        times.append(response_time)
        time.sleep(0.5)  

    return times

if __name__ == "__main__":
    # Setup LED and button
    led = machine.Pin("LED", machine.Pin.OUT)
    button = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_UP)

    # Blink LED to indicate when the game starts
    for _ in range(3):
        led.high()
        time.sleep(0.2)
        led.low()
        time.sleep(0.2)

    #run game and measure response times
    response_times = game(N, led, button)

    # Calc stats
    min_time, max_time, avg_time = compute_stats(response_times)

    # Print stats
    print(f"Minimum Response Time: {min_time} ms")
    print(f"Maximum Response Time: {max_time} ms")
    print(f"Average Response Time: {avg_time} ms")

    # Prepare data for cloud upload
    data = {
        "min_time": min_time,
        "max_time": max_time,
        "avg_time": avg_time,
        "response_times": response_times,
        "total_flashes": N,
        "misses": response_times.count(None),
    }

    # Upload to Firebase
    upload_to_cloud(data)

