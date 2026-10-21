# AI Trashcan

AI Trashcan is an automated waste-sorting project. A Raspberry Pi uses a camera and a TensorFlow Lite image-classification model to identify waste. The result is sent as GPIO signals to a Raspberry Pi Pico, which controls three servo-operated flaps.

## Current project structure

```text
.
├── README.md
├── .gitignore
└── Trashcancode
    ├── Program.py
    ├── main.py
    ├── Trashcan.csproj
    └── japan_2.sln
```

The `.csproj` and solution files are included from the original project setup. The current application code is Python and MicroPython.

## How the system works

### Raspberry Pi: `Trashcancode/Program.py`

`Program.py` runs on a Raspberry Pi and:

1. Captures images from camera index `0`.
2. Crops the region of interest from the camera frame.
3. Resizes the region to `224 x 224` pixels.
4. Runs the image through `model_unquant.tflite`.
5. Classifies the item as `PET`, `Other`, `Can`, or `Empty`.
6. Sends three GPIO signals to the Raspberry Pi Pico.
7. Plays `arigato.mp3` after an item has been sorted.

The camera windows can be closed by pressing `q`.

### Raspberry Pi Pico: `Trashcancode/main.py`

`main.py` runs on a Raspberry Pi Pico with MicroPython. It reads three input signals and controls three PWM servos. A flap opens while its corresponding signal is high and returns to its closed position when the signal goes low.

## Classification

The labels currently configured in `Program.py` are:

| Label | Category | Capacity used by the program |
|---|---|---:|
| `PET` | PET plastic | 2 items |
| `Other` | Burnable/other waste | 3 items |
| `Can` | Cans | 6 items |
| `Empty` | No detected item | No limit |

The classification confidence threshold is `0.5`.

## GPIO configuration

### Raspberry Pi outputs

| Signal | GPIO pin | Destination |
|---|---:|---|
| Signal 1 | GPIO 17 | PET flap |
| Signal 2 | GPIO 18 | Burnable/other waste flap |
| Signal 3 | GPIO 22 | Can flap |

### Raspberry Pi Pico inputs

| Signal | Pico pin | Purpose |
|---|---:|---|
| Signal 1 | GP16 | PET flap |
| Signal 2 | GP19 | Burnable/other waste flap |
| Signal 3 | GP18 | Can flap |

### Raspberry Pi Pico servo outputs

| Servo | Pico pin | Purpose |
|---|---:|---|
| Servo 1 | GP11 | PET flap |
| Servo 2 | GP9 | Burnable/other waste flap |
| Servo 3 | GP13 | Can flap |

The Raspberry Pi and Pico must share a common ground. Check voltage compatibility before connecting GPIO pins.

## Servo calibration

The current PWM duty-cycle values in `main.py` are:

```python
SERVO_OPEN_X_PET = 6767
SERVO_CLOSED_X_PET = 8400

SERVO_OPEN_Y_BURN = 2300
SERVO_CLOSED_Y_BURN = 4000

SERVO_OPEN_Z_CAN = 6969
SERVO_CLOSED_Z_CAN = 4800
```

These values depend on the physical construction and servo installation. Calibrate the servos carefully to prevent the flaps from blocking or overloading the motors.

## Requirements

### Raspberry Pi

- Python 3
- OpenCV
- NumPy
- TensorFlow Lite Runtime
- gpiozero
- `mpg123`
- A connected camera
- The TensorFlow Lite model file `model_unquant.tflite`
- The audio file `arigato.mp3`

Install the Python packages with:

```bash
python3 -m pip install opencv-python numpy gpiozero tflite-runtime
```

Install the audio player on Raspberry Pi OS with:

```bash
sudo apt install mpg123
```

### Raspberry Pi Pico

- Raspberry Pi Pico
- MicroPython firmware
- Thonny or another MicroPython-compatible tool
- Three servo motors

## Setup and usage

### 1. Prepare the Raspberry Pi

Place `model_unquant.tflite` in the directory from which `Program.py` will be started. Place `arigato.mp3` where the program can access it when `mpg123` is called.

From the repository root, start the classifier with:

```bash
python3 Trashcancode/Program.py
```

The program expects the camera to be available as camera index `0`.

### 2. Program the Pico

Copy `Trashcancode/main.py` to the Raspberry Pi Pico and run it with MicroPython. The Pico initializes the three servos in their closed positions and waits for signals from the Raspberry Pi.

## Troubleshooting

### The camera does not open

- Check that the camera is connected.
- Confirm that no other application is using the camera.
- Verify the camera index in `cv2.VideoCapture(0)`.
- On Raspberry Pi OS, check that the camera device is available.

### The model cannot be loaded

- Confirm that `model_unquant.tflite` exists in the program's working directory.
- Check that `tflite-runtime` is installed for the correct Python version and Raspberry Pi architecture.

### The Pico does not move the servos

- Check the servo power supply.
- Verify the servo signal pins.
- Confirm that the Raspberry Pi and Pico share a common ground.
- Check the GPIO signal wiring.
- Recalibrate the PWM values in `main.py`.

### The wrong flap opens

- Verify the Raspberry Pi GPIO mapping.
- Verify the Pico input mapping.
- Confirm that the model labels in `Program.py` match the intended flap.

## Safety

This project controls physical hardware. Test the camera, GPIO signals, and servos separately before running the complete system. Keep hands, cables, and loose objects away from the flaps and servo mechanisms during testing and calibration.

## License

No license has been specified for this repository.
