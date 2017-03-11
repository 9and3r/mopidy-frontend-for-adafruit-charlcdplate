class InputManager:

    # Char LCD plate button names.
    SELECT = 0
    RIGHT = 1
    DOWN = 2
    UP = 3
    LEFT = 4

    def __init__(self):
        self.buttons_current_state = {InputManager.SELECT: False, InputManager.RIGHT: False, InputManager.DOWN: False, InputManager.UP: False, InputManager.LEFT: False}
        self.buttons_last_state = {InputManager.SELECT: False, InputManager.RIGHT: False, InputManager.DOWN: False, InputManager.UP: False, InputManager.LEFT: False}

    def update(self, display):

        result = []

        self.buttons_last_state = self.buttons_current_state
        self.buttons_current_state = {}

        # Update buttons
        for key in self.buttons_last_state:
            self.buttons_current_state[key] = display.is_pressed(key)

        # Check buttons
        for key in self.buttons_current_state:
            if not self.buttons_current_state[key] and self.buttons_last_state[key]:
                # Button released
                result.append(InputEvent('click', key))

        return result


class InputEvent:

    def __init__(self, type, key):
        self.type = type
        self.key = key
