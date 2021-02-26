from flask import Flask
import redis
import uuid
import json
from flask import request

app = Flask(__name__)
redis = redis.Redis(host='redis', port=6379)


class StatusEnum:
    ACCEPTED = {'order': 0, 'slug': 'Accepted',
                'description': 'the request for a new scan has been received and is pending processing'}
    RUNNING = {'order': 1, 'slug': 'Running', 'description': 'the scan is currently running'}
    ERROR = {'order': 2, 'slug': 'Error', 'description': 'an error occurred during the scan (e.g. bad domain name)'}
    COMPLETE = {'order': 3, 'slug': 'Complete', 'description': 'the scan was completed successfully'}
    NOT_FOUND = {'order': 4, 'slug': 'Not found', 'description': 'the scan-id could not be found'}


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


@app.route('/add_scan/', methods=['POST'])
def add_scan():
    scan_id = str(uuid.uuid4())
    target_domain = request.form.get('target_domain')
    scan_service_id = request.form.get('scan_service_id')
    scan_item = {'scan_id': scan_id, 'scan_service_id': scan_service_id, 'target_domain': target_domain}
    redis.rpush('scan_items', json.dumps(scan_item))
    return scan_item, 200


@app.route('/scan_status/<scan_id>', methods=['GET'])
def get_scan_status(scan_id):
    status = None
    pending_scans_items = redis.lrange('scan_items', 0, -1)
    pending_scans_ids = [json.loads(scan_item)['scan_id'] for scan_item in pending_scans_items]

    if scan_id in pending_scans_ids:
        status = StatusEnum.ACCEPTED

    elif redis.sismember('running_scans', scan_id):
        status = StatusEnum.RUNNING

    elif redis.sismember('success_tasks', scan_id):
        status = StatusEnum.COMPLETE

    elif redis.sismember('failed_tasks', scan_id):
        status = StatusEnum.ERROR

    if not status:
        status = StatusEnum.NOT_FOUND

    return status, 200


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)

