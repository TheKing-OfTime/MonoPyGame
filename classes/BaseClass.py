class BaseClass:
    _id = ''
    scene = None
    path_to_main = ''

    def __init__(self, scene):
        self.scene = scene

    def get_id(self) -> str:
        return self._id

    def set_id(self, _id: str):
        self._id = _id
