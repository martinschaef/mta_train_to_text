## Overview
Like the name says.
```
python trains_to_text.py
```
```
Next Q train in 0 min
Next N train in 7 min
Next Q train in 13 min
Next R train in 13 min
Next N train in 20 min
Next Q train in 20 min
Next R train in 21 min
```

Prints the next trains for a given station.

You need to 
```
export export API_KEY="xxxxxxxxxxxxx"
```

You have to get your own API key (for free from) http://datamine.mta.info/user/register

This project is built based on the code by [neoterix](https://github.com/neoterix/nyc-mta-arrival-notify).

## Usage

Update the variables `STOP_IDS` and `TRAIN_NAME` as needed and remember to export you API_KEY. 

## Dependencies

```
pip install --upgrade gtfs-realtime-bindings
pip install protobuf3_to_dict
pip install -U python-dotenv
```
