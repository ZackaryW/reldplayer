import os
from warnings import warn


def pyldplayer_curr_load():
    e = None
    try:
        return os.environ["PYLDPLAYER_CURR"]
    except KeyError as e:  # noqa
        return
    finally:
        if e:
            return
        warn("PYLDPLAYER_CURR will be deprecated in the future")


def lookup_path_via_proc():
    try:
        import psutil

        for proc in psutil.process_iter():
            try:
                if proc.name() == "dnplayer.exe":
                    return os.path.abspath(os.path.dirname(proc.exe()))
                if "dn" in proc.name():
                    path = os.path.abspath(os.path.dirname(proc.exe()))
                    counter = 0
                    while True:
                        contents = os.listdir(path)
                        if "dnplayer.exe" in contents:
                            return path
                        elif "LDPlayer" in contents:
                            path = os.path.join(path, "LDPlayer")
                        else:
                            path = os.path.dirname(path)
                        counter += 1
                        if counter > 5:
                            warn("Failed to find dnplayer.exe")
                            break

            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
    except Exception:
        return
