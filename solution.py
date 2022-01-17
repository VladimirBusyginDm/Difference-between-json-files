import json


def compare(obj_1: list or dict, obj_2: list or dict, obj_diff: dict, path: str, flag: bool, index=0) -> None:
    if isinstance(obj_1, list) and isinstance(obj_2, list):
        compare_list(obj_1, obj_2, obj_diff, path, index)

    elif isinstance(obj_1, dict) and isinstance(obj_2, dict):
        compare_dict(obj_1, obj_2, obj_diff, path)

    elif type(obj_1) != type(obj_2) or (obj_1 != obj_2):
        obj_diff[path + str(index)] = obj_1
        if not flag:
            obj_diff[path + str(index + 1)] = obj_2


def compare_dict(obj_1, obj_2, obj_diff, path) -> None:
    for key in obj_1:
        if key in obj_2:
            if isinstance(obj_1[key], dict) and isinstance(obj_2[key], dict):
                compare(obj_1[key], obj_2[key], obj_diff, path + key + '->', False)  # '->' - обозначение к словарю
            elif isinstance(obj_1[key], list) and isinstance(obj_2[key], list):
                compare(obj_1[key], obj_2[key], obj_diff, path + key + '.', False)  # '.' - обозначение к массиву
            elif type(obj_1) != type(obj_2) or obj_1[key] != obj_2[key]:
                obj_diff[path + key] = obj_1[key]
        else:
            obj_diff[path + key] = obj_1[key]


def compare_list(obj_1, obj_2, obj_diff, path, index) -> None:
    length_compare = len(obj_1) == len(obj_2)
    for i in range(min(len(obj_1), len(obj_2))):
        compare(obj_1[i], obj_2[i], obj_diff, path, length_compare, index)
    if len(obj_1) > len(obj_2):
        for i in range(len(obj_2), len(obj_1)):
            obj_diff[path + '[' + str(i) + ']'] = obj_1[i]


def main() -> None:
    print('Input path to file1.json :')
    path_to_file1 = input()

    print('Input path to file2.json :')
    path_to_file2 = input()

    with open(path_to_file1) as f1:
        data_1 = json.load(f1)

    with open(path_to_file2) as f2:
        data_2 = json.load(f2)

    result = {}
    compare(data_1, data_2, result, '[file-1] ', False)
    compare(data_2, data_1, result, '[file-2] ', False)

    print('Write results in console(-c) or file(-f)?')
    answer = input()
    if answer == '-c':
        print(json.dumps(result, indent=4))
    else:
        print('Input path to output file :')
        path_to_output_file = input()
        with open(path_to_output_file, 'w') as output:
            json.dump(result, output, indent=4)


if __name__ == '__main__':
    main()