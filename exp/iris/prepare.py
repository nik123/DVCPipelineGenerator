import argparse
import subprocess
import os


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--dataset', required=True,
        help="Path to iris dataset")
    parser.add_argument(
        '--prepared', required=True,
        help="Path to transformed dataset prepared for training")
    args = parser.parse_args()

    dataset = args.dataset
    prepared = args.prepared

    parent_dir = os.path.split(prepared)[0]
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir)

    # We don't need to really prepare data. We just simulate data preparation
    # Therefore we just copy input "dataset" to "prepared"
    subprocess.run("cp {} {}".format(dataset, prepared), shell=True,
                   cwd=os.getcwd(), check=True)


if __name__ == '__main__':
    main()
