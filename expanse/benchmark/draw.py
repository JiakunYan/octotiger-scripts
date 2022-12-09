import pandas as pd
import os,sys, json
from matplotlib import pyplot as plt
sys.path.append("../../include")
from draw_simple import *

name = "all"
input_path = "data/"
all_labels = ["nnodes", "job", "parcelport", "nthreads", "level", "Computation Time(s)"]

def plot(df, x_key, y_key, tag_key, title):
    fig, ax = plt.subplots()
    lines = parse_tag(df, x_key, y_key, tag_key)
    for line in lines:
        print(line)
        ax.errorbar(line["x"], line["y"], line["error"], label=line['label'], marker='.', markerfacecolor='white', capsize=3)
    ax.set_xlabel(x_key)
    ax.set_ylabel(y_key)
    ax.set_title(title)
    # ax.legend(bbox_to_anchor = (1.05, 0.6))
    ax.legend()
    output_png_name = os.path.join("draw", "{}.png".format(title))
    fig.savefig(output_png_name)
    output_png_name = os.path.join("draw", "{}.json".format(title))
    with open(output_png_name, 'w') as outfile:
        json.dump(lines, outfile)

def batch(df):
    plot(df, "nnodes", "Computation Time(s)", "parcelport", "20221207-merge-data-tchunk")

if __name__ == "__main__":
    df = pd.read_csv(os.path.join(input_path, name + ".csv"))
    # interactive(df)
    batch(df)
