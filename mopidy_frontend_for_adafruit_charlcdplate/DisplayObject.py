import time


class DisplayObject:

    MAX_CHARS_IN_ROW = 16
    TIME_TO_UPDATE = 0.05

    def __init__(self):
        self.line1 = ""
        self.line2 = ""
        self.last_update = time.clock()
        self.scroll_pos1 = 0
        self.scroll_pos2 = 0

        self.update_indicator1 = False
        self.update_indicator2 = False

        self.line1_full_text1 = None
        self.line2_full_text2 = None

    def change_display_data(self, line1, line2):
        self.set_line1(line1)
        self.set_line2(line2)

    def set_line1(self, line1):
        self.line1 = line1
        self.scroll_pos1 = 0
        if len(self.line1) > DisplayObject.MAX_CHARS_IN_ROW:
            self.update_indicator1 = True
            self.line1_full_text1 = line1
            for i in range(0, DisplayObject.MAX_CHARS_IN_ROW/2, 1):
                self.line1_full_text1 += " "
        else:
            self.update_indicator1 = False
        self.last_update = time.clock()

    def set_line2(self, line2):
        self.line2 = line2
        self.scroll_pos2 = 0
        if len (self.line2) > DisplayObject.MAX_CHARS_IN_ROW:
            self.update_indicator2 = True
            self.line2_full_text2 = line2
            for i in range(0, DisplayObject.MAX_CHARS_IN_ROW/2, 1):
                self.line2_full_text2 += " "
        else:
            self.update_indicator2 = False
        self.last_update = time.clock()

    def update(self):
        if self.update_indicator1 or self.update_indicator2:
            current_time = time.clock()
            if current_time - DisplayObject.TIME_TO_UPDATE > self.last_update:
                self.last_update = current_time

                if self.update_indicator1:
                    self.scroll_pos1 += 1
                    if self.scroll_pos1 > len(self.line1_full_text1):
                        self.scroll_pos1 = 0

                if self.update_indicator2:
                    self.scroll_pos2 += 1
                    if self.scroll_pos2 > len(self.line2_full_text2):
                        self.scroll_pos2 = 0

                return True
        return False


    def getString(self):
        if self.update_indicator1:
            string1 = self.line1_full_text1[self.scroll_pos1:] + self.line1_full_text1[:self.scroll_pos1]
        else:
            string1 = self.line1
        if self.update_indicator2:
            string2 = self.line2_full_text2[self.scroll_pos2:] + self.line2_full_text2[:self.scroll_pos2]
        else:
            string2 = self.line2

        return string1[0:DisplayObject.MAX_CHARS_IN_ROW] + "\n" + string2[0:DisplayObject.MAX_CHARS_IN_ROW]

