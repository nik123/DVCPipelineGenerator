import argparse
import os
import json
import hashlib
from typing import Iterable


def hash_bytestr_iter(bytesiter, hasher, ashexstr=False):
    for block in bytesiter:
        hasher.update(block)
    return hasher.hexdigest() if ashexstr else hasher.digest()


def file_as_blockiter(path, blocksize=65536):
    with open(path, 'rb') as f:
        block = f.read(blocksize)
        while len(block) > 0:
            yield block
            block = f.read(blocksize)


def generate_hash(paths: Iterable, hasher=None):
    if hasher is None:
        hasher = hashlib.sha256()

    def update_hasher(path, hasher):
        if os.path.isdir(path):
            paths = [f.path for f in os.scandir(path)]
            paths = sorted(paths)
            for p in paths:
                update_hasher(p, hasher)

        hash_bytestr_iter(file_as_blockiter(path), hasher)

    for p in paths:
        if not os.path.exists(p):
            raise ValueError("File doesn't exist at path: " + v)
        update_hasher(p, hasher)

    return hasher.hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--config_path',
        help='Path to configuration json',
        required=True)
    parser.add_argument(
        '--out_dir',
        help='Path to output dir. '
             'If "None" then result is saved in current working directory')

    args = parser.parse_args()
    config_path = args.config_path
    out_dir = args.out_dir
    if out_dir is None:
        out_dir = os.getcwd()

    with open(config_path, 'r') as f:
        pipeline_config = json.load(f)

    for name, stage in pipeline_config.items():
        out_path = os.path.join(out_dir, name + ".json")
        if 'paths' in stage:
            paths = sorted(stage['paths'].values())
            paths_hash = generate_hash(paths)
            stage['paths_hash'] = paths_hash

        with open(out_path, 'w') as f:
            json.dump(stage, f, ensure_ascii=False, indent=4)
            # Add newline character for better integration with Unix tools:
            print(end="\n", file=f)


if __name__ == '__main__':
    main()
