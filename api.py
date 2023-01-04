from flask import Flask, jsonify, request
from datetime import datetime
import numpy as np

app = Flask(__name__)

def write_error(data):
    err_file = open("errors.txt", "a")
    err_file.write(data + "\n")
    err_file.close()


'''
Checks if the input string has temperature >= 90, then the api returns a JSON consisting of deviceId, time, overtemp = true.
If the temperature < 90, then the response is overtemp = false.
Returns 400 Bad Request if input string is not formatted correctly.
'''
@app.post('/temp')
def validate_temperature():
    body = request.get_json()
    try:
        data = body['data']
        data = str(data)
        args = data.split(':')

        #checking if the input string is valid
        if not args or len(args) != 4:
            raise OverflowError()

        device_id, epoch_ms, label, temperature = args

        label = str(label).replace("'", "")
        if label != 'Temperature':
            raise ValueError()
        temperature = np.float64(temperature)
        device_id = np.int32(device_id)

        if temperature >= 90:
            time_format = datetime.now()
            #formatting time as per the requirements
            formatted_time = time_format.strftime("%Y/%m/%d %H:%M:%S")
            return jsonify({"overtemp": True, "device_id": int(device_id), "formatted_time": formatted_time})
        #if temperature < 90
        return jsonify({"overtemp": False})
    #handling different types of exceptions and returning 400 Bad Request error
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


'''
returns all data strings which have been incorrectly formatted
'''
@app.get('/errors')
def read_errors():
    with open('errors.txt', 'r') as input_file:
        contents = input_file.read()
        lines = contents.split('\n')
        lines.pop()
    return jsonify({"errors":  lines})


'''
clears the errors buffer
'''
@app.delete('/errors')
def delete_errors():
    with open('errors.txt', 'r+') as file:
        file.truncate()
    return jsonify({"msg": "Error buffer cleared."})



if __name__ == '__main__':
    app.run(debug=True)
