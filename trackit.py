import yaml
import pandas as pd
import numpy as np
from pathlib import Path
import os
from datetime import datetime
from argparse import ArgumentParser


REPO = Path('/Users/marlena/repos/time-tracker')


def start(item, outfile):
    df = pd.DataFrame({
        'item': [item],
        'start': [datetime.now()],
        'end': np.nan
    }, index=[0])
    if os.path.exists(outfile):
        old = pd.read_csv(outfile)
        if not old.loc[(old.end.isnull()), 'end'].empty:
            raise RuntimeError("Need to end the previous session for this item!")
        df = pd.concat([old, df], axis=0).reset_index(drop=True)
    df.to_csv(outfile, index=False)


def end(outfile):
    df = pd.read_csv(outfile)
    if df.loc[(df.end.isnull()), 'end'].empty:
        raise RuntimeError("Need to start a session for this item!")
    df.loc[(df.end.isnull()), 'end'] = datetime.now()
    df.to_csv(outfile, index=False)


def main():

    parser = ArgumentParser()
    parser.add_argument('--item', type=str, required=False)
    args = parser.parse_args()

    with open(REPO / 'cfg.yml') as file:
        settings = yaml.load(file, Loader=yaml.FullLoader)
        items = settings['items']
        outfile = settings['out_file'][0]

    if args.item:
        if args.item not in items:
            raise RuntimeError("Unrecognized item {args.item}."
                               "List of available items is {items}.")

    if args.item:
        start(args.item, outfile)
    else:
        end(outfile)


if __name__ == '__main__':
    main()
