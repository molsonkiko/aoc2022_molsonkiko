import re
import time
import unittest

def valves_with_flow(graph: dict[str, dict]) -> set[str]:
    '''valves with nonzero flow, plus AA, the starting valve'''
    return set(valve for valve, info in graph.items() 
            if info['flow'] > 0 or valve == 'AA')

def parse_one_line(x):
    return re.findall(
        "Valve ([A-Z]{2})\D+(\d+)\D+?([A-Z]{2}(?:, [A-Z]{2})*)", x
    )[0]

def parse_lines(lines: list[str]) -> dict[str, dict]:
    graph = {}
    for line in lines:
        if not line:
            continue
        valve_id, flow_rate_str, leads_to_str = parse_one_line(line)
        flow_rate = int(flow_rate_str)
        graph[valve_id] = {'flow': flow_rate, 'tunnels': leads_to_str.split(', ')}
    return graph

def dijkstra(graph: dict[str, dict], start: str) -> dict[str, str]:
    '''
    For each other node in graph, get a backtrace from that node to start.
    From https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
    '''
    unvisited_valves = set(graph.keys())
    unvisited_valves.remove(start)
    dist = {valve: len(graph) for valve in unvisited_valves}
    prev = {valve: None for valve in unvisited_valves}
    for valve in graph[start]['tunnels']:
        dist[valve] = 1
        prev[valve] = start
    while unvisited_valves:
        valve2 = min(unvisited_valves, key=lambda x: dist[x])
        unvisited_valves.remove(valve2)
        unvisited_neighbors = set(graph[valve2]['tunnels']) & unvisited_valves
        for valve3 in unvisited_neighbors:
            alt = dist[valve2] + 1
            if alt < dist[valve3]:
                dist[valve3] = alt
                prev[valve3] = valve2
    return prev

PathMapType = dict[frozenset[str], list[str]]

def shortest_paths(graph: dict[str, dict], flowing_valves: set[str]) -> PathMapType:
    '''find the shortest paths between each pair of valves with nonzero flow.
    Use Dijkstra's algorithm.
    '''
    backtraces = {valve: dijkstra(graph, valve) for valve in flowing_valves}
    paths = {}
    for valve1, backtrace in backtraces.items():
        for valve2 in flowing_valves - {valve1}:
            path = [valve2]
            valve3 = backtrace[valve2]
            while valve3 != valve1:
                path.append(valve3)
                valve3 = backtrace[valve3]
            path.append(valve1)
            paths[frozenset({valve2, valve1})] = path
    return paths


def next_path_to_follow(
        current_valve: str,
        paths: PathMapType,
        graph: dict[str, dict],
        flowing_valves: set[str],
        minutes_remaining: int
    ) -> list[str]:
    '''
    given the current valve, choose the best valve to open next
    return the path to follow to get to the next valve, and
    '''
    def priority(valve: str) -> float:
        distance = len(paths[frozenset({valve, current_valve})])
        flow = graph[valve]['flow']
        return flow * (minutes_remaining - distance)
    next_to_visit = max(flowing_valves, key=priority)
    priorities = sorted([(valve, priority(valve)) for valve in flowing_valves],
        reverse=True, key=lambda x: x[1])
    print('Priorities: ', priorities)
    next_path = paths[frozenset({current_valve, next_to_visit})]
    if next_path[-1] == current_valve:
        return next_path[::-1]
    return next_path


def reward_of_path(valves: list[str], graph: dict[str, dict], paths: PathMapType) -> int:
    flow_per_minute = 0
    pressure_released = 0
    minutes_remaining = 30
    start = valves[0]
    next_node = valves[1]
    distance = len(paths[frozenset({start, next_node})])
    valve_idx = 1
    while minutes_remaining > 0:
        # travel to next node
        print(f'==============\n{minutes_remaining} minutes remaining\n'
             f'Flow rate: {flow_per_minute}, {pressure_released = }, open valves = {valves[1:valve_idx]}\n'
             f'current valve = {valves[valve_idx]}, going from {start} to {next_node}')
        # pressure escapes from opened valves while you travel
        dist = min(distance, minutes_remaining)
        pressure_released += flow_per_minute * dist
        minutes_remaining -= dist
        if minutes_remaining == 0:
            break
        # now that valve is open, pressure is released faster
        flow_per_minute += graph[valves[valve_idx]]['flow']
        if valve_idx == len(valves) - 1:
            return pressure_released + flow_per_minute * minutes_remaining
        start = valves[valve_idx]
        valve_idx += 1
        next_node = valves[valve_idx]
        distance = len(paths[frozenset({start, next_node})])
    return pressure_released


def Part1(lines: list[str]):
    '''It takes one minute to travel through a tunnel to another room,
    and one minute to open the valve once you are in a room.
    Once a valve is open, it releases *flow* pressure per minute.
    So if a valve with flow=10 is open for 5 minutes and another with flow=4 is
    open for 2 minutes, a total of 58 pressure is released.
    QUESTION: What is the maximum pressure that can be released in 30 minutes?
    '''
    graph = parse_lines(lines)
    flowing_valves = valves_with_flow(graph)
    paths = shortest_paths(graph, flowing_valves)
    # now we know the shortest path between each room we care about.
    # the next step is to use this information to determine the order in which
    # we travel to rooms.
    flowing_valves.remove('AA')
    valve_order = ['AA'] + sorted(flowing_valves, key=lambda x: graph[x]['flow'], reverse=True)
    total_flow = reward_of_path(valve_order, graph, paths)
    return total_flow

