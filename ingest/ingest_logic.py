import uuid
import json
import redis

redis = redis.Redis(host='redis', port=6379)


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
