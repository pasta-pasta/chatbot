
def find_value(data, value):
    if isinstance(data, dict):
        if value in data:
            return data[value]
        else:
            for key, item in data.items():
                result = find_value(item, value)
                if result is not None:
                    return result