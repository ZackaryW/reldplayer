from time import sleep
import typing
import screeninfo
import pygetwindow as gw
def get_screen_dimensions(monitor_index=0):
    monitors = screeninfo.get_monitors()
    if monitor_index < 0 or monitor_index >= len(monitors):
        raise ValueError("Invalid monitor index")
    monitor = monitors[monitor_index]
    # Return both dimensions and the position of the monitor
    return (monitor.width, monitor.height, monitor.x, monitor.y)

def get_all_monitors():
    return screeninfo.get_monitors()

def find_current_monitor(wndPos):
    """Determine which monitor a window is currently on based on its position"""
    for monitor in get_all_monitors():
        if (monitor.x <= wndPos[0] < monitor.x + monitor.width and
                monitor.y <= wndPos[1] < monitor.y + monitor.height):
            return monitor
    return None  # Fallback if no monitor matches, should be handled appropriately

def activatewnd(wnd : gw.Window):
    try:
        wnd.activate()
    except gw.PyGetWindowException:
        pass

def gridOrientation(
        wnds : typing.List[gw.Window],
        row : int, 
        col : int, 
        maxwidth : float = None,
        maxheight : float = None,
        minwidth : float = None,
        minheight : float = None,
        monitor : int = 0,
        
    ):

        screen_width, screen_height, monitor_x, monitor_y = get_screen_dimensions(monitor_index=monitor)
        num_windows = len(wnds)
        if num_windows == 0 or row == 0 or col == 0:
            return  # Early return if invalid input

        window_width = screen_width // col
        window_height = screen_height // row

        # Apply max and min dimensions
        if maxwidth is not None:
            window_width = min(window_width, maxwidth)
        if maxheight is not None:
            window_height = min(window_height, maxheight)
        if minwidth is not None:
            window_width = max(window_width, minwidth)
        if minheight is not None:
            window_height = max(window_height, minheight)

        for index, window_instance in enumerate(wnds):
            window_instance : gw.Win32Window
            new_x = (index % col) * window_width + monitor_x
            new_y = (index // col) * window_height + monitor_y

            activatewnd(window_instance)
            window_instance.resizeTo(window_width, window_height)
            window_instance.moveTo(new_x, new_y)

            if index == row * col - 1:
                break
                
            sleep(0.2)