# --- Day 16: Proboscidea Volcanium ---
# The sensors have led you to the origin of the distress signal: yet another handheld device, 
# just like the one the Elves gave you. However, you don't see any Elves around; instead, the device is surrounded by elephants! 
# They must have gotten lost in these tunnels, and one of the elephants apparently figured out how to turn on the distress signal.

# The ground rumbles again, much stronger this time. What kind of cave is this, exactly? You scan the cave with your handheld device; 
# it reports mostly igneous rock, some ash, pockets of pressurized gas, magma... this isn't just a cave, it's a volcano!

# You need to get the elephants out of here, quickly. Your device estimates that you have 30 minutes before the volcano erupts, 
# so you don't have time to go back out the way you came in.

# You scan the cave for other options and discover a network of pipes and pressure-release valves. 
# You aren't sure how such a system got into a volcano, but you don't have time to complain; your device produces a report (your puzzle input) 
# of each valve's flow rate if it were opened (in pressure per minute) and the tunnels you could use to move between the valves.

# There's even a valve in the room you and the elephants are currently standing in labeled AA. 
# You estimate it will take you one minute to open a single valve and one minute to follow any tunnel from one valve to another. 
# What is the most pressure you could release?

# For example, suppose you had the following scan output:

# Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
# Valve BB has flow rate=13; tunnels lead to valves CC, AA
# Valve CC has flow rate=2; tunnels lead to valves DD, BB
# Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
# Valve EE has flow rate=3; tunnels lead to valves FF, DD
# Valve FF has flow rate=0; tunnels lead to valves EE, GG
# Valve GG has flow rate=0; tunnels lead to valves FF, HH
# Valve HH has flow rate=22; tunnel leads to valve GG
# Valve II has flow rate=0; tunnels lead to valves AA, JJ
# Valve JJ has flow rate=21; tunnel leads to valve II
# All of the valves begin closed. You start at valve AA, but it must be damaged or jammed or something: 
# its flow rate is 0, so there's no point in opening it. However, you could spend one minute moving to valve BB and another minute opening it; 
# doing so would release pressure during the remaining 28 minutes at a flow rate of 13, a total eventual pressure release of 28 * 13 = 364. 
# Then, you could spend your third minute moving to valve CC and your fourth minute opening it, providing an additional 26 minutes of eventual 
# pressure release at a flow rate of 2, or 52 total pressure released by valve CC.

# Making your way through the tunnels like this, you could probably open many or all of the valves by the time 30 minutes have elapsed. 
# However, you need to release as much pressure as possible, so you'll need to be methodical. Instead, consider this approach:

# == Minute 1 ==
# No valves are open.
# You move to valve DD.

# == Minute 2 ==
# No valves are open.
# You open valve DD.

# == Minute 3 ==
# Valve DD is open, releasing 20 pressure.
# You move to valve CC.

# == Minute 4 ==
# Valve DD is open, releasing 20 pressure.
# You move to valve BB.

# == Minute 5 ==
# Valve DD is open, releasing 20 pressure.
# You open valve BB.

# == Minute 6 ==
# Valves BB and DD are open, releasing 33 pressure.
# You move to valve AA.

# == Minute 7 ==
# Valves BB and DD are open, releasing 33 pressure.
# You move to valve II.

# == Minute 8 ==
# Valves BB and DD are open, releasing 33 pressure.
# You move to valve JJ.

# == Minute 9 ==
# Valves BB and DD are open, releasing 33 pressure.
# You open valve JJ.

# == Minute 10 ==
# Valves BB, DD, and JJ are open, releasing 54 pressure.
# You move to valve II.

# == Minute 11 ==
# Valves BB, DD, and JJ are open, releasing 54 pressure.
# You move to valve AA.

# == Minute 12 ==
# Valves BB, DD, and JJ are open, releasing 54 pressure.
# You move to valve DD.

# == Minute 13 ==
# Valves BB, DD, and JJ are open, releasing 54 pressure.
# You move to valve EE.

# == Minute 14 ==
# Valves BB, DD, and JJ are open, releasing 54 pressure.
# You move to valve FF.

