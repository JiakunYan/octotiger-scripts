import re
import sys

# filename = "run/slurm_output.default.n32-lci.j22470107.out"
filename = "run/debug.log"
pattern = r"^(\d):.+matchtable.+insert \((\S+), (\S+), (\S+)\),.* return (\d)"
def parse_tuple(line, pattern):
    match = re.search(pattern, line)
    if match:
        key = str(match.group(1)) + "-" + str(match.group(2))
        return key, int(match.group(4)), int(match.group(5))
    return None, None, None


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]

    print("Process file " + filename)

    with open(filename, "r") as file:
        lines = file.readlines()

    mt_map = dict()
    count = 0
    for line in lines:
        count += 1
        key, type, ret = parse_tuple(line, pattern)
        if key != None:
            if type == 1:
                if key in mt_map:
                    if (mt_map[key] < 0) != (ret == 0):
                        print("Error:", key, mt_map[key], type, ret)
                        print(count)
                        exit(1)
                    mt_map[key] += 1
                else:
                    mt_map[key] = 1
            else:
                if key in mt_map:
                    if (mt_map[key] > 0) != (ret == 0):
                        print("Error:", key, mt_map[key], type, ret)
                        print(count)
                        exit(1)
                    mt_map[key] -= 1
                else:
                    mt_map[key] = -1
            # print(key, mt_map[key], type, ret)
            if mt_map[key] == 0:
                mt_map.pop(key)

    print(count)
    print(mt_map)