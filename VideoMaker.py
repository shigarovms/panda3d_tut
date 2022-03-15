import imageio
import os

filenames = []
for filename in sorted(os.listdir('mediaContent/framesForMovie')):
    if filename[0] != '.':
        filenames.append(filename)

images = []
for filename in filenames:
    images.append(imageio.imread(f'mediaContent/framesForMovie/{filename}'))
    os.remove(f'mediaContent/framesForMovie/{filename}')
imageio.mimsave('mediaContent/exportedVideo/pandaMovie.gif', images, duration=1/12)


