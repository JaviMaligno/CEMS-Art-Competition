import scaper #On Windows requires installing SoX and adding it to PATH https://scaper.readthedocs.io/en/latest/installation.html
import os
import numpy as np
import moviepy.editor as mp

def set_scaper(duration = 20.0, seed = 123, path_to_audio = "audio"):
    '''Creates a scaper object with the audio files provided in the audio folder. This can be uses to generate sound scapes.
    The folder architecture is crucial for this to work, as it requires foreground and background folders.
    These folders must contain folders labelling each group of audio tracks.'''
    path_to_audio = path_to_audio  # os.path.expanduser('~/audio')
    soundscape_duration = duration
    seed = seed
    foreground_folder = os.path.join(path_to_audio, 'foreground')
    background_folder = os.path.join(path_to_audio, 'background')
    sc = scaper.Scaper(soundscape_duration, foreground_folder, background_folder)
    sc.ref_db = -20
    return sc


def sound_scape(data, audio_file_name, duration = 20):
    '''Creates a sound scape with the scaper object. The sounds are distributed and pitched randomly according to the data.'''
    sc = set_scaper(duration=duration)
    distribution = (data - np.min(data)) / (np.max(data) - np.min(data))
    distribution_list = list(distribution/np.sum(distribution))
    pitch = list(2*(distribution - 0.5))

    sc.add_background(label=('const', 'breath'),
                      source_file=('choose', []),
                      source_time=('const', 0))
    sc.add_event(label=('const', 'heartbeat'),
                 source_file=('choose', []),
                 source_time=('const', 0),
                 event_time=('uniform', 0, duration),
                 event_duration=('truncnorm', 2, 1, 0.1, 3.9),
                 snr=('normal', 10, 3),
                 pitch_shift=('choose_weighted',  pitch, distribution_list),
                 time_stretch=('uniform', 0.8, 1.2))
    audiofile = 'audio/'+audio_file_name+'.wav'
    jamsfile = 'audio/'+audio_file_name+'.jams'
    txtfile = 'audio/'+audio_file_name+'.txt'
    sc.generate(audiofile, jamsfile,
                allow_repeated_label=True,
                allow_repeated_source=True,
                reverb=0.1,
                disable_sox_warnings=True,
                no_audio=False,
                txt_path=txtfile)

def add_sound(audio_file_name, video_file_name, final_video_name):
    '''Takes the .wav soundscape file and adds it to the animation, creating a new video.'''
    audio = mp.AudioFileClip("audio/" + audio_file_name + ".wav")
    video1 = mp.VideoFileClip("video/" + video_file_name + ".mp4")
    final = video1.set_audio(audio)
    final.write_videofile("samples/" + final_video_name + ".mp4")

