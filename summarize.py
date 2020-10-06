import pandas as pd
import yaml
from datetime import timedelta, datetime
from argparse import ArgumentParser
from pathlib import Path


REPO = Path('/Users/marlena/repos/time-tracker')


def main():

    parser = ArgumentParser()
    parser.add_argument('--start', type=str, required=False)
    parser.add_argument('--end', type=str, required=False)
    parser.add_argument('--last', type=int, required=False)
    args = parser.parse_args()

    if args.last and (args.start or args.end):
        raise RuntimeError()

    with open(REPO / 'cfg.yml') as file:
        settings = yaml.load(file, Loader=yaml.FullLoader)
        outfile = settings['out_file'][0]

    df = pd.read_csv(outfile)

    df['start'] = pd.to_datetime(df['start'])
    df['end'] = pd.to_datetime(df['end'])

    if args.start:
        start = pd.to_datetime(args.start)
        df = df.loc[df.start >= start]
    if args.end:
        end = pd.to_datetime(args.end)
        df = df.loc[df.end <= end]
    if args.last is not None:
        delta = timedelta(args.last)
        df = df.loc[df.start >= datetime.now() - delta]

    df['total'] = df['end'] - df['start']
    df['hours'] = df.total.dt.total_seconds() / 3600

    df = df[['item', 'hours']]
    groups = df.groupby('item')['hours'].sum()
    groups.sort_values(ascending=False, inplace=True)
    print("\n")
    print(f"Total {round(groups.sum(), 2)} HOURS")
    print("--------------------")
    print(groups)


if __name__ == '__main__':
    main()
