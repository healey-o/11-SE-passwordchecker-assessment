import tkinter as tk
from tkinter import ttk
import gooeypie as gp

#This file allows me to create and style custom gooeypie widgets, by editing existing widgets

class ColourProgressbar(ttk.Progressbar, gp.GooeyPieWidget):
    """ Similar to ordinary gooeypie PorgressBar, but with changable colours

     """

    def __init__(self, container, mode='determinate'):
        """Creates a new ColourProgressBar widget

        Args
            container: The window or container to which the widget will be added
            mode (str): Optional - the mode of the progress bar, either 'determinate' or 'indeterminate'
        """
        gp.GooeyPieWidget.__init__(self, container)

        self._value = tk.IntVar()
        self.style = ttk.Style()
        self.style.theme_use('alt')
        self.style.configure("red.Horizontal.TProgressbar", foreground='red', background='red')
        ttk.Progressbar.__init__(self, container, style="red.Horizontal.TProgressbar", variable=self._value)
        self.mode = mode

    def __str__(self):
        return f"<Progressbar widget>"

    def __repr__(self):
        return self.__str__()

    @property
    def value(self):
        """Gets or sets the value of the progress bar as a number between 0 and 100"""
        return self._value.get()

    @value.setter
    def value(self, value):
        if type(value) not in (int, float):
            raise ValueError('Progressbar value must be an integer')
        if not (0 <= value <= 100):
            raise ValueError('Progressbar value must be an integer between 0 and 100 (inclusive)')

        self._value.set(value)

    @property
    def mode(self):
        """Gets or sets the mode of the progress bar - either 'determinate' or 'indeterminate'"""
        return self.cget('mode')

    @mode.setter
    def mode(self, mode):
        if mode not in ('determinate', 'indeterminate'):
            raise ValueError("mode must be either 'determinate' or 'indeterminate'")
        self.config(mode=mode)

    @property
    def width(self):
        """Gets or sets the width of the progress bar in pixels"""
        return self.cget('length')

    @width.setter
    def width(self, width):
        if type(width) != int:
            raise ValueError('width must be a positive integer')
        if width <= 0:
            raise ValueError('width must be a positive integer')

        self.config(length=width)
