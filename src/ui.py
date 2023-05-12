from typing import NamedTuple

from asciimatics.screen import Screen

from life import Board


def place_glider_at_position(board, row_start, col_start):
    board.place_cell(row_start, col_start + 1)
    board.place_cell(row_start + 1, col_start + 2)
    for i in range(col_start, col_start + 3):
        board.place_cell(row_start + 2, i)


left_arrow = -203
up_arrow = -204
right_arrow = -205
down_arrow = -206

arrows = {left_arrow, up_arrow, right_arrow, down_arrow}


def print_board(board, screen):
    screen.fill_polygon(
        [
            [
                (0, 0),
                (screen.width // 2, 0),
                (screen.width // 2, screen.height),
                (0, screen.height),
            ]
        ]
    )
    for row_num, row in enumerate(str(board).split()):
        screen.print_at(row, 1, row_num + 1)


def ensure_in_range(value, low_limit, high_limit):
    value = low_limit if value < low_limit else value
    value = high_limit if value > high_limit else value
    return value


class InterfaceController:
    def __init__(self, screen: Screen):
        self.screen = screen
        self.board = Board(screen.width // 2 - 2, screen.height - 2)
        self.board_position = NamedTuple("Pos", x=int, y=int)(1, 1)
        self.x_cursor, self.y_cursor = screen.width // 5, screen.height // 3
        self.paused: bool = True
        self.timeout = 0.33
        self.actions_handlers = {ord("q"): exit, ord("s"): self.pause}
        self.paused_handlers = {
            ord(" "): self.invert_cell,
            ord("g"): self.place_glider,
        }
        self.run()

    def run(self):
        while True:
            if not self.paused:
                self.board.next()
            print_board(self.board, self.screen)
            self.print_right_sidebar()
            if self.paused:
                self.print_cursor()
            self.screen.refresh()
            self.screen.wait_for_input(self.timeout)
            event = self.screen.get_event()
            if event is not None:
                self.process_event(event)

    def print_cursor(self):
        is_cell_under = self.board.is_alive(self.y_cursor - 1, self.x_cursor - 1)
        center = ".o"[is_cell_under]
        self.print_at(f"<{center}>", self.x_cursor - 1, self.y_cursor)

    def process_event(self, event):
        if not hasattr(event, "key_code"):
            return
        key_code = event.key_code
        if key_code in arrows:
            self.move_cursor(key_code)
            return
        handler = None
        if self.paused:
            handler = self.paused_handlers.get(key_code)
        handler = handler or self.actions_handlers.get(key_code)
        if handler is not None:
            handler()

    def move_cursor(self, direction: int):
        x_cursor, y_cursor = self.x_cursor, self.y_cursor
        if direction == down_arrow:
            y_cursor += 1
        if direction == up_arrow:
            y_cursor -= 1
        if direction == left_arrow:
            x_cursor -= 1
        if direction == right_arrow:
            x_cursor += 1
        self.y_cursor = ensure_in_range(y_cursor, 1, self.screen.height - 2)
        self.x_cursor = ensure_in_range(x_cursor, 1, self.screen.width // 2 - 2)

    def pause(self):
        self.paused = not self.paused

    def invert_cell(self):
        self.board.toggle_cell(
            self.y_cursor - self.board_position.y, self.x_cursor - self.board_position.x
        )

    def place_glider(self):
        place_glider_at_position(self.board, self.y_cursor, self.x_cursor)

    def print_pause(self):
        text = "PAUSED" if self.paused else "           "
        self.print_at(text, self.screen.width // 2 + 2, self.screen.height // 2)

    def print_help(self):
        screen = self.screen
        help_lines = (
            "Navigate cursor with arrows",
            "Press <space> for placing cell",
            "Press <s> for start/stop",
            "Press <q> for quit",
        )
        print_at_x = screen.width // 2 + 2
        print_at_y = 1
        self.print_at(help_lines, print_at_x, print_at_y)

    def print_generation(self):
        self.print_at(
            f"Generation: {0}",
            self.screen.width // 2 + 2,
            self.screen.height - 1,
        )

    def print_right_sidebar(self):
        self.print_help()
        self.print_generation()
        self.print_pause()
        self.screen.refresh()

    def print_at(self, text, x_pos, y_pos):
        """Output one or few lines at position on screen."""
        if isinstance(text, str):
            text = (text,)
        for line_no, line in enumerate(text):
            self.screen.print_at(line, x_pos, y_pos + line_no)


def main():
    Screen.wrapper(InterfaceController)
