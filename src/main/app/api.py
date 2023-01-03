from flask import Flask, jsonify, request
from datetime import datetime
import numpy as np

app = Flask(__name__)

def write_error(data):
    err_file = open("errors.txt", "a")
    err_file.write(data + "\n")
    err_file.close()

@app.post('/temp')
def temperature():
    body = request.get_json()
    try:
        data = body['data']
        data = str(data)
        args = data.split(':')

        if not args or len(args) != 4:
            raise OverflowError()

        device_id, epoch_ms, label, temperature = args

        label = str(label).replace("'", "")
        if label != 'Temperature':
            raise ValueError()
        temperature = np.float64(temperature)
        device_id = np.int32(device_id)
        epoch_ms = np.int64(epoch_ms)

        if temperature >= 90:
            time_format = datetime.now()
            formatted_time = time_format.strftime("%Y/%m/%d %H:%M:%S")
            return jsonify({"overtemp": True, "device_id": int(device_id), "formatted_time": formatted_time})
        return jsonify({"overtemp": False})

    except ValueError as e:
        write_error(data)
        return jsonify({'error': 'bad request'}), 400

    except TypeError as e:
        write_error(data)
        return jsonify({'error': 'bad request'}), 400

    except IndexError as e:
        write_error(data)
        return jsonify({'error': 'bad request'}), 400

    except KeyError as e:
        write_error(data)
        return jsonify({'error': 'bad request'}), 400

    except OverflowError as e:
        write_error(data)
        return jsonify({'error': 'bad request'}), 400

    except BufferError as e:
        write_error(data)
        return jsonify({'error': 'bad request'}), 400


@app.get('/errors')
def get_errors():
    with open('errors.txt', 'r') as input_file:
        contents = input_file.read()
        lines = contents.split('\n')
        lines.pop()
    return jsonify({"errors":  lines})


@app.delete('/errors')
def delete_errors():
    with open('errors.txt', 'r+') as file:
        file.truncate()
    return jsonify({"msg": "buffered cleared"})



if __name__ == '__main__':
    app.run(debug=True)