# == Minute 15 ==
# Valves BB, DD, and JJ are open, releasing 54 pressure.
# You move to valve GG.

# == Minute 16 ==
# Valves BB, DD, and JJ are open, releasing 54 pressure.
# You move to valve HH.

# == Minute 17 ==
# Valves BB, DD, and JJ are open, releasing 54 pressure.
# You open valve HH.

# == Minute 18 ==
# Valves BB, DD, HH, and JJ are open, releasing 76 pressure.
# You move to valve GG.

# == Minute 19 ==
# Valves BB, DD, HH, and JJ are open, releasing 76 pressure.
# You move to valve FF.

# == Minute 20 ==
# Valves BB, DD, HH, and JJ are open, releasing 76 pressure.
# You move to valve EE.

# == Minute 21 ==
# Valves BB, DD, HH, and JJ are open, releasing 76 pressure.
# You open valve EE.

# == Minute 22 ==
# Valves BB, DD, EE, HH, and JJ are open, releasing 79 pressure.
# You move to valve DD.

# == Minute 23 ==
# Valves BB, DD, EE, HH, and JJ are open, releasing 79 pressure.
# You move to valve CC.

# == Minute 24 ==
# Valves BB, DD, EE, HH, and JJ are open, releasing 79 pressure.
# You open valve CC.

# == Minute 25 ==
# Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.

# == Minute 26 ==
# Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.

# == Minute 27 ==
# Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.

# == Minute 28 ==
# Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.

# == Minute 29 ==
# Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.

# == Minute 30 ==
# Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.
# This approach lets you release the most pressure possible in 30 minutes with this valve layout, 1651.

# Work out the steps to release the most pressure in 30 minutes. What is the most pressure you can release?


import re
import timeit


TIME_LIMIT = 30
TIME_VALVE_TRAVEL = 1
TIME_VALVE_OPEN = 1



class Valve:
    def __init__(self, name, flow_rate):
        self.name = name
        self.flow_rate = flow_rate
        self.children = set()
    

    def __repr__(self):
        return f'Valve: {self.name}, Flow Rate: {self.flow_rate}'



def read_input(file_path):
    with open(file_path, 'r') as file:
        lines = file.read().splitlines()

    valve_infos = dict()
    regex = r'Valve (..) has flow rate=(\d+); tunnel[s]? lead[s]? to valve[s]? (.+)'

    for line in lines:
        match = re.findall(regex, line)[0]
        source_valve= match[0]
        flow_rate = int(match[1])
        destination_valves = tuple(match[2].split(', '))
        valve_infos[source_valve] = (flow_rate, destination_valves)

    return valve_infos



def process_data(valve_infos):
    current_valve = 'AA'
  
    # Build valve item data.
    valves = dict()
    for k, v in valve_infos.items():
        valve = Valve(k, v[0])
        valves[k] = valve

    # Added children valve items to valve item parents.
    for k, v in valve_infos.items():
        valve = valves[k]
        for child_valve_name in v[1]:
            child_valve = valves[child_valve_name]
            valve.children.add(child_valve)

  



    return 1



def run():
    input_data_sample = read_input('./day_16_input_sample.txt')
    input_data = read_input('./day_16_input.txt')

    print('DAY 16')

    # Part 1 Answer
    answer_1_sample = process_data(input_data_sample)
    print(f'Answer 1 Sample: {answer_1_sample}') # 24
    # answer_1 = process_data(input_data)
    # print(f'Work out the steps to release the most pressure in 30 minutes. What is the most pressure you can release? : {answer_1}') # 

    # # Part 2 Answer
    # answer_2_sample = process_data(input_data_sample)
    # print(f'Answer 2 Sample: {answer_2_sample}') # 
    # answer_2 = process_data(input_data)
    # print(f'How many units of sand come to rest? : {answer_2}') # 



if __name__ == '__main__':
    start_time = timeit.default_timer()
    run()
    print('Runtime: {} seconds.'.format(round(timeit.default_timer() - start_time, 5)))
