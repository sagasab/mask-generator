import shutil
from pathlib import Path

import glob

import numpy
from PIL import Image

out_dir = Path('out')

# Clean output directory
if out_dir.exists():
    shutil.rmtree(out_dir)

# Make output directory
out_dir.mkdir()

input_images = glob.glob('in/**/original/**')


def mask_image(in_path):
    image = Image.open(in_path)
    arr = numpy.asarray(image).copy()
    for h in arr:
        for w in h:
            a = w[3]

            if a > 20:
                w[0] = 255
                w[1] = 255
                w[2] = 255
                w[3] = 255
            else:
                w[0] = 0
                w[1] = 0
                w[2] = 0
                w[3] = 255

    mask = Image.fromarray(arr)
    out_masks_dir = Path('out').joinpath(folder_name).joinpath('masks')

    if not out_masks_dir.exists():
        out_masks_dir.mkdir()

    filename = f'{Path(path).stem}.png'
    out_mask = out_masks_dir.joinpath(filename)

    mask.save(out_mask)


total = len(input_images)

for i, path in enumerate(input_images):
    original = Path(path)

    folder_name = str(original.parent.parent.name)
    out_original_dir = Path('out').joinpath(folder_name).joinpath('images')

    if not out_original_dir.exists():
        out_original_dir.mkdir(parents=True)

    out_original = out_original_dir.joinpath(original.name)
    shutil.copy(original, out_original)

    processed_filename = f'{original.stem}.png'
    processed_file = original.parent.parent.joinpath('processed').joinpath(processed_filename)

    mask_image(processed_file)
    print(f'Completed ==> {i + 1} / {total}')
