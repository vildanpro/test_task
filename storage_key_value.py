import json
import os
import argparse
import tempfile


def check_storage_exists(file_path_check):
    if not os.path.isfile(file_path_check):
        try:
            with open(file_path_check, 'w') as f:
                json.dump({}, f)
        except Exception as e:
            exit(e)


def read_json_file(file_path_read):
    check_storage_exists(file_path_read)
    with open(file_path_read, 'r') as json_file:
        return json.load(json_file)


def write_json_file(file_path_write, json_data):
    check_storage_exists(file_path_write)
    with open(file_path_write, 'w') as json_file:
        json.dump(json_data, json_file)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-key", "--key", dest="key", help="Storage key")
    parser.add_argument("-val", "--val", dest="value", default=None, help="Storage value")
    return parser.parse_args()


class StorageData:
    def __init__(self, storage_file_name):
        self.storage_file_path = os.path.join(os.getcwd(), storage_file_name)
        self.args = get_args()
        self.data = read_json_file(self.storage_file_path)

    def get_values(self):
        return read_json_file(self.storage_file_path)

    def get_value(self, get_key):
        self.data = read_json_file(self.storage_file_path)
        val = self.data.get(get_key)
        if val:
            return ', '.join(val)

    def set_value(self, set_key, set_value):
        self.data = read_json_file(self.storage_file_path)
        if set_key in self.data.keys():
            self.data[set_key].append(set_value if set_value else 'None')
        else:
            self.data[set_key] = [set_value if set_value else 'None']
        write_json_file(self.storage_file_path, self.data)
        return {set_key: self.data[set_key]}


class StorageTempFile:
    def __init__(self):
        self.temp_file = tempfile.NamedTemporaryFile(mode='w+')
        self.temp_file.write(json.dumps({}))
        self.temp_file.flush()
        self.storage_file_path = self.temp_file.name

    def __del__(self):
        self.temp_file.close()

    def read_temp_file(self):
        self.temp_file.seek(0)
        return json.loads(self.temp_file.read())

    def get_values(self):
        return self.read_temp_file()

    def get_value(self, get_key):
        data = self.read_temp_file()
        val = data.get(get_key)
        if val:
            return ', '.join(val)

    def set_value(self, set_key, set_value):
        data = self.read_temp_file()
        print(data)
        if set_key in data.keys():
            data[set_key].append(set_value if set_value else 'None')
        else:
            data[set_key] = [set_value if set_value else 'None']
        self.temp_file.seek(0)
        self.temp_file.write(json.dumps(data))
        self.temp_file.flush()
        return {set_key: data[set_key]}


if __name__ == '__main__':
    storage = StorageData('storage.data')

    key = storage.args.key
    value = storage.args.value

    if key and value:
        storage.set_value(key, value)
    else:
        print(storage.get_value(key))
