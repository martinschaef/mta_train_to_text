import time, os, sys, requests
from google.transit import gtfs_realtime_pb2
from protobuf_to_dict import protobuf_to_dict
from sense_hat import SenseHat

sense = SenseHat()
sense.rotation = 180


TOO_SHORT_TIME=3 # Don't show the time if the train is closer than TOO_SHORT_TIME minutes
TOO_LONG_TIME=9 # Don't show the time if the train is further than TOO_LONG_TIME minutes

# The stops that we want to look at.
# Check goole_transit.zip/stops.txt for full list.
STOP_IDS=["R08S"] # This is for south bound 39 Ave
# if you want north bound 34 St on NQRW, you woud use:
# STOP_IDS=["R17N", "D17N"] 
# For Queensboro Plaza: R09,R09N,R09S and 718,718N,718S 
TRAIN_NAME="N" # Pick the train to get the right feed. See get_train_feed_url()
API_KEY=os.environ['API_KEY'] # get one from http://datamine.mta.info/user/register

# based on the feeds at http://datamine.mta.info/list-of-feeds
def get_train_feed_url(api_key, train_name):
    feed_id=0
    if train_name in ["1", "2", "3", "4", "5", "6"]:
        feed_id=1
    elif train_name in ["A", "C", "E"]:
        feed_id=26
    elif train_name in ["N", "Q", "R", "W"]:
        feed_id=16
    elif train_name in ["B", "D", "F", "M"]:
        feed_id=21
    elif train_name in ["L"]:
        feed_id=2
    elif train_name in ["SIR"]:
        feed_id=11
    elif train_name in ["G"]:
        feed_id=31
    elif train_name in ["J", "Z"]:
        feed_id=36
    else:
        raise Exception("Unknown train name {}. Check http://datamine.mta.info/list-of-feeds".format())
    return 'http://datamine.mta.info/mta_esi.php?key={}&feed_id={}'.format(api_key, feed_id)

# Returns a list of pairs of train arrival time and train id (as string)
# Takes the train data (from a feed) and the station id as input. For
# station IDs check the stops.txt file in the google_transit.zip
def station_time_lookup(train_data, station):
    collected_times = []
    for trains in train_data: # trains are dictionaries
        if trains.get('trip_update', False) != False:
            unique_train_schedule = trains['trip_update'] # train_schedule is a dictionary with trip and stop_time_update

            # E.g.
            # 'trip': {   'route_id': u'R',
            #             'start_date': u'20180120',
            #             'trip_id': u'107400_R..S'}            
            train_info = unique_train_schedule['trip']
            route_id = train_info['route_id']

            unique_arrival_times = unique_train_schedule['stop_time_update'] # arrival_times is a list of arrivals
            for scheduled_arrivals in unique_arrival_times: #arrivals are dictionaries with time data and stop_ids
                if scheduled_arrivals.get('stop_id', False) == station:                    
                    time_data = scheduled_arrivals['arrival']
                    unique_time = time_data['time']
                    if unique_time != None:
                        collected_times.append((unique_time, route_id))
    return collected_times


while True:
    try:
        # Requests subway status data feed from City of New York MTA API
        feed = gtfs_realtime_pb2.FeedMessage()
        response = requests.get(get_train_feed_url(API_KEY, TRAIN_NAME))
        feed.ParseFromString(response.content)
        subway_feed = protobuf_to_dict(feed) # subway_feed is a dictionary
        realtime_data = subway_feed['entity'] # train_data is a list

        # Run the above function for all stations
        arriving_trains = list()
        for stop_id in STOP_IDS:
            arriving_trains.extend(station_time_lookup(realtime_data, stop_id))

        arriving_trains.sort(key=lambda tup: tup[0])

        # Grab the current time so that you can find out the minutes to arrival
        current_time = int(time.time())

	found_train=False
        for arrival_time, train_name in arriving_trains:
            time_to_train = int(((arrival_time - current_time) / 60))
            print ("Next {} train in {} min".format(train_name, time_to_train))

            if time_to_train<TOO_SHORT_TIME or time_to_train > TOO_LONG_TIME:
                continue
            color = [0, 0, 100]
            if time_to_train < 7:
                color = [0, 0, 250]
            if time_to_train < 5:
                color = [250, 0, 0]

            sense.show_letter(s=str(time_to_train), text_colour = color)
            found_train = True          
            break
        if found_train == False:
            sense.show_letter(s=">", text_colour = [100,100,0])
        time.sleep(10) # sleep for 10 seconds
    except:
        print(sys.exc_info()[0])
	break

sense.clear(0, 0, 0)

