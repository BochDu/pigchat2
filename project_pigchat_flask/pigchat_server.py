from flask import Flask, request, jsonify
import core_pigchat
import core_pigtime

app = Flask(__name__)

@app.route('/get_pig_timestamp', methods=['GET'])
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

        result = core_pigtime.get_pig_timestamp(year, month, day)
        return jsonify({"pig_timestamp": result})
    except ValueError:
        return jsonify({"error": "Year, month, and day must be valid integers."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/utf8_to_emoji', methods=['POST'])
def convert_utf8_to_emoji():
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"error": "No JSON data provided"}), 400

        utf8_str = data.get('utf8_str')
        timestamp_str = data.get('timestamp')
        password = data.get('password')

        if utf8_str is None or timestamp_str is None or password is None:
            return jsonify({"error": "Missing required parameters"}), 400

        try:
            timestamp = int(timestamp_str)
        except (ValueError, TypeError):
            return jsonify({"error": "Timestamp must be an integer"}), 400

        result = core_pigchat.utf8_to_emoji(utf8_str, timestamp, password)
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/emoji_to_utf8', methods=['POST'])
def convert_emoji_to_utf8():
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"error": "No JSON data provided"}), 400

        emoji_str = data.get('emoji_str')
        timestamp_str = data.get('timestamp')
        password = data.get('password')

        if emoji_str is None or timestamp_str is None or password is None:
            return jsonify({"error": "Missing required parameters"}), 400

        try:
            timestamp = int(timestamp_str)
        except (ValueError, TypeError):
            return jsonify({"error": "Timestamp must be an integer"}), 400

        result = core_pigchat.emoji_to_utf8(emoji_str, timestamp, password)
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)