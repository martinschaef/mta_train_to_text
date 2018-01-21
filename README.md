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
export API_KEY="xxxxxxxxxxxxx"
```

You have to get your own API key (for free from) http://datamine.mta.info/user/register

This project is built based on the code by [neoterix](https://github.com/neoterix/nyc-mta-arrival-notify).

## Usage

Update the variables `STOP_IDS` and `TRAIN_NAME` as needed and remember to export you API_KEY. 

## Usage with Raspberry Pi and Sense Hat

![Demo](https://raw.githubusercontent.com/martinschaef/mta_train_to_text/master/img/demo.jpg) 

If you have a Raspberry Pi and a [Sense Hat](https://www.raspberrypi.org/products/sense-hat/) you can use [train_count_down.py](https://github.com/martinschaef/mta_train_to_text/blob/master/train_count_down.py) to show you the time in minutes to the next train on the matrix display. It is set up to only show trains that are between 3 and 9 minutes away, but that can be customized in the code.

You need to install
```
sudo apt-get install sense-hat
```
more on Sense Hat [here](https://pythonhosted.org/sense-hat/).

## Dependencies

```
pip install --upgrade gtfs-realtime-bindings
pip install protobuf3_to_dict
pip install -U python-dotenv
```
