import math
import sys
import random

# Constants
Q_LIMIT = 100
BUSY = 1
IDLE = 0

# Global variables
next_event_type = 0
num_custs_delayed = 0
num_delays_required = 0
num_events = 0
num_in_q = 0
server_status = 0
area_num_in_q = 0.0
area_server_status = 0.0
mean_interarrival = 0.0
mean_service = 0.0
sim_time = 0.0
time_arrival = [0.0] * (Q_LIMIT + 1)
time_last_event = 0.0
time_next_event = [0.0] * 3
total_of_delays = 0.0


def initialize():
    global sim_time, server_status, num_in_q, time_last_event, num_custs_delayed, total_of_delays, area_num_in_q, area_server_status, num_events, time_next_event

    sim_time = 0.0
    server_status = IDLE
    num_in_q = 0
    time_last_event = 0.0

    num_custs_delayed = 0
    total_of_delays = 0.0
    area_num_in_q = 0.0
    area_server_status = 0.0

    num_events = 2
    time_next_event[1] = sim_time + expon(mean_interarrival)
    time_next_event[2] = 1.0e+30


def timing():
    global sim_time, next_event_type

    min_time_next_event = 1.0e+29
    next_event_type = 0

    for i in range(1, num_events + 1):
        if time_next_event[i] < min_time_next_event:
            min_time_next_event = time_next_event[i]
            next_event_type = i

    if next_event_type == 0:
        print("\nEvent list empty at time", sim_time)
        sys.exit(1)

    sim_time = min_time_next_event


def arrive():
    global num_in_q, server_status, num_custs_delayed, total_of_delays

    global time_next_event

    delay = 0.0
    time_next_event[1] = sim_time + expon(mean_interarrival)

    if server_status == BUSY:
        num_in_q += 1
        if num_in_q > Q_LIMIT:
            print("\nOverflow of the array time_arrival at time", sim_time)
            sys.exit(2)
        time_arrival[num_in_q] = sim_time
    else:
        delay = 0.0
        total_of_delays += delay
        num_custs_delayed += 1
        server_status = BUSY
        time_next_event[2] = sim_time + expon(mean_service)


def depart():
    global num_in_q, server_status, num_custs_delayed, total_of_delays

    global time_next_event

    delay = 0.0

    if num_in_q == 0:
        server_status = IDLE
        time_next_event[2] = 1.0e+30
    else:
        num_in_q -= 1
        delay = sim_time - time_arrival[1]
        total_of_delays += delay
        num_custs_delayed += 1
        time_next_event[2] = sim_time + expon(mean_service)
        for i in range(1, num_in_q + 1):
            time_arrival[i] = time_arrival[i + 1]


def report():
    global total_of_delays, num_custs_delayed, area_num_in_q, sim_time, area_server_status

    print("\n\nAverage delay in queue", total_of_delays / num_custs_delayed, "minutes")
    print("Average number in queue", area_num_in_q / sim_time)
    print("Server utilization", area_server_status / sim_time)
    print("Time simulation ended", sim_time, "minutes")


def update_time_avg_stats():
    global time_last_event, area_num_in_q, area_server_status, sim_time, num_in_q, server_status

    time_since_last_event = sim_time - time_last_event
    time_last_event = sim_time

    area_num_in_q += num_in_q * time_since_last_event
    area_server_status += server_status * time_since_last_event


def expon(mean):
    return -mean * math.log(random.random())


def main():
    global infile, outfile, mean_interarrival, mean_service, num_delays_required

    infile = open("mm1.in", "r") # Open input file for reading data from it
    outfile = open("mm1.out", "w")

    num_events = 2

    mean_interarrival, mean_service, num_delays_required = map(float, infile.readline().split())

    print("Single-server queueing system\n", file=outfile)
    print("Mean interarrival time {:11.3f} minutes\n".format(mean_interarrival), file=outfile)
    print("Mean service time {:16.3f} minutes\n".format(mean_service), file=outfile)
    print("Number of customers {:14d}\n".format(int(num_delays_required)), file=outfile)

    initialize()

    while num_custs_delayed < num_delays_required:
        timing()
        update_time_avg_stats()

        if next_event_type == 1:
            arrive()
        elif next_event_type == 2:
            depart()

    report()

    infile.close()
    outfile.close()


if __name__ == "__main__":
    main()
