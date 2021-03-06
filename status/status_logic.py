import json
import redis

redis = redis.Redis(host='redis', port=6379)


class StatusEnum:
    ACCEPTED = {'order': 0, 'slug': 'Accepted',
                'description': 'the request for a new scan has been received and is pending processing'}
    RUNNING = {'order': 1, 'slug': 'Running', 'description': 'the scan is currently running'}
    ERROR = {'order': 2, 'slug': 'Error', 'description': 'an error occurred during the scan (e.g. bad domain name)'}
    COMPLETE = {'order': 3, 'slug': 'Complete', 'description': 'the scan was completed successfully'}
    NOT_FOUND = {'order': 4, 'slug': 'Not found', 'description': 'the scan-id could not be found'}

    @staticmethod
    def get_statuses():
        return [StatusEnum.ACCEPTED, StatusEnum.RUNNING, StatusEnum.ERROR, StatusEnum.COMPLETE,
                StatusEnum.NOT_FOUND]


class StatusLogic:
    @staticmethod
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

        return status

