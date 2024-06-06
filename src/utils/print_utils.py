def print_json_tree(data, depth=1, max_depth=2, indent=''):
    if depth > max_depth:
        return
    if isinstance(data, dict):
        for key, value in data.items():
            print(f"{indent}- {key}")
            if isinstance(value, (dict, list)):
                print_json_tree(value, depth+1, max_depth, indent + '  ')
    elif isinstance(data, list):
        for i, value in enumerate(data):
            print(f"{indent}- {i}")
            if isinstance(value, (dict, list)):
                print_json_tree(value, depth+1, max_depth, indent + '  ')