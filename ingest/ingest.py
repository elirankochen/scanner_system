from flask import Flask
import redis
from flask import request

from ingest_logic import IngestLogic

app = Flask(__name__)
redis = redis.Redis(host='redis', port=6379)


@app.route('/add_consecutive_scans/', methods=['POST'])
def add_consecutive_scans():
    scan_id = IngestLogic.generate_scan_id()
    target_domain = request.form.get('target_domain')
    scan_services_id = request.form.get('scan_services_id')
    for scan_service_id in scan_services_id:
        IngestLogic.add_scan(scan_id, scan_service_id, target_domain)
    return scan_id, 200


@app.route('/add_scan/', methods=['POST'])
def add_scan():
    scan_id = IngestLogic.generate_scan_id()
    target_domain = request.form.get('target_domain')
    scan_service_id = request.form.get('scan_service_id')
    IngestLogic.add_scan(scan_id, scan_service_id, target_domain)
    return scan_id, 200


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)

