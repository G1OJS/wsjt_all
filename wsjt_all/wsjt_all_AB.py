import configparser
import wsjt_all as wall

config = configparser.ConfigParser()
config.read("wsjt_all.ini")
allA = config.get("inputs","allA")
allB = config.get("inputs","allB")
session_guard_seconds = int(config.get("settings","session_guard_seconds"))
wall.plot_all_historic(allA, allB, session_guard_seconds)


#plot_live(allA, allB, plot_window_seconds)
