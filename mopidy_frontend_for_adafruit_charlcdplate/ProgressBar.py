class ProgressBar:

    PROGRESS_CHARS = [u"\u2600", u"\u2601", u"\u2602", u"\u2603", u"\u2604"]

    def __init__(self, max, num_chars, pixels_in_char):
        self.max = max
        self.value = 0
        self.total_pixels = num_chars * pixels_in_char
        self.pixels_in_char = pixels_in_char
        self.string = ""
        self.pixels_to_draw = 0
        self.update = True
        self.set_value(0)

    def set_value(self, value):
        self.value = value
        if self.max > 0:
            pixels_to_draw = value * self.total_pixels / self.max
        else:
            pixels_to_draw = self.total_pixels

        if self.pixels_to_draw != pixels_to_draw:
            self.pixels_to_draw = pixels_to_draw
            self.string = ""

            for i in range(0, pixels_to_draw / self.pixels_in_char):
                self.string += ProgressBar.PROGRESS_CHARS[self.pixels_in_char - 1]

            rest = pixels_to_draw % self.pixels_in_char
            if rest > 0:
                self.string += ProgressBar.PROGRESS_CHARS[rest - 1]

            self.update = True

    def set_max(self, max):
        self.max = max
        self.set_value(self.value)

    def get_string(self):
        self.update = False
        return self.string

