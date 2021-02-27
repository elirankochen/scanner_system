import requests
import json
from time import time, sleep

INGEST_LOCALHOST = 'http://localhost'
STATUS_LOCALHOST = 'http://localhost:5002'

def get_mock_scanner_targets():
    return [{'target_domain':'www.google.com', 'scan_service_id': 1},
            {'target_domain':'www.google.com', 'scan_service_id': 2},
            {'target_domain':'www.google.com', 'scan_service_id': 3},
            {'target_domain':'www.google.com', 'scan_service_id': 4},
            {'target_domain':'www.google.com', 'scan_service_id': 5},
            {'target_domain':'w.google.com', 'scan_service_id': 1},
            {'target_domain':'w.google.com', 'scan_service_id': 2},
            {'target_domain':'w.google.com', 'scan_service_id': 3},
            {'target_domain':'w.google.com', 'scan_service_id': 4},
            {'target_domain':'w.google.com', 'scan_service_id': 5}]

def get_mock_consecutive_scans():
    return [{'target_domain':'www.google.com', 'scan_services_id': [1, 2, 3, 4, 5]}]

def init_consecutive_scans():
    scans_id = []
    for bulk_scanners in get_mock_consecutive_scans():
        response = requests.post(f'{INGEST_LOCALHOST}/add_consecutive_scans/', data=bulk_scanners)
        scans_id.append(str(response.content, 'utf-8'))
    return scans_id

def init_scanner_system():
    scans_id = []
    for scanner_target in get_mock_scanner_targets():
        response = requests.post(f'{INGEST_LOCALHOST}/add_scan/', data=scanner_target)
        scans_id.append(str(response.content, 'utf-8'))
    return scans_id

def get_scans_status(scans_id):
    for scan_id in scans_id:
        response = requests.get(f'{STATUS_LOCALHOST}/scan_status/{scan_id}')
        print(f'scan_id- {scan_id} status - {json.loads(response.content)["slug"]}')


if __name__ == '__main__':
scans_id_for_status = init_scanner_system()
while True:
    sleep(5 - time() % 5)
    get_scans_status(scans_id_for_status)
    print('----------------------------------------------------------')
