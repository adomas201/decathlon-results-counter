'''

This application counts full score of every decathlon
participator and writes final table with places to
chosen file

'''

# formula to count track event points
def track_event_points(A, B, C, P):
    return int(A * ((B - P) ** C))

# formula to count field event points
def field_event_points(A, B, C, P):
    return int(A * ((P - B) ** C))

# converts metres to centimetres
def metres_cm(metres):
    return metres * 100

# converts minutes with seconds to only seconds
def minutes_sec(time):
    minutes = time.partition(":")[0]
    seconds = time.partition(":")[2]
    time = int(minutes) * 60
    time = time + float(seconds)
    return time

# function choose constants for formula to count points
def points_data(P, event):
    if event == 0: # 100m running
        a = 25.4347
        b = 18
        c = 1.81
        return track_event_points(a, b, c, P)
    elif event == 5: # 100m hurdles
        a = 5.74352
        b = 28.5
        c = 1.92
        return track_event_points(a, b, c, P)
    elif event == 9: # 1500m
        a = 0.03768
        b = 480
        c = 1.85
        P = minutes_sec(P) # converts minutes to seconds for formula
        return track_event_points(a, b, c, P)
    elif event == 4: # 400m
        a = 1.53775
        b = 82
        c = 1.81
        return track_event_points(a, b, c, P)
    elif event == 6: # Discus throw
        a = 12.91
        b = 4
        c = 1.1
        return field_event_points(a, b, c, P)
    elif event == 3: # High jump
        a = 0.8465
        b = 75
        c = 1.42
        P = metres_cm(P) # converts metres to centimetres for formula as needed for all jumping events
        return field_event_points(a, b, c, P)
    elif event == 8: # javelin throw
        a = 10.14
        b = 7
        c = 1.08
        return field_event_points(a, b, c, P)
    elif event == 1: # long jump
        a = 0.14354
        b = 220
        c = 1.4
        P = metres_cm(P)
        return field_event_points(a, b, c, P)
    elif event == 7: # pole vault
        a = 0.2797
        b = 100
        c = 1.35
        P = metres_cm(P)
        return field_event_points(a, b, c, P)
    elif event == 2: # shot put
        a = 51.39
        b = 1.5
        c = 1.05
        return field_event_points(a, b, c, P)

# athlete class, with every event points, results and place
class Athlete:
    def __init__(self, name, hundred, long_jump, shot, high_jump, four_hundreds, hurdles, discus, pole, javelin, kilo_five):
        self.name = name
        self.hundred = hundred
        self.hurdles = hurdles
        self.kilo_five = kilo_five
        self.four_hundreds = four_hundreds
        self.discus = discus
        self.high_jump = high_jump
        self.javelin = javelin
        self.long_jump = long_jump
        self.pole = pole
        self.shot = shot
        self.result = 0
        self.place = 0

# function to count all points from every event
    def count_points(self, hundred, long_jump, shot, high_jump, four_hundreds, hurdles, discus, pole, javelin, kilo_five):
        results = 0
        results = results + points_data(float(hundred), 0)
        results = results + points_data(float(long_jump), 1)
        results = results + points_data(float(shot), 2)
        results = results + points_data(float(high_jump), 3)
        results = results + points_data(float(four_hundreds), 4)
        results = results + points_data(float(hurdles), 5)
        results = results + points_data(float(discus), 6)
        results = results + points_data(float(pole), 7)
        results = results + points_data(float(javelin), 8)
        results = results + points_data(kilo_five, 9)
        self.result = results

# function that gives athlete specific place
    def give_place(self, place):
        self.place = place

# read and add info to athletes array
def read_athletes_info(file_name):
    global athletes # used not only in this function
    global athletes_number
    data_file = open(file_name, "r")
    athletes_number = data_file.readline()
    for athl in range(int(athletes_number)):
        info = data_file.readline()
        info = info.split('\t')
        athletes.append(Athlete(info[0],info[1],info[2],info[3],info[4],info[5],info[6],info[7],info[8],info[9],info[10]))
        athletes[athl].count_points(info[1],info[2],info[3],info[4],info[5],info[6],info[7],info[8],info[9],info[10])
    data_file.close()

# sort athletes from winner to the last
def find_winner(athletes):
    for x in range((int(athletes_number)) - 1):
        for y in range(x, int(athletes_number)):
            if athletes[y].result > athletes[x].result:
                temp = athletes[x]
                athletes[x] = athletes[y]
                athletes[y] = temp

# gives athletes specific places
def give_places(athletes):
    skip = 0
    same_places = 0
    for x in range(int(athletes_number)): # if there are similar results, skip these athletes
        if (skip > 0):
            skip = skip - 1
            continue

        if (same_places == 0): # if there are no similar results, give athlete his place
            for y in range(x + 1, int(athletes_number)):
                if (athletes[x].result == athletes[y].result):
                    same_places = same_places + 1
            if (same_places == 0):
                athletes[x].give_place(str(x + 1))

        if (same_places > 0): # if there are some similar results, give athletes these places and later skip these athletes
            for same in range(0, same_places + 1):
                new_index = x + same
                place_string = str(x + 1) + "-" + str(same_places + x + 1)
                athletes[new_index].give_place(str(place_string))
            skip = same_places
            same_places = 0

# write results table to txt file
def write_file(athletes, file_name):
    file = open(file_name, "w+")
    file.write(" Place |      name      |score| 100m |long jump| shot |high jump| 400m |100m hurdles|discus throw|pole throw|javelin throw|  1.5km  |" + "\n" + "\n ")
    for x in range(int(athletes_number)):
        file.write(' {:6} {:15}  {:5} {:6}   {:7} {:6}   {:7} {:6}    {:9}    {:9}   {:8}    {:10} {:9}'.format(str(athletes[x].place),
                                                                                    str(athletes[x].name),
                                                                                    str(athletes[x].result),
                                                                                    str(athletes[x].hundred),
                                                                                    str(athletes[x].long_jump),
                                                                                    str(athletes[x].shot),
                                                                                    str(athletes[x].high_jump),
                                                                                    str(athletes[x].four_hundreds),
                                                                                    str(athletes[x].hurdles),
                                                                                    str(athletes[x].discus),
                                                                                    str(athletes[x].pole),
                                                                                    str(athletes[x].javelin),
                                                                                    str(athletes[x].kilo_five)
                                                                                    ))
    file.close()


# if application launched standalone
if __name__ == "__main__":
    athletes_number = 0
    athletes = []
    read_athletes_info('athletes.txt')
    find_winner(athletes)
    give_places(athletes)
    write_file(athletes, 'results.txt')