api = "https://db.satnogs.org/api/"
observations = 'observations/'
satellites = "satellites/"
telemetry = "telemetry/?"
web_address = "https://network.satnogs.org/"

keys = dict()
with open("../keys.txt", 'r') as file_in:
    keys['api'] = file_in.readline().strip()
    keys['cookie'] = file_in.readline().strip()
    keys['token'] = file_in.readline().strip()

observation_template = {
    'Observation_id': None,
    'Satellite': None,
    'Station': None,
    'Status': None,
    'Status_Message': None,
    'Transmitter': None,
    'Frequency': None,
    'Mode': None,
    'Metadata': None,
    'Downloads': None,
    'Waterfall_Status': None,
}

directories = {
    "data": "../data",
    "satellites": "../data/satellites/",
    "satellites_json": "../data/satellites/satellites.json",
    "satellites_csv": "../data/satellites/satellites.csv",
    "tm_events":  "../data/telemetry_events/",
    "tm_compiled": "../data/telemetry_compiled/",
    "tm_compiled_json": "../data/telemetry_compiled/events.json",
    "tm_compiled_csv": "../data/telemetry_compiled/events.csv",
    "observations": "../data/observations/",
    "waterfalls": "../data/observations/waterfalls/",
    "observation_json": "../data/observations/observations.json",
    "observation_csv": "../data/observations/observations.csv",
    "logs": "../data/logs/",
    "log_file": "../data/logs/log.txt",
    "combined_csv": "../data/combined.csv"
}

if __name__ == '__main__':
    print(f'api = {api}')
    print(f'observation = {observations}')
    print(f'satellites = {satellites}')
    print(f'telemetry = {telemetry}')
    print(f'web_address = {web_address}')
    print(f'keys = {keys}')
    print(f'observation_template: {observation_template}')
