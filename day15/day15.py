import os

def print_cave_map(cave):
    for row in cave:
        for spot in row:
            print(spot, end='')
        print("")
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

    cave_map = [['.']]
    x_offset = 0
    y_offset = 0
    for line in f:
        parts = line.split(':')
        sensor_coord_strs = parts[0].strip().split(' ')
        beacon_coord_strs = parts[1].strip().split(' ')
        sensor_x = int(sensor_coord_strs[2].split('=')[1].strip(',')) + x_offset
        sensor_y = int(sensor_coord_strs[3].split('=')[1]) + y_offset

        beacon_x = int(beacon_coord_strs[4].split('=')[1].strip(',')) + x_offset
        beacon_y = int(beacon_coord_strs[5].split('=')[1]) + y_offset

        distance = abs(beacon_x - sensor_x) + abs(beacon_y - sensor_y)

        print("Sensor: {}, {} | Beacon: {}, {} | Distance: {}".format(sensor_x, sensor_y, beacon_x, beacon_y, distance))

        ### expand cave map as necessary ###
        ### add columns ###
        while sensor_x - distance < 0 or beacon_x < 0:
            for i in range(0, len(cave_map)):
                cave_map[i].insert(0, '.')
            x_offset += 1
            sensor_x += 1
            beacon_x += 1
        
        while (sensor_x + distance) > len(cave_map[0]) - 1 or beacon_x > len(cave_map[0]) - 1:
            for i in range(0, len(cave_map)):
                cave_map[i].append('.')

        ### add rows ###
        while sensor_y - distance < 0 or beacon_y < 0:
            new_row = []
            for i in range(0, len(cave_map[0])):
                new_row.append('.')
            cave_map.insert(0, new_row)
            y_offset += 1
            sensor_y += 1
            beacon_y += 1
        
        while (sensor_y + distance) > len(cave_map) - 1 or beacon_y > len(cave_map) - 1:
            new_row = []
            for i in range(0, len(cave_map[0])):
                new_row.append('.')
            cave_map.append(new_row)

        # print_cave_map(cave_map)
        print("Sensor: {}, {} | Beacon: {}, {} | Distance: {}".format(sensor_x, sensor_y, beacon_x, beacon_y, distance))
        cave_map[sensor_y][sensor_x] = 'S'
        cave_map[beacon_y][beacon_x] = 'B'

        ### carve out area around sensor ###
        start_y = sensor_y - distance
        y = start_y
        x = 0

        while y <= sensor_y:
            y = start_y + x # plus x because we're advancing downward (larger y)

            # raster across filling in the space with octothorpes
            for x_ind in range(0-x, x+1, 1):
                if cave_map[y][x_ind + sensor_x] == '.':
                    cave_map[y][x_ind + sensor_x] = '#'
            
            x += 1
        
        start_y = sensor_y + distance
        y = start_y
        x = 0
        while y > sensor_y:
            y = start_y - x

            # raster across filling in the space with octothorpes
            for x_ind in range(0-x, x+1, 1):
                if cave_map[y][x_ind + sensor_x] == '.':
                    cave_map[y][x_ind + sensor_x] = '#'
            
            x += 1
        print_cave_map(cave_map)
        input("ENTER")
    
    print("="*79)
    print_cave_map(cave_map)
    print("="*79)