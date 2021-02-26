import redis
import json
import time

redis = redis.Redis(host='redis', port=6379)


class StatusEnum:
    ACCEPTED = {'order': 0, 'slug': 'Accepted',
                'description': 'the request for a new scan has been received and is pending processing'}
    RUNNING = {'order': 1, 'slug': 'Running', 'description': 'the scan is currently running'}
    ERROR = {'order': 2, 'slug': 'Error', 'description': 'an error occurred during the scan (e.g. bad domain name)'}
    COMPLETE = {'order': 3, 'slug': 'Complete', 'description': 'the scan was completed successfully'}
    NOT_FOUND = {'order': 4, 'slug': 'Not found', 'description': 'the scan-id could not be found'}


def process_scanner_requests():
    while True:
        first_scan_item = redis.lpop('scan_items')
        if first_scan_item:
            first_scan_object = json.loads(first_scan_item)
            redis.sadd('running_scans', first_scan_object['scan_id'])
            scanner_status = run_scanner(first_scan_object)
            time.sleep(5)
            redis.srem('running_scans', first_scan_object['scan_id'])
            save_scanner_status(first_scan_object, scanner_status)


def save_scanner_status(scan_item, status):
    redis.sadd('success_tasks', scan_item['scan_id']) if status == StatusEnum.COMPLETE \
        else redis.sadd('failed_tasks', scan_item['scan_id'])


def run_scanner(scan_item):
    return StatusEnum.ERROR if 'www' not in scan_item['target_domain'] else StatusEnum.COMPLETE


if __name__ == '__main__':
    process_scanner_requests()

