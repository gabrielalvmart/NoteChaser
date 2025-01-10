class TrackSingleton:
    _instance = None
    _track = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TrackSingleton, cls).__new__(cls)
        return cls._instance

    def set_track(self, track):
        self._track = track

    def get_track(self):
        return self._track