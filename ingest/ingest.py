from flask import Flask
import redis
import uuid
import json
from flask import request

app = Flask(__name__)
redis = redis.Redis(host='redis', port=6379)


@app.route('/delete_items_redis')
def delete_items_redis():
    redis.delete('scan_items')
    redis.delete('running_scans')
    redis.delete('success_tasks')
    redis.delete('failed_tasks')
    return str(redis.lrange('scan_items', 0, -1)), 200


@app.route('/get_items_redis')
def get_items():
    items = redis.lrange('scan_items', 0, -1)
    return str(len(items)), 200


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


class IngestLogic:

    @staticmethod
    def add_scan(scan_id, scan_service_id, target_domain):
        scan_item = {'scan_id': scan_id, 'scan_service_id': scan_service_id, 'target_domain': target_domain}
        redis.rpush('scan_items', json.dumps(scan_item))

    def delete_scan(self):
        pass

    @staticmethod
    def generate_scan_id():
        return str(uuid.uuid4())


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)

