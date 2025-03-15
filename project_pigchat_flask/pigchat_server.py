import sys
import os
import traceback
from flask import Flask, request, jsonify

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from core import pigchat
from core import pigtime

app = Flask(__name__)
# app.config['MODE'] = "shadow"
app.config['MODE'] = "emoji"
app.config['STRATEGY'] = "capacity"


@app.route('/pigtime', methods=['GET'])
def api_get_pig_timestamp():
    try:
        year = request.args.get('year')
        month = request.args.get('month')
        day = request.args.get('day')

        if year:
            year = int(year)
        if month:
            month = int(month)
        if day:
            day = int(day)

        result = pigtime.get_pig_timestamp(year, month, day)
        return jsonify({"pigtime": result})
    except ValueError:
        return jsonify({"error": "Year, month, and day must be valid integers."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/duplex', methods=['POST'])
def convert_utf8_to_emoji():
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"error": "No JSON data provided"}), 400

        input_str = data.get('input_str')
        timestamp_str = data.get('timestamp')
        password = data.get('password')

        if input_str is None or timestamp_str is None:
            return jsonify({"error": "Missing required parameters"}), 400

        try:
            timestamp = int(timestamp_str)
        except (ValueError, TypeError):
            return jsonify({"error": "Timestamp must be an integer"}), 400

        if password is None:
            password = ''

        result = pigchat.duplex_convert(input_str, timestamp, password, strategy=app.config['STRATEGY'], mode=app.config['MODE'])
        return jsonify({"result": result})
    except Exception as e:
        traceback.print_exception(e)
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)
