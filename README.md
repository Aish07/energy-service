# energy-service

## Project Setup

Clone the project from https://github.com/Aish07/energy-service.git

Required:
   
`python3 setup.py install`

`pip install -r requirements.txt`

Optional but preferred: 

Install [Advanced Rest Client](https://chrome.google.com/webstore/detail/advanced-rest-client/hgmloofddffdnphfgcellkdfbfbjeloo?hl=en-US) to access the endpoints.

## Project Execution

From the root folder, use the following command to run the app:

`python3 api.py`

The project is hosted on Heroku. Please use the below urls:

1. https://energy-service-temp.herokuapp.com/temp - POST
2. https://energy-service-temp.herokuapp.com/errors - GET, DELETE

Please note that a header 'Content-Type' with value 'application/json' will be required to call the above endpoints.


## Test Scenarios


## Problem Statement

The `POST` request at `/temp` should accept a JSON blob in the following format:
- `{"data": __data_string__}`
- where `__data_string__` is format:
    - `__device_id__:__epoch_ms__:'Temperature':__temperature__`
      - where `__device_id__` is the device ID (int32)
      - `__epoch_ms__` is the timestamp in EpochMS (int64)
      - `__temperature__` is the temperature (float64)
      - and `'Temperature'` is the exact string
- Example `{"data": "365951380:1640995229697:'Temperature':58.48256793121914"}`
  
Response:
- If for any reason the data string is not formatted correctly, return `{"error": "bad request"}` with a `400` status code
- If the temperature is at or over 90
  - return `{"overtemp": true, "device_id": __device_id__, "formatted_time": __formatted_time__}`,
    - where `__device_id__` is the device ID (int32)
    - and `__formatted_time__` is the timestamp formatted to `%Y/%m/%d %H:%M:%S`
  - otherwise return `{"overtemp": false}`

The `GET` request at `/errors` should return all data strings which have been incorrectly formatted. The response should 
be in the following format:
- `{"errors": [__error1__, __error2__] }`
  - Where `__errorX__` is the exact data string received

The `DELETE` request at `/errors` should clear the errors buffer.

