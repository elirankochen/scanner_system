from flask import Flask

from status_logic import StatusLogic

app = Flask(__name__)


@app.route('/scan_status/<scan_id>', methods=['GET'])
def get_scan_status(scan_id):
    status = StatusLogic.get_scan_status(scan_id)
    return status, 200


if __name__ == '__main__':
    app.run('0.0.0.0', port=5002, debug=True)

