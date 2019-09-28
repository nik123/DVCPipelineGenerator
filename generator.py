import argparse
import os
import json
import hashlib
from typing import Iterable


def dvc_command(stage, out_dir):
    stage_path = os.path.join(out_dir, stage["name"] + ".dvc")
    cmd = stage["cmd"]
    dvc_cmd = "dvc run -f " + stage_path

    def generate_params(param, param_type):
        if "cached" in param and param["cached"] == False:
            param_type = param_type.upper()

        dvc_param = " " + param_type + " " + param["path"]
        if "arg" in param:
            cmd_param = " " + param["arg"] + " " + param["path"]

        return (dvc_param, cmd_param)

    for dep in stage["deps"]:
        params = generate_params(dep, "-d")
        dvc_cmd += params[0]
        cmd += params[1]

    for out in stage["outs"]:
        params = generate_params(out, "-o")
        dvc_cmd += params[0]
        cmd += params[1]

    for metric in stage["metrics"]:
        params = generate_params(metric, '-m')
        dvc_cmd += params[0]
        cmd += params[1]

    return dvc_cmd + " " + cmd


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

    for stage in pipeline_config["stages"]:
        dvc_cmd = dvc_command(stage, out_dir)
        print(dvc_cmd)


if __name__ == '__main__':
    main()
