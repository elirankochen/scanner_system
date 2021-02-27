import redis

redis = redis.Redis(host='redis', port=6379)


class ProcessLogic:
    @staticmethod
    def save_scanner_status(scan_item, status_succeeded):
        redis.sadd('success_tasks', scan_item['scan_id']) if status_succeeded \
            else redis.sadd('failed_tasks', scan_item['scan_id'])
    @staticmethod
    def run_scanner(scan_item):
        # run scanner will identify if it is a consecutive scans according to scan_services_id
        # first runs the validators, in this case only them(1)
        # after validators succeeded run the actual scan test
        return 'www' in scan_item['target_domain']
