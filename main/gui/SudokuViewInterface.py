from abc import ABC, abstractmethod


class SudokuViewInterface(ABC):

    @abstractmethod
    def set_grid_value(self, row: int, col: int, num: str):
        pass

    @abstractmethod
    def disable_start_button(self) -> None:
        pass

    @abstractmethod
    def set_cell_font_color(self, row: int, col: int, color: str):
        pass

    @abstractmethod
    def show_acknowledge_dialog(self, title: str, msg: str):
        pass

    @abstractmethod
    def activate(self, row: int, col: int):
        pass

    @abstractmethod
    def deactivate(self, row: int, col: int):
        pass

    @abstractmethod
    def highlight(self, row: int, col: int):
        pass

    @abstractmethod
    def unhighlight(self, row: int, col: int):
        pass
