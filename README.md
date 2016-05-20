## CMU-FCE
Python script that allows users to lookup FCE information quickly. Prints outs a nicely formatted table enumerating avg. hours/week and avg. course rating. Omits entries from the Qatar campus and entries with the old-style formatting.
## Usage
`python cmu-fce.py -n 15462 -e`
### Flags
`-n` : Course number (e.g. 18290)

`-h` : View help

`-t` : Number of entries taken into account in summary statistics (default is 6)

`-v` : Verbose mode, prints out all available data entries

`-e` : Exclude Summer semester

## Example
![alt text](https://github.com/eourcs/cmu-fce/blob/master/examples/15251-1.png "15-251 Lookup Example")

## Dependencies
Python 3.+
