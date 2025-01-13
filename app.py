from flask import Flask, render_template, jsonify
import torch
from model import EthernetFrameGenerator, generate_frame
import numpy as np  # Import NumPy for type conversion

app = Flask(__name__)

# Charger le modèle
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = EthernetFrameGenerator().to(device)
model.load_state_dict(torch.load('ethernet_generator.pth', map_location=device))
model.eval()

# Dictionnaire pour décoder les protocoles
protocol_mapping = {0: 'ICMP', 1: 'UDP', 2: 'TCP', 3: 'TLSv1.2', 4: 'RARP'}

# Liste pour stocker les trames générées
generated_frames = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['GET'])
def generate():
    generated_frame = generate_frame(model, device)
    
    # Dénormalisation des valeurs
    time = denormalize_time(generated_frame[0], 0.0, 100.0)
    source_ip = float_to_ip(generated_frame[1])
    dest_ip = float_to_ip(generated_frame[2])
    protocol = decode_protocol(generated_frame[3])
    length = denormalize_length(generated_frame[4])
    
    original_frame = {
        "Time": float(time),  # Convert to standard Python float
        "Source": source_ip,
        "Destination": dest_ip,
        "Protocol": protocol,
        "Length": float(length)  # Convert to standard Python float
    }
    
    # Ajouter la trame générée à la liste
    generated_frames.append(original_frame)
    
    return jsonify(original_frame)

@app.route('/frames', methods=['GET'])
def get_frames():
    # Convert all float32 values in the list to standard Python floats
    frames_to_return = []
    for frame in generated_frames:
        frame_converted = {
            "Time": float(frame["Time"]),
            "Source": frame["Source"],
            "Destination": frame["Destination"],
            "Protocol": frame["Protocol"],
            "Length": float(frame["Length"])
        }
        frames_to_return.append(frame_converted)
    
    return jsonify(frames_to_return)

def denormalize_time(normalized_time, time_min, time_max):
    return (normalized_time * (time_max - time_min)) + time_min

def float_to_ip(normalized_ip):
    ip_int = int(normalized_ip * (256 ** 4))
    return '.'.join(str((ip_int >> (8 * i)) & 0xFF) for i in reversed(range(4)))

def decode_protocol(normalized_protocol):
    protocol_integer = int(round(normalized_protocol * len(protocol_mapping)))
    return protocol_mapping.get(protocol_integer, 'Unknown')

def denormalize_length(normalized_length):
    return normalized_length * 1500

if __name__ == '__main__':
    app.run(debug=True)