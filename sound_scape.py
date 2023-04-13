# %%
import scaper
import os
import pandas as pd
import numpy as np
import moviepy.editor as mp

def set_scaper(duration = 20.0, seed = 123, path_to_audio = "audio"):
    path_to_audio = path_to_audio  # os.path.expanduser('~/audio')
    soundscape_duration = duration
    seed = seed
    foreground_folder = os.path.join(path_to_audio, 'foreground')
    background_folder = os.path.join(path_to_audio, 'background')
    sc = scaper.Scaper(soundscape_duration, foreground_folder, background_folder)
    sc.ref_db = -20
    return sc


def sound_scape(data, audio_file_name, duration = 20):
    sc = set_scaper(duration=duration)
    #df = pd.read_csv(data_directory, on_bad_lines="skip")
    #data = df["DATA"].head(15*duration).to_numpy()
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
    audiofile = 'audio'+audio_file_name+'.wav'
    jamsfile = 'audio'+audio_file_name+'.jams'
    txtfile = 'audio'+audio_file_name+'.txt'
    sc.generate(audiofile, jamsfile,
                allow_repeated_label=True,
                allow_repeated_source=True,
                reverb=0.1,
                disable_sox_warnings=True,
                no_audio=False,
                txt_path=txtfile)
data_directory = "Data\\Data\\"+"03"+".csv"
df = pd.read_csv(data_directory, on_bad_lines="skip")
data = df["DATA"].head(15*3).to_numpy()  
sound_scape(data, "03"+"short", duration= 3)
# %%
def add_sound(audio_file_name, video_file_name, final_video_name):
    audio = mp.AudioFileClip("audio/" + audio_file_name + ".wav")
    video1 = mp.VideoFileClip("video/" + video_file_name + ".mp4")
    final = video1.set_audio(audio)
    final.write_videofile("samples/" + final_video_name + ".mp4")
""" file_numbers = ["03", "04", "08", "14", "16", "29", "30", "33", "36"]

for file_number in file_numbers:
    directory = "Data\\Data\\" + file_number + ".csv"
    df = pd.read_csv(directory, on_bad_lines="skip")
    data = df["DATA"].head(300).to_numpy()
    distribution = (data - np.min(data)) / (np.max(data) - np.min(data))
    distribution_list = list(distribution/np.sum(distribution))
    pitch = list(2*(distribution - 0.5))

    sc.add_background(label=('const', 'breath'),
                      source_file=('choose', []),
                      source_time=('const', 0))
    sc.add_event(label=('const', 'heartbeat'),
                 source_file=('choose', []),
                 source_time=('const', 0),
                 event_time=('uniform', 0, 20),
                 event_duration=('truncnorm', 2, 1, 0.1, 3.9),
                 snr=('normal', 10, 3),
                 pitch_shift=('choose_weighted',  pitch, distribution_list),
                 time_stretch=('uniform', 0.8, 1.2))
    audiofile = file_number+'.wav'
    jamsfile = file_number+'.jams'
    txtfile = file_number+'.txt'
    sc.generate(audiofile, jamsfile,
                allow_repeated_label=True,
                allow_repeated_source=True,
                reverb=0.1,
                disable_sox_warnings=True,
                no_audio=False,
                txt_path=txtfile) """
# %%