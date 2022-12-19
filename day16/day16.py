import os
import queue
import copy

#-----------------------------------------------------------------------------
def find_max_valve(valves, curr_valve):
    max_valve = valves[curr_valve]['valve_list'][0]
    max_flow = 0
    for valve in valves[curr_valve]['valve_list']:
        if not valves[valve]['is_open'] and valves[valve]['flow_rate'] > max_flow:
            max_valve = valve
            max_flow = valves[valve]['flow_rate']
    
    return max_valve

#-----------------------------------------------------------------------------
def find_paths_to_dest(valves: dict, path: list, paths: list, dest: str):
# def find_path_to_dest(valves: dict, start_valve: str, path: list, paths: list, dest: str):
    # print("Path = ", path)
    curr_valve = path[-1]

    opts = valves[curr_valve]['valve_list']

    if dest in opts:# == dest:
        # print("Path to dest. {} = {}".format(dest, path))
        new_path = copy.deepcopy(path)
        new_path.append(dest)
        paths.append(new_path)
    else:
        if len(opts) == 1:
            path.append(opts[0])
            print("Path to dest. {} = {}".format(dest, path))
            paths.append(copy.deepcopy(path))
        else:
            for opt in opts:
                if opt != path[0] and opt != curr_valve:
                    # path.append(opt)
                    new_path = copy.deepcopy(path)
                    new_path.append(opt)
                    find_paths_to_dest(valves, new_path, paths, dest)
                    paths.append(new_path)
    
#-----------------------------------------------------------------------------
def find_best_path(valves, curr_valve, target_valve):
    path = []
    valve = target_valve
    last_valve = ''
    iter_count = 0
    while valve != curr_valve:
        opts = valves[valve]['valve_list']
        for opt in opts:
            if opt == curr_valve:
                valve = opt
                break
            elif opt != last_valve:
                path.insert(0, opt)
                last_valve = valve
                valve = opt
                break
    return path
#-----------------------------------------------------------------------------
if __name__ == "__main__":
    file_list = os.listdir()
    for i in range(0, len(file_list)):
        print("{}\t{}".format(i, file_list[i]))

    try:
        fname = file_list[int(input("Line Number: "))]
    except IndexError or ValueError:
        fname = "sensors.txt"

    f = open(fname, 'r')

    valves = {}
    nonzero_valves = []
    for line in f:
        parts = line.strip().split(';')
        valve_id = parts[0].split(' ')[1]
        flow_rate = int(parts[0].split('=')[1])
        valve_list = []
        second_part_words = parts[1].strip().split(' ')
        for i in range(4, len(second_part_words)):
            valve_list.append(second_part_words[i].strip(','))
        valves[valve_id] = {}
        valves[valve_id]['flow_rate'] = flow_rate
        valves[valve_id]['valve_list'] = valve_list
        valves[valve_id]['is_open'] = False
        if flow_rate > 0:
            nonzero_valves.append(valve_id)
    
    for valve in valves.keys():
        flow = valves[valve]['flow_rate']
        l = valves[valve]['valve_list']
        print("Valve {}: flow_rate={:d}, Leads to {}".format(valve, flow, l))
    
    curr_valve = 'AA'

    minute = 0
    total_release = 0
    
    for dest in nonzero_valves:
        paths = []
        find_paths_to_dest(valves, ['AA'], paths, dest)
        for path in paths:
            print("Possible path to {} = {}".format(dest, path))
    
    """
    while minute < 30:
        minute += 1
        print("\n== Minute {} ==".format(minute))
        valves_open = []
        for id in valves.keys():
            if valves[id]['is_open']:
                valves_open.append(id)
        release = 0
        if len(valves_open) < 1:
            print("No valves are open.")
        else:
            print("Valves open: {}".format(valves_open))
            for valve in valves_open:
                release += valves[valve]['flow_rate']
            print("{} pressure released.".format(release))
        
        total_release += release

        if valves[curr_valve]['is_open'] or valves[curr_valve]['flow_rate'] == 0:
            best_move = ''
            shortest_path = 1000
            for target in nonzero_valves:
                path = find_best_path(valves, curr_valve, target)
                if len(path) < shortest_path:
                    shortest_path = len(path)
                    best_move = path[0]
            curr_valve = best_move
            print("Moving to valve {}.".format(curr_valve))
        else:
            # open current valve
            print("Opening valve {}...".format(curr_valve))
            valves[curr_valve]['is_open'] = True
        # choose to move or open this valve during this minute
        # if valves[curr_valve]['is_open'] or valves[curr_valve]['flow_rate'] == 0:
        #     # time to move
        #     curr_valve = find_max_valve(valves, curr_valve)
        #     print("Moving to valve {}.".format(curr_valve))
        # else:
        #     if not valves[curr_valve]['is_open']:
        #         # consider moving to another better valve rather than spending a minute opening this valve
        #         max_valve = find_max_valve(valves, curr_valve)
        #         if valves[max_valve]['flow_rate'] >= 2*valves[curr_valve]['flow_rate']:
        #             curr_valve = max_valve
        #             print("Moving to valve {}.".format(curr_valve))
        #         else:
        #             # open current valve
        #             print("Opening valve {}...".format(curr_valve))
        #             valves[curr_valve]['is_open'] = True
        #     else:
        #         # open current valve
        #         print("Opening valve {}...".format(curr_valve))
        #         valves[curr_valve]['is_open'] = True
    """
    # print("\n=== SUMMARY ===")
    # print("We released {} pressure units.".format(total_release))