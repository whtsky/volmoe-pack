#!/usr/bin/env python3
import sys
import re
import zipfile
import tempfile
import argparse
import itertools

from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("base_path", type=str, help="")
parser.add_argument("-o", "--output_path", help="where to store generated zip files")
parser.add_argument(
    "-e",
    "--episode-per-pack",
    type=int,
    help="how many episode per zip pack",
    default=5,
)
parser.add_argument(
    "-t",
    "--trailing",
    choices=["merge", "ignore", "pack"],
    help="how to deal with trailing volumes",
    default="pack"
)

args = parser.parse_args()

SUPPORTED_IMG_EXTENSIONS = ["jpg", "jpeg", "png"]

episode_number = re.compile("(\d+)")


def get_episode_number(path: Path):
    return episode_number.findall(path.name)[0]


base_path = Path(args.base_path)
output_path = args.output_path and Path(args.output_path) or Path(args.base_path)
output_path.mkdir(exist_ok=True)

episoide_per_pack = args.episode_per_pack


def glob_images(path: Path):
    files = []
    for ext in SUPPORTED_IMG_EXTENSIONS:
        files += path.glob("*.{}".format(ext))
    return sorted(files)


def grouper(folders):
    while folders:
        if len(folders) < episoide_per_pack * 2 and args.trailing == "merge":
            yield folders
            return
        yield folders[:episoide_per_pack]
        folders = folders[episoide_per_pack:]
        if len(folders) < episoide_per_pack and args.trailing == "ignore":
            return


def check_image_file_length(folders):
    files = list(itertools.chain(*map(glob_images, folders)))
    if len(set(map(len, [x.stem for x in files]))) not in (0, 1):
        raise Exception("文件名数字序号长度需要保持一致\n%s" % "\n".join(map(str, files)))


folders = sorted(
    [x for x in base_path.iterdir() if x.is_dir() and not x.name.startswith(".")]
)
check_image_file_length(folders)
for group in grouper(folders):
    print(group)
    pack_name = "{}-{}".format(
        get_episode_number(group[0]), get_episode_number(group[-1])
    )
    print("Creating {}.zip".format(pack_name))
    zip_path = output_path / "{}.zip".format(pack_name)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        navpoints = []
        for ep_folder in group:
            files = glob_images(ep_folder)
            # Add images
            for file in files:
                zf.write(str(file), ep_folder.name + "/" + file.name)
            # Add navpoint
            navpoints.append("{0},{0}={1}".format(ep_folder.name, files[0].name))
        zf.writestr("vol-navpoint.txt", "\n".join(navpoints))
