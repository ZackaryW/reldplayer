import typing
import pyautogui
import pygetwindow as gw
import pyscreeze


class SettingGUi:
    def __init__(self, wnd: gw.Window) -> None:
        self.__wnd = wnd

    @property
    def wnd(self):
        return self.__wnd

    def __screenshot(self):
        return pyscreeze.screenshot(
            region=(
                int(self.__wnd.left),
                int(self.__wnd.top),
                int(self.__wnd.width),
                int(self.__wnd.height),
            )
        )
    
    def __easyocr(self):
        from zro2.easyocr import get_text_coordinates
        import numpy
        self.__ocr_result = get_text_coordinates(numpy.array(self.__screenshot()))
        return self.__ocr_result
    
    @property
    def ocr_result(self):
        return self.__ocr_result

    def menu(
        self,
        option: typing.Literal[
            "Advanced",
            "Model",
            "Game settings",
            "Audio",
            "Network",
            "Shortcuts",
            "Wallpaper",
            "Other settings",
        ],
    ):
        res = self.__easyocr()

        for r in res:
            if r["text"] == option:
                top_left = r["top_left"]
                bottom_right = r["bottom_right"]

                pyautogui.click(
                    int(top_left[0] + (bottom_right[0] - top_left[0]) / 2),
                    int(top_left[1] + (bottom_right[1] - top_left[1]) / 2),
                )
