"""A video player class."""

from .video_library import VideoLibrary
import random


class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self.cur_video = None
        self.paused = False

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""
        print("Here's a list of all available videos:")
        videos = sorted(self._video_library.get_all_videos(), key=lambda x: x.title)
        for video in videos:
            flag_str = ""
            if video.flagged:
                flag_str = f" - FLAGGED (reason: {video.flag_reason})"
            print(f"  {video.to_string() + flag_str}")

    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """
        err = "Cannot play video:"
        vid_to_play = self._video_library.get_video(video_id)
        if vid_to_play != None:
            if not vid_to_play.flagged:
                if self.cur_video != None:
                    self.stop_video()
                print("Playing video:", vid_to_play.title)
                self.cur_video = vid_to_play
                self.paused = False
            else:
                print(err, f"Video is currently flagged (reason: {vid_to_play.flag_reason})")
        else:
            print(err, "Video does not exist")

    def stop_video(self):
        """Stops the current video."""

        if self.cur_video != None:
            print("Stopping video:", self.cur_video.title)
            self.cur_video = None
        else:
            print("Cannot stop video: No video is currently playing")

    def play_random_video(self):
        """Plays a random video from the video library."""

        videos = [v for v in self._video_library.get_all_videos() if not v.flagged]
        if len(videos) != 0:
            vid_to_play = random.choice(videos)
            self.play_video(vid_to_play.video_id)
        else:
            print("No videos available")

    def pause_video(self):
        """Pauses the current video."""

        if self.cur_video != None:
            if not self.paused:
                print("Pausing video:", self.cur_video.title)
                self.paused = True
            else:
                print("Video already paused:", self.cur_video.title)
        else:
            print("Cannot pause video: No video is currently playing")


    def continue_video(self):
        """Resumes playing the current video."""

        if self.cur_video != None:
            if self.paused:
                print("Continuing video:", self.cur_video.title)
                self.paused = False
            else:
                print("Cannot continue video: Video is not paused")
        else:
            print("Cannot continue video: No video is currently playing")

    def show_playing(self):
        """Displays video currently playing."""

        cur = self.cur_video

        if self.cur_video != None:
            msg = f"Currently playing: {cur.to_string()}"
            if self.paused:
                msg += " - PAUSED"
            print(msg)
        else:
            print("No video is currently playing")

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """

        playlist = self._video_library.get_playlist(playlist_name.lower())
        if playlist == None:
            self._video_library.create_playlist(playlist_name)
            print("Successfully created new playlist:", playlist_name)
        else:
            print("Cannot create playlist: A playlist with the same name already exists")

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        err = f"Cannot add video to {playlist_name}:"
        playlist = self._video_library.get_playlist(playlist_name.lower())
        if playlist != None:
            vid = self._video_library.get_video(video_id)
            if vid != None:
                if not vid.flagged:
                    added = playlist.add_video(video_id)
                    if added:
                        print(f"Added video to {playlist_name}: {vid.title}")
                    else:
                        print(err, "Video already added")
                else:
                    print(err, f"Video is currently flagged (reason: {vid.flag_reason})")
            else:
                print(err, "Video does not exist")
        else:
            print(err, "Playlist does not exist")

    def show_all_playlists(self):
        """Display all playlists."""

        playlists = sorted(self._video_library.get_all_playlists(), key=lambda x: x.name)
        if len(playlists) > 0:
            print("Showing all playlists:")
            for pl in playlists:
                print(pl.name)
        else:
            print("No playlists exist yet")

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlist = self._video_library.get_playlist(playlist_name.lower())
        if playlist != None:
            print("Showing playlist:", playlist_name)
            if len(playlist.videos) > 0:
                for video_id in playlist.videos:
                    video = self._video_library.get_video(video_id)
                    flag_str = ""
                    if video.flagged:
                        flag_str = f" - FLAGGED (reason: {video.flag_reason})"
                    print("  " + video.to_string() + flag_str)
            else:
                print("  No videos here yet")
        else:
            print(f"Cannot show playlist {playlist_name}: Playlist does not exist")

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        err = f"Cannot remove video from {playlist_name}:"
        playlist = self._video_library.get_playlist(playlist_name.lower())
        if playlist != None:
            vid = self._video_library.get_video(video_id)
            if vid != None:
                removed = playlist.remove_video(video_id)
                if removed:
                    print(f"Removed video from {playlist_name}: {vid.title}")
                else:
                    print(err, "Video is not in playlist")
            else:
                print(err, "Video does not exist")
        else:
            print(err, "Playlist does not exist")

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        err = f"Cannot clear playlist {playlist_name}:"

        playlist = self._video_library.get_playlist(playlist_name.lower())
        if playlist != None:
            playlist.clear()
            print(f"Successfully removed all videos from {playlist_name}")
        else:
            print(err, "Playlist does not exist")

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        err = f"Cannot delete playlist {playlist_name}:"

        deleted = self._video_library.delete_playlist(playlist_name.lower())
        if deleted:
            print(f"Deleted playlist: {playlist_name}")
        else:
            print(err, "Playlist does not exist")

    def play_from_selection(self, found_vids):
        print("Would you like to play any of the above? If yes, specify the number of the video.")
        print("If your answer is not a valid number, we will assume it's a no.")
        command = input()
        if command.isdigit():
            command = int(command)
            if command <= len(found_vids) and command > 0:
                self.play_video(found_vids[command-1].video_id)

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """

        all_videos = sorted(self._video_library.get_all_videos(), key=lambda x: x.title)
        found_vids = [v for v in all_videos if search_term.lower() in v.title.lower()
                                                and not v.flagged]
        if len(found_vids) > 0:
            print(f"Here are the results for {search_term}:")
            for i in range(len(found_vids)):
                video = found_vids[i]
                print(f"  {i+1}) {video.to_string()}")
            self.play_from_selection(found_vids)
        else:
            print("No search results for", search_term)

    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        all_videos = sorted(self._video_library.get_all_videos(), key=lambda x: x.title)
        found_vids = []
        for vid in all_videos:
            tags = [tag.lower() for tag in vid.tags]
            if video_tag.lower() in tags and not vid.flagged:
                found_vids.append(vid)
        if len(found_vids) > 0:
            print(f"Here are the results for {video_tag}:")
            for i in range(len(found_vids)):
                video = found_vids[i]
                print(f"  {i+1}) {video.to_string()}")
            self.play_from_selection(found_vids)
        else:
            print("No search results for", video_tag)

    def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        err = "Cannot flag video:"
        vid_to_flag = self._video_library.get_video(video_id)
        if vid_to_flag != None:
            if vid_to_flag == self.cur_video:
                self.stop_video()
            if not vid_to_flag.flagged:
                vid_to_flag.flag(flag_reason)
                print(f"Successfully flagged video: {vid_to_flag.title} (reason: {vid_to_flag.flag_reason})")
            else:
                print(err, "Video is already flagged")
        else:
            print(err, "Video does not exist")

    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        err = "Cannot remove flag from video:"
        vid_to_allow = self._video_library.get_video(video_id)
        if vid_to_allow != None:
            if vid_to_allow.flagged:
                vid_to_allow.allow()
                print(f"Successfully removed flag from video: {vid_to_allow.title}")
            else:
                print(err, "Video is not flagged")
        else:
            print(err, "Video does not exist")
