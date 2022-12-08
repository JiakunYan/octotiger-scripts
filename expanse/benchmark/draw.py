import pandas as pd
import os,sys
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
        ax.errorbar(line["x"], line["y"], line["error"], label=line['label'], marker='.', markerfacecolor='white', capsize=3)
    ax.set_xlabel(x_key)
    ax.set_ylabel(y_key)
    ax.set_title(title)
    # ax.legend(bbox_to_anchor = (1.05, 0.6))
    ax.legend()
    output_png_name = os.path.join("draw", "{}.png".format(title))
    fig.savefig(output_png_name)

def batch(df):
    plot(df, "nnodes", "Computation Time(s)", "parcelport", "all")

if __name__ == "__main__":
    df = pd.read_csv(os.path.join(input_path, name + ".csv"))
    # interactive(df)
    batch(df)
