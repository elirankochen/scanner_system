import redis
import json
import time
from process_logic import ProcessLogic
redis = redis.Redis(host='redis', port=6379)


def process_scanner_requests():
    while True:
        first_scan_item = redis.lpop('scan_items')
        if first_scan_item:
            first_scan_object = json.loads(first_scan_item)
            redis.sadd('running_scans', first_scan_object['scan_id'])
            status_succeeded = ProcessLogic.run_scanner(first_scan_object)
            time.sleep(5)
            redis.srem('running_scans', first_scan_object['scan_id'])
            ProcessLogic.save_scanner_status(first_scan_object, status_succeeded)


if __name__ == '__main__':
    process_scanner_requests()
