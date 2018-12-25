import matplotlib.pyplot as plt
from matplotlib import animation
from IPython.display import display, HTML
import numpy as np

def plot_sequence_images(image_array):
    ''' Display images sequence as an animation in jupyter notebook
    
    Args:
        image_array(numpy.ndarray): image_array.shape equal to (num_images, height, width, num_channels)
    '''
    dpi = 72.0
    xpixels, ypixels = image_array[0].shape[:2]
    fig = plt.figure(figsize=(ypixels/dpi, xpixels/dpi), dpi=dpi)
    im = plt.figimage(image_array[0])

    def animate(i):
        im.set_array(image_array[i])
        return (im,)

    anim = animation.FuncAnimation(fig, animate, frames=len(image_array), interval=33, repeat_delay=1, repeat=True)
    display(HTML(anim.to_html5_video()))
    
# Demo of plot_sequence_images
import cv2
video_path = "/home/linux_fhb/data/suzhouc/test/top_camera.mp4"
video = cv2.VideoCapture()
video.open(video_path)
imgs = []
while True:
    is_valid, img = video.read()
    if not is_valid: break
    imgs.append(img)
video.release()
plot_sequence_images(imgs)
    
#############################
    
def plot_animation_function(xy_generator, frames=100, figsize=(6, 4), 
                            xlim=(0,2), ylim=(0, 2),interval=20, blit=True):
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    line, = ax.plot([], [], lw=2)
    def init():
        line.set_data([], [])
        return (line,)
    def animate(*args, **kwargs):
        x, y = next(xy_generator)
        line.set_data(x, y)
        return (line,)
    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=frames,
                                  interval=interval, blit=blit)
    display(HTML(anim.to_html5_video()))
    fig.delaxes(ax)

# Demo of plot_animation_function
frames = 100
def GeneratorXY(frames):
    for i in range(frames):
        x = np.linspace(0, 2, 1000)
        y = np.sin(2 * np.pi * (x - 0.01 * i))
        yield (x, y)
        
plot_animation_function(GeneratorXY(frames), frames=frames, figsize=(8, 6),
                       xlim=(0, 2), ylim=(-2, 2))