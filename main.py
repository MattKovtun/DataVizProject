# https://think.cs.vt.edu/corgis/csv/music/music.html

import pandas as pd

FIELDS_OF_INTEREST = ["artist.name", "song.hotttnesss", "tempo", "terms", "year", "title"]


def select_specifics(filename):
    df = pd.read_csv(filename)
    df = df[FIELDS_OF_INTEREST]
    return df


if __name__ == "__main__":
    filename = "music.csv"
    df = select_specifics(filename)
    print(df.head())

    ars = df["terms"].tolist()
    summary = dict()

    for a in ars:
        summary[a] = summary.get(a, 0) + 1

    pp = [(key, summary[key]) for key in summary]
    pp.sort(key=lambda x: x[1], reverse=True)
    print(pp)


