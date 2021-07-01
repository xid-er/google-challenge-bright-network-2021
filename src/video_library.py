"""A video library class."""

from .video import Video
from .video_playlist import Playlist
from pathlib import Path
import csv


# Helper Wrapper around CSV reader to strip whitespace from around
# each item.
def _csv_reader_with_strip(reader):
    yield from ((item.strip() for item in line) for line in reader)


class VideoLibrary:
    """A class used to represent a Video Library."""

    def __init__(self):
        """The VideoLibrary class is initialized."""
        self._videos = {}
        with open(Path(__file__).parent / "videos.txt") as video_file:
            reader = _csv_reader_with_strip(
                csv.reader(video_file, delimiter="|"))
            for video_info in reader:
                title, url, tags = video_info
                self._videos[url] = Video(
                    title,
                    url,
                    [tag.strip() for tag in tags.split(",")] if tags else [],
                )

        self._playlists = []

    def get_all_videos(self):
        """Returns all available video information from the video library."""
        return list(self._videos.values())

    def get_video(self, video_id):
        """Returns the video object (title, url, tags) from the video library.

        Args:
            video_id: The video url.

        Returns:
            The Video object for the requested video_id. None if the video
            does not exist.
        """
        return self._videos.get(video_id, None)

    def get_all_playlists(self):
        return self._playlists

    def get_playlist(self, name):
        for pl in self._playlists:
            if pl.name.lower() == name:
                return pl
        return None

    def create_playlist(self, name):
        self._playlists.append(Playlist(name))

    def delete_playlist(self, name):
        for pl in self._playlists:
            if pl.name == name:
                self._playlists.remove(pl)
                return True
        return False
