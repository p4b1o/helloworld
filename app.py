from flask import Flask, render_template, request, jsonify, send_from_directory
import requests
import re
import whois as python_whois  # Import python-whois

app = Flask(__name__)

def is_tor_node(ip):
    response = requests.get(f'https://check.torproject.org/torbulkexitlist')
    tor_nodes = response.text.splitlines()
    return ip in tor_nodes

def is_valid_ip(ip):
    ip_pattern = re.compile(r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$')
    return ip_pattern.match(ip) is not None

def get_whois_info(ip):
    try:
        w = python_whois.whois(ip)
        if isinstance(w, dict):
            return w
        elif hasattr(w, '__dict__'):
            return w.__dict__
        else:
            return {}
    except Exception as e:
        return {}

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        ip = request.form['ip']
        if not is_valid_ip(ip):
            return jsonify({'error': 'Invalid IP address'}), 400
        result = is_tor_node(ip)
        whois_info = get_whois_info(ip)
        return render_template('index.html', result=result, ip=ip, whois_info=whois_info, dark_mode=True)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)