from flask import Flask, send_from_directory, request, jsonify
import time
import threading

# Create the Flask application object
app = Flask(__name__)

# Use a dictionary to store heartbeat data
beacon_status = {}

# Route to serve the static HTML file
@app.route('/')
def serve_html():
    return send_from_directory('.', 'index.html')

# Heartbeat API endpoint
@app.route('/heartbeat', methods=['POST'])
def heartbeat():
    data = request.json
    beacon_id = data.get('id', 'Unknown')
    # Save the beacon's ID and the current timestamp
    beacon_status[beacon_id] = {'last_seen': time.time()}
    print(f"Heartbeat received from Beacon ID: {beacon_id}")
    return jsonify({"status": "ok"})

# Create the Admin Dashboard Endpoint
@app.route('/admin')
def serve_admin():
    return send_from_directory('.', 'admin.html')

@app.route('/admin/status')
def admin_status():
    return jsonify(beacon_status)

# Function to check for missing heartbeats in a separate thread
def check_for_missing_heartbeats():
    while True:
        current_time = time.time()
        inactive_beacons = []

        for beacon_id, data in beacon_status.items():
            if (current_time - data['last_seen']) > 60:
                inactive_beacons.append(beacon_id)

        for beacon_id in inactive_beacons:
            print(f"Beacon {beacon_id} is offline. Removing from status list.")
            del beacon_status[beacon_id]

        time.sleep(30)

# Run the Flask server
if __name__ == '__main__':
    # Start the background thread for the heartbeat check
    heartbeat_checker_thread = threading.Thread(target=check_for_missing_heartbeats)
    heartbeat_checker_thread.daemon = True
    heartbeat_checker_thread.start()

    app.run(host='0.0.0.0', port=5000)
