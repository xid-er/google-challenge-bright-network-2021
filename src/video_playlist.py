"""A video playlist class."""


class Playlist:
    """A class used to represent a Playlist."""

    def __init__(self, name: str):
        """Playlist constructor."""
        self._name = name
        self._videos = []

    @property
    def name(self) -> str:
        """Returns the name of a playlist."""
        return self._name

    @property
    def videos(self) -> list:
        """Returns the list of videos in a playlist."""
        return self._videos

    def add_video(self, video_id):
        if not video_id in self._videos:
            self._videos.append(video_id)
            return True
        else:
            return False

    def remove_video(self, video_id):
        if video_id in self._videos:
            self._videos.remove(video_id)
            return True
        else:
            return False

    def clear(self):
        self._videos = []
