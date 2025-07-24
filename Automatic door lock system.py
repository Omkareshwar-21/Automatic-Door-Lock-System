import time

# --- MOCK GPIO MODULE FOR SIMULATION ---
class MockPWM:
    def _init_(self, pin, freq):
        self.pin = pin
        self.freq = freq
        print(f"[PWM] Initialized on pin {pin} with frequency {freq}Hz")

    def start(self, duty_cycle):
        print(f"[PWM] Started with duty cycle: {duty_cycle}%")

    def ChangeDutyCycle(self, duty_cycle):
        print(f"[PWM] Changed duty cycle to: {duty_cycle}%")

    def stop(self):
        print("[PWM] Stopped")

class MockGPIO:
    BCM = "BCM"
    OUT = "OUT"
    HIGH = 1
    LOW = 0

    def setmode(self, mode):
        print(f"[GPIO] Mode set to {mode}")

    def setwarnings(self, flag):
        pass

    def setup(self, pin, mode):
        print(f"[GPIO] Pin {pin} setup as {mode}")

    def output(self, pin, state):
        state_str = "HIGH" if state else "LOW"
        print(f"[GPIO] Pin {pin} output set to {state_str}")

    def cleanup(self):
        print("[GPIO] Cleaned up")

    def PWM(self, pin, freq):
        return MockPWM(pin, freq)

# Replace RPi.GPIO with mock
GPIO = MockGPIO()

# --- Constants ---
SERVO_PIN = 18
BUZZER_PIN = 23
LED_PIN = 24
CORRECT_PASSWORD = "1234"

# --- Setup ---
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(SERVO_PIN, GPIO.OUT)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.setup(LED_PIN, GPIO.OUT)

servo = GPIO.PWM(SERVO_PIN, 50)
servo.start(0)

# --- Functions ---
def unlock_door():
    print("✅ Door Unlocked")
    GPIO.output(LED_PIN, GPIO.HIGH)
    servo.ChangeDutyCycle(7)
    time.sleep(0.5)
    servo.ChangeDutyCycle(0)
    time.sleep(2)
    lock_door()

def lock_door():
    print("🔒 Door Locked")
    GPIO.output(LED_PIN, GPIO.LOW)
    servo.ChangeDutyCycle(2)
    time.sleep(0.5)
    servo.ChangeDutyCycle(0)

def access_denied():
    print("❌ Access Denied!")
    GPIO.output(BUZZER_PIN, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(BUZZER_PIN, GPIO.LOW)

# --- Main Program ---
def main():
    try:
        lock_door()
        while True:
            password = input("Enter Password: ").strip()
            if password == CORRECT_PASSWORD:
                unlock_door()
            else:
                access_denied()

    except KeyboardInterrupt:
        print("\nExiting Program...")

    finally:
        servo.stop()
        GPIO.cleanup()
        print("GPIO Cleaned Up.")

if _name_ == "_main_":
    main()