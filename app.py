from flask import Flask, render_template, request, jsonify
import serial
import serial.tools.list_ports

app = Flask(__name__)

# Find available COM ports
ports = serial.tools.list_ports.comports()
port_list = [port.device for port in ports]

if not port_list:
    print("No available COM ports detected. Exiting...")
    exit()

arduino_port = port_list[0]  # Use first detected port
baud_rate = 9600

try:
    serial_inst = serial.Serial(arduino_port, baud_rate, timeout=1)
    print(f"Connected to {arduino_port}")
except serial.SerialException:
    print("Failed to connect to the Arduino. Check the port and try again.")
    serial_inst = None

@app.route('/')
def index():
    return render_template('switch.html')

@app.route('/control_led', methods=['POST'])
def control_led():
    if serial_inst is None:
        return jsonify({'status': 'error', 'message': 'Arduino not connected'})

    data = request.json
    command = data.get("command", "").upper()

    if command in ["ON", "OFF"]:
        serial_inst.write((command + "\n").encode('utf-8'))  # Send command to Arduino
        return jsonify({'status': 'success', 'message': f'LED turned {command}'})
    else:
        return jsonify({'status': 'error', 'message': 'Invalid command'})

if __name__ == '__main__':
    app.run(debug=True)