def Part2(lines: list[str]) -> int:
    return 0


SAMPLE_INPUT = [
    "Valve AA has flow rate=0; tunnels lead to valves DD, II, BB",
    "Valve BB has flow rate=13; tunnels lead to valves CC, AA",
    "Valve CC has flow rate=2; tunnels lead to valves DD, BB",
    "Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE",
    "Valve EE has flow rate=3; tunnels lead to valves FF, DD",
    "Valve FF has flow rate=0; tunnels lead to valves EE, GG",
    "Valve GG has flow rate=0; tunnels lead to valves FF, HH",
    "Valve HH has flow rate=22; tunnel leads to valve GG",
    "Valve II has flow rate=0; tunnels lead to valves AA, JJ",
    "Valve JJ has flow rate=21; tunnel leads to valve II",
]

CIRCLE = [
    'Valve AA has flow rate=0; tunnels lead to valves BB, EE',
    'Valve BB has flow rate=5; tunnels lead to valves AA, CC',
    'Valve CC has flow rate=10; tunnels lead to valves BB, DD',
    'Valve DD has flow rate=15; tunnels lead to valves CC, EE',
    'Valve EE has flow rate=20; tunnels lead to valves DD, AA',
]

CANNOT_COMPLETE = [
    'Valve AA has flow rate=0; tunnels leads to valves QQ, RR, BB',
    'Valve QQ has flow rate=0; tunnels lead to valves AA, PP',
    'Valve PP has flow rate=0; tunnels lead to valves QQ, OO',
    'Valve OO has flow rate=0; tunnels lead to valves PP, NN',
    'Valve NN has flow rate=0; tunnels lead to valves OO, MM',
    'Valve MM has flow rate=0; tunnels lead to valves NN, LL',
    'Valve LL has flow rate=0; tunnels lead to valves MM, KK',
    'Valve KK has flow rate=10; tunnel leads to valve LL',
    'Valve RR has flow rate=0; tunnels lead to valves AA, SS',
    'Valve SS has flow rate=0; tunnels lead to valves RR, TT',
    'Valve TT has flow rate=0; tunnels lead to valves SS, UU',
    'Valve UU has flow rate=0; tunnels lead to valves TT, VV',
    'Valve VV has flow rate=0; tunnels lead to valves UU, WW',
    'Valve WW has flow rate=15; tunnel leads to valve VV',
    'Valve BB has flow rate=0; tunnels lead to valves, AA, CC',
    'Valve CC has flow rate=0; tunnels lead to valves BB, DD',
    'Valve DD has flow rate=0; tunnels lead to valves CC, EE',
    'Valve EE has flow rate=0; tunnels lead to valves DD, FF',
    'Valve FF has flow rate=0; tunnels lead to valves EE, GG',
    'Valve GG has flow rate=20; tunnel leads to valve FF'
]


class Part1Tests(unittest.TestCase):
    def testPart1_sample_input(self):
        self.assertEqual(Part1(SAMPLE_INPUT), 1651)

    def test_circle(self):
        '''
        Minute 1: go to EE; 0 pressure released; no valves open
        Minute 2: open EE; 0 pressure released; no valves open
        Minute 3: go to DD; 20 pressure released; EE is open, releasing 20
        Minute 4: open DD; 20 + 20 = 40 pressure released; EE is open, releasing 20
        Minute 5: go to CC; 40 + 35 = 75 pressure released; EE + DD are open, releasing 35
        Minute 6: open CC; 75 + 35 = 110 pressure released; EE + DD are open, releasing 35
        Minute 7: go to BB; 110 + 45 = 155 pressure released; EE + DD + CC are open, releasing 45
        Minute 8: open BB; 155 + 45 = 200 pressure released; EE + DD + CC are open, releasing 45
        Minutes 9-30: hang out; 200 + 50 * 22 = 1300 pressure released; EE + DD + CC + BB are open, releasing 50
        '''
        self.assertEqual(Part1(CIRCLE), 1300)

    def test_cannot_complete(self):
        '''
        Minutes 1-6: Travel to GG; nothing open
        Minute 7: Open GG; nothing open
        Minutes 8-19: Travel to WW; GG is open, releasing 12 * 20 = 240 presure
        Minute 20: Open WW; GG is open, releasing 20 pressure, total released: 260
        Minutes 21-30: Travel to OO; GG + WW are open, releasing 35 * 10 pressure
        Total released: 610
        '''
        self.assertEqual(Part1(CANNOT_COMPLETE), 610)


class TestPart2(unittest.TestCase):
    def testPart2_sample_input(self):
        self.assertEqual(Part2(SAMPLE_INPUT), 0)


if __name__ == '__main__':
    with open('day16_input.txt') as f:
        lines = re.split('\r?\n', f.read())
    part1_answer = Part1(lines)
    print(f'part 1 answer = {part1_answer}')
    part2_answer = Part2(lines)
    print(f'part 2 answer = {part2_answer}')
    unittest.main()