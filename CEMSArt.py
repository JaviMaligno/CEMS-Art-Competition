import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from functools import partial
import pandas as pd
from sound_scape import sound_scape, add_sound
import warnings
warnings.filterwarnings("ignore")
import matplotlib as mpl 
# Requires installing ffmpeg and adding it to the PATH
mpl.rcParams['animation.ffmpeg_path'] = r'C:\ffmpeg\bin\\ffmpeg.exe'

# The color maps that will be available for the pictures
cmaps = ['viridis', 'plasma', 'inferno', 'magma', 'cividis', 'winter', 'cool', 'Wistia','hot'
        'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
           'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
            'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn',
            'binary', 'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink',
            'spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia',
            'hot', 'afmhot', 'gist_heat', 'copper',
            'PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu',
            'RdYlBu', 'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic',
         'twilight', 'twilight_shifted', 'hsv',
         'Pastel1', 'Pastel2', 'Paired', 'Accent',
            'Dark2', 'Set1', 'Set2', 'Set3',
            'tab10', 'tab20', 'tab20b', 'tab20c',
            'flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern',
            'gnuplot', 'gnuplot2', 'CMRmap', 'cubehelix', 'brg',
            'gist_rainbow', 'rainbow', 'jet', 'turbo', 'nipy_spectral',
            'gist_ncar']

def julia_quadratic(zx, zy, cx, cy, threshold):
    """Calculates whether the number z[0] = zx + i*zy with a constant c = x + i*y belongs
    to the Julia set. In order to belong, the sequence z[n + 1] = z[n]**2 + c, 
    must not diverge after 'threshold' number of steps. The sequence diverges
    if the absolute value of z[n+1] is greater than 4.
    
    :param float zx: the x component of z[0]
    :param float zy: the y component of z[0]
    :param float cx: the x component of the constant c
    :param float cy: the y component of the constant c
    :param int threshold: the number of iterations to considered it converged
    """
    # initial conditions
    z = complex(zx, zy)
    c = complex(cx, cy)
    
    for i in range(threshold):
        z = z**2 + c
        if abs(z) > 4.:  # it diverged
            return i
        
    return threshold - 1  # it didn't diverge

def generate_picture(a = 2 * np.pi / 4., r = 0.7885, density_per_unit = 400, threshold=20):
    ''' Generates a picture of a Julia set given the parameters. The constant c is represented as
     c = r*cos(a) + i*r*sin(a) = r*e^{i*a}'''
    # how many pixles per unit # I need 1000 to get 4K, 500 for 2K https://en.wikipedia.org/wiki/4K_resolution
    x_start, y_start = -2, -2  # an interesting region starts here
    width, height = 4, 4  
    

    re = np.linspace(x_start, x_start + width, width * density_per_unit )  # real axis
    im = np.linspace(y_start, y_start + height, height * density_per_unit)  # imaginary axis

    X = np.empty((len(re), len(im)))  # the initial array-like image
    
    cx, cy = r * np.cos(a), r * np.sin(a)

    # fill-in the image with the number of interations
    for i in range(len(re)):
        for j in range(len(im)):
            X[i, j] = julia_quadratic(zx=re[i], zy=im[j], cx=cx, cy=cy, threshold=threshold)

    #plt.savefig('julia_Set.png', dpi=300, bbox_inches='tight')
    return X

def animate(i, a = 2*np.linspace(0,2*np.pi, 100), r = [0.7885]*100, cmap = "magma"):
    '''Generates a picture for each i, this can be used to create an animation'''
    # clear axes object
    ax = plt.axes()
    ax.clear()
    ax.set_xticks([], [])
    ax.set_yticks([], [])
    # fill-in the image with the number of interations
    X = generate_picture(a[i], r = r[i])
    
    img = ax.imshow(X.T, interpolation="hamming", cmap=cmap)
    plt.gcf().text(0.15, 0.08, 'by Javier Aguilar Martín', fontsize=18)
    return [img]
    
    
def generate_animation(as_mp4 = True, file_name ='julia_set',  a = 2*np.linspace(0,2*np.pi, 100),r = [0.7885]*100, cmap = "magma", fps = 15):
    '''Generates an animation by creating many pictures iteratively.'''
    frames = len(a)
    fig = plt.figure(figsize=(10, 10))
    ax = plt.axes()
    ax.clear()
    ax.set_xticks([], [])
    ax.set_yticks([], [])
    anim = animation.FuncAnimation(fig, partial(animate, a = a, r = r, cmap = cmap), frames=frames, blit=True)
    if as_mp4:
            # Set up formatting for the movie files
            Writer = animation.writers['ffmpeg']
            writer = Writer(fps=fps, metadata=dict(artist='Me'), bitrate=1800)
            # save the animation as a mp4 file 
            anim.save('video/'+file_name+'.mp4', writer=writer)   
    else:
            anim.save('video/'+file_name+'.gif', writer='imagemagick')  

def create_video(data, file_name ='julia_set', as_mp4 = True):
    '''Takes the data an produces an animation by choosing the parameters and color map according to the data.
    The file name is the chosen name for the video and the audio'''
    index = data[0]
    distribution = (data - np.min(data))/(np.max(data)-np.min(data))
    r = distribution+0.5
    a = 2*np.pi*distribution
    cmap = cmaps[index % len(cmaps)]
    generate_animation(file_name = file_name, a = a, r = r, cmap = cmap, as_mp4 = as_mp4)

def CEMS_Art(file_name, data_directory, duration= 20):
    '''Generates the final product by extracting the data, creating the video and adding the sound.'''
    df = pd.read_csv(data_directory, on_bad_lines="skip")
    data = df["DATA"].head(round(15*duration)).to_numpy()
    sound_scape(data, file_name, duration=duration)
    create_video(data, file_name=file_name)
    add_sound(file_name, file_name, file_name)



