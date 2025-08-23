# wsjt-all
**A Python command-line tool to analyse WSJT-X 'all.txt' files**
## Purpose
The point of this tool is to make analysing the WSJT-X 'all.txt' files easy, avoiding having to open them with text editors, and providing various plots and statistical summaries.

This initial version has been developed specifically to analyse a *pair* of all.txt files, to compare *reception* performance achieved with two different and *simultaneous* station configurations. 

My own pesonal motivation here is to compare my reception performance, in a fairly dense urban/sub-urban location, with reception at a remote site (web SDR). To do this, I run two separate instances of WSJT-X, with one connected to the transceiver as normal, and the other receiving audio via a virtual cable from a web SDR running in a browser window. This results in a second ALL.txt file with a few sessions that overlap the sessions in the large 'main' all.txt file. Browsing these files to compare reception is not trivial, and getting a good overview of the differences is difficult - hence, this software.

I will probably develop this next to produce plots from *single* ALL.txt files, and produce more / different plots etc.

## Installation
Install with pip:
```
pip install wsjt_all
```

## Usage
There are currently two simple command line commands to use:
```
wsjt_all_ab
```
This runs the comparison described above, automatically finding 'sessions' (defined time ranges covering reception of a single mode on a single band) and then automatically finding sessions that are common to both all files. A plot is produced and saved in the 'plots' folder for every common session.

```
wsjt_all_ab_live
```
This analyses the very last session in the all files, and plots a live-updating plot covering the current time to 5 minutes ago. It will be blank if you are not currently running two instances of WSJT-X as described above.

## Configuration
The software uses a simple wsjt_all.ini file to locate the all.txt files and set a couple of options. If none exists, the software can create a template for you but you still need to edit it to specify the paths to the all files. The wsjt_all.ini file looks like this:
```
[inputs]
allA = C:\Users\drala\AppData\Local\WSJT-X\all.txt
allB = C:\Users\drala\AppData\Local\WSJT-X - AltAB\all.txt

[settings]
session_guard_seconds = 300
live_plot_window_seconds = 300
```

