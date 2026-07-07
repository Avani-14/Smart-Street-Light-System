import RPi.GPIO as GPIO
import serial
import time
import pynmea2

# GPIO setup for buzzer and LED
BUZZER_PIN = 18  # GPIO 18 (Pin 12)
LED_PIN = 17     # GPIO 17 (Pin 11)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.setup(LED_PIN, GPIO.OUT)

# Serial setup for GSM (SIM900A) and GPS (NEO-6M)
GSM_PORT = "/dev/serial0"  # Raspberry Pi UART (GPIO 14/15)
GPS_PORT = "/dev/ttyUSB0"  # USB-to-serial adapter for GPS
BAUD_RATE = 9600

# Initialize serial connections
gsm_serial = serial.Serial(GSM_PORT, BAUD_RATE, timeout=1)
gps_serial = serial.Serial(GPS_PORT, BAUD_RATE, timeout=1)

# Emergency contact number (replace with actual number)
EMERGENCY_NUMBER = "+917587045168"  # Example: "+12025550123"

def initialize_gsm():
    """Initialize the SIM900A GSM module."""
    print("Initializing GSM module...")
    gsm_serial.write(b'AT\r\n')
    time.sleep(1)
    response = gsm_serial.read(gsm_serial.in_waiting).decode()
    if "OK" in response:
        print("GSM module initialized.")
    else:
        print("GSM initialization failed.")
        return False
    
    # Set SMS mode to text
    gsm_serial.write(b'AT+CMGF=1\r\n')
    time.sleep(1)
    response = gsm_serial.read(gsm_serial.in_waiting).decode()
    if "OK" in response:
        print("SMS mode set to text.")
        return True
    else:
        print("Failed to set SMS mode.")
        return False

def send_sms(number, message):
    """Send an SMS using the SIM900A GSM module."""
    print(f"Sending SMS to {number}...")
    gsm_serial.write(b'AT+CMGS="' + number.encode() + b'"\r\n')
    time.sleep(1)
    gsm_serial.write(message.encode() + b"\r\n")
    time.sleep(1)
    gsm_serial.write(bytes([26]))  # Ctrl+Z to send SMS
    time.sleep(2)
    response = gsm_serial.read(gsm_serial.in_waiting).decode()
    if "+CMGS" in response:
        print("SMS sent successfully.")
    else:
        print("Failed to send SMS.")

def get_gps_location():
    """Read GPS data from NEO-6M and return latitude and longitude."""
    print("Reading GPS data...")
    while True:
        line = gps_serial.readline().decode('utf-8', errors='ignore')
        if line.startswith('$GPGGA'):
            try:
                msg = pynmea2.parse(line)
                if msg.latitude and msg.longitude:
                    latitude = f"{msg.latitude:.6f} {msg.lat_dir}"
                    longitude = f"{msg.longitude:.6f} {msg.lon_dir}"
                    print(f"Location: {latitude}, {longitude}")
                    return latitude, longitude
            except pynmea2.ParseError:
                print("Error parsing GPS data.")
        time.sleep(0.1)
    return None, None

def accident_detected():
    """Placeholder for accident detection using SmartCam SMCM-NS1T1AN."""
    coord = get_gps_location()
    #Upload the accident.ipynb code here i am writing this for you 

    
    time.sleep(2)  # Simulate processing time
    return True  # Simulated accident detection

def alert_nearby():
    """Activate buzzer and flash LED to alert nearby people."""
    print("Alerting nearby people...")
    for _ in range(5):  # Flash and beep 5 times
        GPIO.output(LED_PIN, GPIO.HIGH)
        GPIO.output(BUZZER_PIN, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(LED_PIN, GPIO.LOW)
        GPIO.output(BUZZER_PIN, GPIO.LOW)
        time.sleep(1)

def main():
    try:
        # Initialize GSM module
        if not initialize_gsm():
            print("Exiting due to GSM initialization failure.")
            return

        while True:
            # Check for accident (placeholder for SmartCam detection)
            if accident_detected():
                print("Accident detected!")
                
                # Get GPS location
                latitude, longitude = get_gps_location()
                if latitude and longitude:
                    # Send SMS to emergency services
                    message = f"Accident detected! Location: {latitude}, {longitude}"
                    send_sms(EMERGENCY_NUMBER, message)
                
                # Alert nearby people
                alert_nearby()
            else:
                print("No accident detected.")
                time.sleep(5)  # Check again after 5 seconds

    except KeyboardInterrupt:
        print("Program terminated by user.")
    finally:
        # Cleanup
        GPIO.cleanup()
        gsm_serial.close()
        gps_serial.close()
        print("Resources cleaned up.")

if __name__ == "__main__":
    main()