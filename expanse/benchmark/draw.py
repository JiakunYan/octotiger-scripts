import pandas as pd
import os,sys, json
from matplotlib import pyplot as plt
sys.path.append("../../include")
from draw_simple import *

job_tag = "total"
name = "20230110-" + job_tag
input_path = "data/"
all_labels = ["nnodes", "job", "parcelport", "nthreads", "level", "tag", "Time(s)"]

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

    # speedup
    ax2 = ax.twinx()
    for line in lines:
        if "mpi" in line["label"]:
            baseline = line["y"]
            break
    speedup_lines = []
    for line in lines:
        speedup = [float(b) / float(x) for x, b in zip(line["y"], baseline)]
        speedup_lines.append({"label": line["label"], "x": line["x"], "y": speedup})
        ax2.plot(line["x"], speedup, label=line['label'], marker='.', markerfacecolor='white', linestyle='dashed')
    ax2.set_ylabel("Speedup")
    # ax.legend(bbox_to_anchor = (1.05, 0.6))
    # ax2.legend()

    output_png_name = os.path.join("draw", "{}.png".format(title))
    fig.savefig(output_png_name)
    output_png_name = os.path.join("draw", "{}.json".format(title))
    with open(output_png_name, 'w') as outfile:
        json.dump({"Time": lines, "Speedup": speedup_lines}, outfile)

def batch(df):
    df1_tmp = df[df.apply(lambda row:
                          row["level"] == 6 and
                          row["tag"] != "nodreg",
                          axis=1)]
    df1 = df1_tmp.copy()
    df1["parcelport-tag"] = df1_tmp["parcelport"] +"-" + df1_tmp["tag"]
    plot(df1, "nnodes", "Time(s)", "parcelport-tag", name + "-detail")

    df2 = df[df.apply(lambda row:
                      row["level"] == 6 and
                      (((row["tag"] == job_tag) and
                      (row["parcelport"] == "lci")) or
                      (row["parcelport"] == "mpi")),
                      axis=1)]
    plot(df2, "nnodes", "Time(s)", "parcelport", name)

    df3 = df[df.apply(lambda row:
                      row["level"] == 7,
                      axis=1)]
    plot(df3, "nnodes", "Time(s)", "parcelport", name + "-l7")


if __name__ == "__main__":
    df = pd.read_csv(os.path.join(input_path, name + ".csv"))
    # interactive(df)
    batch(df)
