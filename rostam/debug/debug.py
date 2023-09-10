import re
import sys

filename = "debug/full4.log"
pattern_send_start = r"send connection \((\d+), (\d+), (\d+).* start!"
pattern_send_done = r"send connection \((\d+), (\d+), (\d+).* done!"
pattern_recv_start = r"recv connection \((\d+), (\d+), (\d+).* start!"
pattern_recv_done = r"recv connection \((\d+), (\d+), (\d+).* done!"

def parse_tuple(line, pattern):
    match = re.search(pattern, line)
    if match:
        tuple = (int(match.group(1)), int(match.group(2)), int(match.group(3)))
        return tuple
    return None


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]

    print("Process file " + filename)

    with open(filename, "r") as file:
        lines = file.readlines()

    send_map = dict()
    recv_map = dict()
    count = 0
    for line in lines:
        count += 1
        tuple = parse_tuple(line, pattern_send_start)
        if tuple != None:
            if tuple in send_map:
                send_map[tuple] += 1
            else:
                send_map[tuple] = 1
            continue
        tuple = parse_tuple(line, pattern_send_done)
        if tuple != None:
            if not tuple in send_map:
                print("Unexpected send done %s!", tuple)
                exit(1)
                send_map[tuple] = -1
            else:
                if send_map[tuple] == 1:
                    send_map.pop(tuple)
                else:
                    send_map[tuple] -= 1
            continue

        tuple = parse_tuple(line, pattern_recv_start)
        if tuple != None:
            if tuple in recv_map:
                recv_map[tuple] += 1
            else:
                recv_map[tuple] = 1
            continue
        tuple = parse_tuple(line, pattern_recv_done)
        if tuple != None:
            if not tuple in recv_map:
                print("Unexpected recv done %s!", tuple)
                exit(1)
                recv_map[tuple] = -1
            else:
                if recv_map[tuple] == 1:
                    recv_map.pop(tuple)
                else:
                    recv_map[tuple] -= 1
            continue

    print("Send")
    print(send_map)
    print("Recv")
    print(recv_map)