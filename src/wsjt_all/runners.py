import configparser
from .plotter import plot_all_historic, plot_live


def wsjt_all_ab():
    config = configparser.ConfigParser()
    config.read("wsjt_all.ini")
    allA = config.get("inputs","allA")
    allB = config.get("inputs","allB")
    session_guard_seconds = int(config.get("settings","session_guard_seconds"))
    plot_all_historic(allA, allB, session_guard_seconds)


def wsjt_all_ab_live():
    config = configparser.ConfigParser()
    config.read("wsjt_all.ini")
    allA = config.get("inputs","allA")
    allB = config.get("inputs","allB")
    live_plot_window_seconds = int(config.get("settings","live_plot_window_seconds"))
    plot_live(allA, allB, live_plot_window_seconds)
