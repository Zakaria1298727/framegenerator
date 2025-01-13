# Ethernet Frame Generator with Flask and PyTorch

This project is a web application built with Flask and PyTorch that generates Ethernet frames using a trained deep learning model. The application allows users to generate frames dynamically and stores them in a list, which can be displayed in a table on the front end.

---

## Features
- **Ethernet Frame Generation**: Generates Ethernet frames using a PyTorch-based deep learning model.
- **Dynamic Storage**: Stores generated frames in a list and displays them in a table.
- **Web Interface**: A simple web interface built with Flask and HTML/JavaScript for interacting with the model.

---

## Prerequisites
Before running the project, ensure you have the following installed:
- Python 3.8 or higher
- Flask
- PyTorch
- NumPy
- Pandas (if using dataset functionality)
# How to Use
## 1. Generate Frames
Click the "Generate Frame" button to generate a new Ethernet frame.

Each frame will be added to the table below the button.

## 2. View Generated Frames
The table displays all generated frames, including:

- Time: The timestamp of the frame.

- Source IP: The source IP address.

- Destination IP: The destination IP address.

- Protocol: The protocol used (e.g., TCP, UDP, ICMP).

- Length: The length of the frame.

## 3. API Endpoints
The application provides the following API endpoints:

- /generate: Generates a new Ethernet frame and returns it in JSON format.

- /frames: Returns a list of all generated frames in JSON format.
