import pandas as pd
import os,sys, json
from matplotlib import pyplot as plt
sys.path.append("../../include")
from draw_simple import *
import numpy as np

job_tag = "all"
name = "20230522-" + job_tag
input_path = "data/"
all_labels = ["name", "Total(s)", "Computation(s)", "Regrid(s)"]

def plot(df, x_key, y_key, tag_key, filename, title = None, base = "mpi", label_dict=None, with_error=True):
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
        if base in label_dict:
            base = label_dict[base]

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
    for line in lines:
        if base == line["label"]:
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
    # df["tag"] = np.where((df["parcelport"] == "lci") & (df["tag"] == "default"), "default-numa", df["tag"])
    # df["tag"] = np.where((df["parcelport"] == "lci") & (df["tag"] == "numalocal"), "default", df["tag"])

    df1_tmp = df[df.apply(lambda row:
                          row["nnodes"] >= 2 and
                          row["level"] == 6 and
                          row["tag"] in ["numactl"],
                          axis=1)]
    df1 = df1_tmp.copy()
    plot(df1, "nnodes", "Time(s)", "parcelport", name + "-brief", title="MPI parcelport v.s. LCI parcelport",
         base="mpi", label_dict=label_dict, with_error=False)

    df1_tmp = df[df.apply(lambda row:
                          row["nnodes"] >= 2 and
                          row["level"] == 6 and
                          row["tag"] in ["default", "numactl"],
                          axis=1)]
    df1_tmp["tag"] = np.where((df1_tmp["tag"] == "default"), "local", df1_tmp["tag"])
    df1_tmp["tag"] = np.where((df1_tmp["tag"] == "numactl"), "interleave", df1_tmp["tag"])
    df1 = df1_tmp.copy()
    df1["parcelport-tag"] = df1_tmp["parcelport"] +"-" + df1_tmp["tag"]
    plot(df1, "nnodes", "Time(s)", "parcelport-tag", name + "-numa",
         title="Numa effect of the MPI and LCI parcelports", base="mpi-interleave",
         label_dict=label_dict, with_error=False)

    df1_tmp = df[df.apply(lambda row:
                          row["nnodes"] >= 2 and
                          row["level"] == 6 and
                          row["tag"] not in ["default", "with-libnuma"],
                          axis=1)]
    df1_tmp["tag"] = np.where((df1_tmp["tag"] == "numactl"), "default", df1_tmp["tag"])
    df1 = df1_tmp.copy()
    df1["parcelport-tag"] = df1_tmp["parcelport"] +"-" + df1_tmp["tag"]
    plot(df1, "nnodes", "Time(s)", "parcelport-tag", name + "-opt", title="LCI parcelport optimizations",
         base="mpi-default", label_dict=label_dict, with_error=False)

    # df2 = df[df.apply(lambda row:
    #                   row["level"] == 6 and
    #                   (((row["tag"] == job_tag) and
    #                   (row["parcelport"] == "lci")) or
    #                   (row["parcelport"] == "mpi")),
    #                   axis=1)]
    # plot(df2, "nnodes", "Time(s)", "parcelport", name)

    # df3 = df[df.apply(lambda row:
    #                   row["level"] == 7,
    #                   axis=1)]
    # plot(df3, "nnodes", "Time(s)", "parcelport", name + "-l7")


if __name__ == "__main__":
    df = pd.read_csv(os.path.join(input_path, name + ".csv"))
    df = df[all_labels]
    # interactive(df)
    batch(df)
