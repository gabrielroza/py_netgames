class Token:
    def __init__(self, color, radius):
        self._color = color
        self._radius = radius

    def get_color(self) -> tuple:
        return self._color

    def get_radius(self) -> float:
        return self._radius
