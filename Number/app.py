from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
port = 8008

request_timeout = 0.5  # seconds

# Helper function to fetch data from a URL with a timeout
def fetch_data(url):
    try:
        response = requests.get(url, timeout=request_timeout)
        return response.json().get('numbers', [])
    except requests.exceptions.RequestException as error:
        print(f"Error fetching data from URL: {url}")
        return []

# Main API endpoint
@app.route('/numbers', methods=['GET'])
def get_numbers():
    url = request.args.get('url')

    if not url:
        return jsonify({'error': 'At least one URL is required.'}), 400

    urls = url if isinstance(url, list) else [url]

    # Fetch data from all provided URLs concurrently
    responses = [fetch_data(url) for url in urls]

    # Merge and sort unique integers
    merged_numbers = sorted(set([num for sublist in responses for num in sublist]))

    return jsonify({'numbers': merged_numbers})

# Start the server
if __name__ == '__main__':
    app.run(port=port)

