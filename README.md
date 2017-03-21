# snow-removal

## Requirements

Only need a computer that can run shell scripts and use python3.

## Usage

### Getting Data

Tweak the station name and date ranges in the file `get_data.sh` to your parameters.


**Important!** Make sure that the parameters in `get_data.sh` are the same as in `run_snow_removal.sh`!

Once your parameters are set run the codes in this order:

    bash get_data.sh
    bash run_snow_removal.sh
    python3 plot_data.py
