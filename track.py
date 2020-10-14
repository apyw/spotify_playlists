class Track:
    def __init__(self, id):
        self.id = id
    def create_uris(self):
        return f"spotify:track:{self.id}"