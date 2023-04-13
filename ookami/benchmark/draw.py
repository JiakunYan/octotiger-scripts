import pandas as pd
import os,sys, json
from matplotlib import pyplot as plt
sys.path.append("../../include")
from draw_simple import *
import numpy as np

job_tag = "first"
name = "20230330-" + job_tag
input_path = "data/"
all_labels = ["nnodes", "job", "parcelport", "nthreads", "level", "tag", "Time(s)"]

def plot(df, x_key, y_key, tag_key, filename, title = None, baseline = None, label_dict=None, with_error=True):
    if label_dict is None:
        label_dict = {}
    if title == None:
        title = filename

    fig, ax = plt.subplots()
    lines = parse_tag(df, x_key, y_key, tag_key)
    # update labels
    if label_dict != None:
        for line in lines:
            print(line)
            label = line["label"]
            if label in label_dict:
                line["label"] = label_dict[line["label"]]

    # time
    for line in lines:
        if with_error:
            ax.errorbar(line["x"], line["y"], line["error"], label=line["label"], marker='.', markerfacecolor='white', capsize=3)
        else:
            ax.plot(line["x"], line["y"], label=line["label"], marker='.', markerfacecolor='white')
    ax.set_xlabel(x_key)
    ax.set_ylabel(y_key)
    ax.set_title(title)
    # ax.legend(bbox_to_anchor = (1.05, 0.6))
    ax.legend()

    # speedup
    ax2 = ax.twinx()
    map_label_line = {}
    for line in lines:
        map_label_line[line["label"]] = line
    speedup_lines = []
    if baseline != None:
        for line in lines:
            baseline_label = baseline(line["label"])
            assert(line["x"] == map_label_line[baseline_label]["x"])
            speedup = [float(b) / float(x) for x, b in zip(line["y"], map_label_line[baseline_label]["y"])]
            speedup_lines.append({"label": line["label"], "x": line["x"], "y": speedup})
            ax2.plot(line["x"], speedup, label=line['label'], marker='.', markerfacecolor='white', linestyle='dashed')
    ax2.set_ylabel("Speedup")
    # ax.legend(bbox_to_anchor = (1.05, 0.6))
    # ax2.legend()

    output_png_name = os.path.join("draw", "{}.png".format(filename))
    fig.savefig(output_png_name)
    output_json_name = os.path.join("draw", "{}.json".format(filename))
    with open(output_json_name, 'w') as outfile:
        json.dump({"Time": lines, "Speedup": speedup_lines}, outfile)

def batch(df):
    label_dict={
        "lci-no-sendimm-bq": "lci w/o lock bypass",
        "lci-nobq": "lci w/o backlog queue",
        "lci-1dev": "lci w/o 2 progress threads",
        "lci-default": "lci parcelport",
        "mpi-default": "mpi parcelport",
        "lci-interleave": "lci w/ numa interleave",
        "lci-local": "lci w/ numa local",
        "mpi-interleave": "mpi w/ numa interleave",
        "mpi-local": "mpi w/ numa local",
    }

    df1_tmp = df[df.apply(lambda row:
                          row["nnodes"] >= 2 and
                          row["tag"] in ["default"],
                          axis=1)]
    df1 = df1_tmp.copy()
    df1["parcelport-level"] = df1_tmp["parcelport"] + "-" + df1_tmp["level"].astype(str)
    def baseline_fn(label):
        return label.replace("lci", "mpi")
    plot(df1, "nnodes", "Time(s)", "parcelport-level", name + "-brief", title="MPI parcelport v.s. LCI parcelport",
         baseline=baseline_fn, label_dict=label_dict, with_error=False)


if __name__ == "__main__":
    df = pd.read_csv(os.path.join(input_path, name + ".csv"))
    # interactive(df)
    batch(df)
