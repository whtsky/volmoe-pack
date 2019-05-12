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
    default="pack",
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


folders = sorted(
    [x for x in base_path.iterdir() if x.is_dir() and not x.name.startswith(".")]
)
for group in grouper(folders):
    print(group)
    pack_name = "{}-{}".format(
        get_episode_number(group[0]), get_episode_number(group[-1])
    )
    print("Creating {}.zip".format(pack_name))
    zip_path = output_path / "{}.zip".format(pack_name)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        navpoints = []
        group_pad_width = max(len(str(len(group))), 3)
        for i, ep_folder in enumerate(group):
            files = glob_images(ep_folder)
            if len(set(map(len, [x.stem for x in files]))) not in (0, 1):
                raise Exception("文件名数字序号长度需要保持一致\n%s" % "\n".join(map(str, files)))
            file_pad_width = max(len(str(len(files))), 3)
            folder_name = str(i).zfill(group_pad_width)
            first_filename = "0".zfill(file_pad_width) + files[0].suffix
            # Add images
            for file_i, file in enumerate(files):
                filename = str(file_i).zfill(file_pad_width) + file.suffix
                zf.write(str(file), folder_name + "/" + filename)
            # Add navpoint
            navpoints.append(
                "{ep_name},{folder_name}={file_name}".format(
                    ep_name=ep_folder.name,
                    folder_name=folder_name,
                    file_name=first_filename,
                )
            )
        zf.writestr("vol-navpoint.txt", "\n".join(navpoints))
