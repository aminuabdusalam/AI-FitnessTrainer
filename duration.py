from moviepy.video.io.VideoFileClip import VideoFileClip

def get_video_duration(file_path):
    # create a VideoFileClip object for the video
    video = VideoFileClip(file_path)
    # get the duration of the video in seconds
    duration = video.duration
    # close the video file
    video.reader.close()
    video.audio.reader.close_proc()
    # return the duration
    return duration


print(get_video_duration('pushup_demo.mp4'))