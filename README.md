# wsjt_all
**A Python command-line tool to analyse WSJT-X 'all.txt' files**
## Purpose
The point of this tool is to make analysing the WSJT-X 'all.txt' files easy, avoiding having to open them with text editors, and providing various plots and statistical summaries.

**Whilst the tool is fully functional, the presentation of the data is being developed as I use this for my own interest, and some things need tidying (such as the cryptic '3FT8', '14FT8' in the plot title) that I haven't yet got around to**

**This initial version has been developed specifically to analyse a *pair* of all.txt files, to compare *reception* performance achieved with two different and *simultaneous* station configurations.** 

My own pesonal motivation here is to compare my reception performance, in a fairly dense urban/sub-urban location, with reception at a remote site (web SDR). To do this, I run two separate instances of WSJT-X, with one connected to the transceiver as normal, and the other receiving audio via a virtual cable from a web SDR running in a browser window. This results in a second ALL.txt file with a few sessions that overlap the sessions in the large 'main' all.txt file. Browsing these files to compare reception is not trivial, and getting a good overview of the differences is difficult - hence, this software.

I will probably develop this next to produce plots from *single* ALL.txt files, and produce more / different plots etc.

The questions I had in my mind, that I wrote this to try to answer, include:
 - At the basic level, how does my receive performance (All file A) compare to that of a 'good reference' (All file B): number of callsigns collected at each, comparison of SNR when both A and B receive the same callsign either simultaneously or within a specified time window.
 - How does that comparison change over time? Are signals fading in at A and out at B & vice versa? Is this true only for some callsigns and are the rest static or going the other way?
 - How variable is SNR at A, and at B?
 - What does SNR correlate with at A and B, if anything? (e.g. distance, bearing)
 - What's more meaningful, SNR or number of times a callsign is received over a time window?

## Outputs
After you run the program, you will find a 'plots' folder in which you will find plots like this:

<img width="600" height="800" alt="2025-08-22 0005 3FT8 for 5 25 mins" src="https://github.com/user-attachments/assets/b1f5d755-6bf1-400c-ac21-23917474c7f1" />

In the upper plot, the markers represent each callsign detected in the session, and the marker position shows the number of times this callsign was seen within the session time window in each all.txt file. To allow visibility of markers that lie on top of each other, some random position errors are deliberately added. Markers lying on the X axis or Y axis were seen in only one of the all files.

In the lower plot, the markers represent each signal report (SNR in dB) found, plotting one 'all.txt' file against the other. Reports falling on the dashed black line are equal in SNR between the two files / reception configurations. Reports from a given remote callsign are shown as a collection by coloring them a specific (but random) colour per callsign, and by joining the markers with lines. Of course, there are typically far more callsigns than colours available, so colours are re-used across different callsigns. 

The sepecific example above shows reception on 80m FT8, around midnight in summer, at G1OJS (on the X axis), compared with decodes derived from audio from the web SDR at Hack Green in England (on the Y axis). 

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

Note - I keep my all.txt files fairly small by archiving sections into other files, so if you have a single all file covering years of operation, you may have to edit it or wait quite a while for the plots!

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

