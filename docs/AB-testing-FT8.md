# Using FT8 to Benchmark Station Rx/Tx Performance with wsjt_all
## Introduction
This page gives some background about why I developed wsjt_all; a bit about my personal exploration of ways to check that I'm getting the best possible performance out of my ham radio station, given the constraints I have. Every ham radio station
has constraints of *some* kind, and part of the fun of the hobby for me is working out how to do the best with the situation you're in. Getting instant signal reports in volume from [pskreporter](https://pskreporter.info/) has been a huge help in achieving this.

## My station
I live in a conservation area where no outside antennas are permitted, so everything I use is indoors. Despite this, when I look at pskreporter, I often have the longest
distance reach, and largest coverage area, of stations operating from my country (England), on what I would call some of the most difficult bands; 80m, 160m, and 2m. And that's on
both transmit and receive with a single Icom IC-7100 as the station transceiver. I'm not claiming
to 'win' all the time; clearly there are many stations with long Yagis reaching far into Europe on 2m and stations with superb receiving antennas in remote locations who do far 
better than I do. But what I do know is that I'm winning the battle against local QRM and using antennas that work well on transmit too, and I'm *absolutely* doing better than at least half
of other stations irrespective of location.

### TL;DR - the antennas
I've worked with attic antennas in two houses now over the last decade, and found that it's pretty easy to set up a fan dipole to cover at least 20m to 10m if not 40m to 6m. What I use 
currently is:
160, 80, 60, 40: Small transmitting loop 7.5m circumference made from 10mm copper tube
20, 15, 17, 10, 6m: fan dipole (I don't have 30m and 12m currently)
2m - my G1OJS Contraspiral

The thing that has made the most difference though is the addition of an active receive loop to these antennas for HF work. I use an LZ1AQ amplifier with a small loop made from 20mm wide 
aluminium strip, right at the top of the attic. Using the fan dipoles for Rx results in a very high noise floor even with careful minimisation (and measurement of) common mode currents. 
I have previously used an end-fed wire cut to 20m length, bent into a U shape to fit in my 5m x 5m attic space, which was great on transmit but even worse on receive than the fan dipoles as 
you would expect!

# Benchmarking
After I had played the game of watching the noise level on the S meter whilst adding chokes, turning off ring mains and devices etc, running up and downstairs and scribbling notes and thinking
"was that better?", I got interested in what I could do with pskreporter. Using the online maps helped me get a feel for how well my antennas were working on transmit, but I didn't get much info
for receive. When I later learned that once you get a spot on pskrepoter from a particular station, you won't get another for at least 20 minutes, I started to dig into using the live data feed from [mqtt.pskr.info](http://mqtt.pskreporter.info/), where there is no 20 minute limitation on repeated spots.

## BandOpticon
The first thing I did with the live data feed was write some software to show a live view of the digi-mode activity to and from my neighboring ham stations (in nearby Maidenhead squares). This told me what band activity was like *now* and at least I could then tell if bands were active but for some reason I couldn't hear activity. That was the first objective measure in a sea of subjective ones!
After a lot of work learning Python (where BandOpticon started) and then re-learning JavaScript, I developed BandOpticon into a web-based page so that anyone can use it. The current version is
[here](https://g1ojs.github.io/BandOpticon/BandOpticon). You can use this web page to see what bands are active, and get a view of what the connectivity is between your local squares or stations and remote squares/callsigns. There are some experimental views in there that look towards benchmarking too.

## Wsjt-all

