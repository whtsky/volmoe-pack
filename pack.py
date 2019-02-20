import sys
import re
import zipfile
import tempfile

from pathlib import Path

SUPPORTED_IMG_EXTENSIONS = ['jpg', 'jpeg', 'png']

if len(sys.argv) < 3:
    print("Usage: {} <base_path> <output_path> [episode-per-pack=5]".format(sys.argv[0]))

episode_number = re.compile("(\d+)")
def get_episode_number(path: Path):
    return episode_number.findall(path.name)[0]

base_path = Path(sys.argv[1])
output_path = Path(sys.argv[2])
output_path.mkdir(exist_ok=True)

episoide_per_pack = len(sys.argv) == 4 and int(sys.argv[3]) or 5


def glob_images(path: Path):
    files = []
    for ext in SUPPORTED_IMG_EXTENSIONS:
        files += path.glob("*.{}".format(ext))
    return sorted(files)


def grouper(folders):
    while folders:
        yield folders[:episoide_per_pack]
        folders = folders[episoide_per_pack:]


folders = sorted([x for x in base_path.iterdir() if x.is_dir()])
for group in grouper(folders):
    print(group)
    pack_name = "{}-{}".format(get_episode_number(group[0]), get_episode_number(group[-1]))
    print("Creating {}.zip".format(pack_name))
    zip_path = output_path / "{}.zip".format(pack_name)
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        navpoints = []
        for ep_folder in group:
            files = glob_images(ep_folder)
            # Add images
            for file in files:
                zf.write(str(file), ep_folder.name + '/' + file.name)
            # Add navpoint
            navpoints.append("{0},{0}={1}".format(ep_folder.name, files[0].name))
        zf.writestr('vol-navpoint.txt', '\n'.join(navpoints))
