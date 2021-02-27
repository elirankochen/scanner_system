import redis
import json
import time

redis = redis.Redis(host='redis', port=6379)


def process_scanner_requests():
    while True:
        first_scan_item = redis.lpop('scan_items')
        if first_scan_item:
            first_scan_object = json.loads(first_scan_item)
            redis.sadd('running_scans', first_scan_object['scan_id'])
            status_succeeded = run_scanner(first_scan_object)
            time.sleep(5)
            redis.srem('running_scans', first_scan_object['scan_id'])
            save_scanner_status(first_scan_object, status_succeeded)


def save_scanner_status(scan_item, status_succeeded):
    redis.sadd('success_tasks', scan_item['scan_id']) if status_succeeded\
        else redis.sadd('failed_tasks', scan_item['scan_id'])


def run_scanner(scan_item):
    #run scanner will identify if it is a consecutive scans according to scan_services_id
    #first runs the validators, in this case only them(1)
    #after validators succeeded run the actual scan test
    return 'www' in scan_item['target_domain']


if __name__ == '__main__':
    process_scanner_requests()
