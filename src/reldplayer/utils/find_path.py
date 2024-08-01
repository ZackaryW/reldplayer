import os
import psutil as psutil
from psutil import AccessDenied
import pygetwindow as pw


def get_ldpath_via_psutil():
    for proc in psutil.process_iter():
        if proc.name() in ["dnplayer.exe", "dnmultiplayer.exe"]:
            try:
                return os.path.dirname(proc.cmdline()[0])
            except AccessDenied:
                continue


def get_ldpath_via_windows():
    #
    windows = pw.getAllWindows()
    windows = {w.title: w for w in windows if w.title}
    pass


get_ldpath_via_windows()
