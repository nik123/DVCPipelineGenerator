import argparse
import os
import json
import hashlib
import yaml
from typing import Iterable
from functools import reduce


def dvc_command(stage, out_dir):
    stage_path = os.path.join(out_dir, stage["name"] + ".dvc")
    cmd = stage["cmd"]
    dvc_cmd = "dvc run -f " + stage_path

    def generate_params(param, param_type):
        if "cached" in param and param["cached"] == False:
            param_type = param_type.upper()
        paths = param["paths"]
        if isinstance(paths, str):
            paths = [paths]

        dvc_param = ""
        for p in paths:
            dvc_param += " " + param_type + " " + p
        if "arg" in param:
            cmd_param = reduce(
                lambda x, y: x + " " + y,
                [" " + param["arg"], *paths])
        else:
            cmd_param = ""

        return (dvc_param, cmd_param)

    if "deps" in stage:
        for dep in stage["deps"]:
            params = generate_params(dep, "-d")
            dvc_cmd += params[0]
            cmd += params[1]

    if "outs" in stage:
        for out in stage["outs"]:
            params = generate_params(out, "-o")
            dvc_cmd += params[0]
            cmd += params[1]

    if "metrics" in stage:
        for metric in stage["metrics"]:
            params = generate_params(metric, '-m')
            dvc_cmd += params[0]
            cmd += params[1]

    if "args" in stage:
        for arg in stage["args"]:
            cmd += " " + arg

    full_cmd = dvc_cmd + " " + cmd

    if os.path.exists(stage_path):
        with open(stage_path, 'r') as f:
            d = yaml.safe_load(f)
            if d["cmd"] == cmd:
                full_cmd = "dvc repro " + stage_path

    return full_cmd


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--config_path',
        help='Path to configuration file for pipeline',
        required=True)
    parser.add_argument(
        '--out_dir',
        help='Path to output dir. '
             'If "None" then result is saved in same dir with config')

    args = parser.parse_args()
    config_path = args.config_path
    out_dir = args.out_dir
    if out_dir is None:
        out_dir = os.path.split(args.config_path)[0]

    with open(config_path, 'r') as f:
        pipeline_config = yaml.safe_load(f)

    for stage in pipeline_config["stages"]:
        dvc_cmd = dvc_command(stage, out_dir)
        print(dvc_cmd)


if __name__ == '__main__':
    main()
