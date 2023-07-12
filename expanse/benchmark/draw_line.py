import pandas as pd
import os,sys, json
from matplotlib import pyplot as plt
sys.path.append("../../include")
from draw_simple import *
import numpy as np

job_tag = "paper"
job_name = "20230712-" + job_tag
input_path = "data/"
all_labels = ["name", "nnodes", "max_level", "Total(s)", "Computation(s)", "Regrid(s)"]

def plot(df, x_key, y_key, tag_key, title, filename = None, base = "mpi", label_dict=None, with_error=True):
    if label_dict is None:
        label_dict = {}
    df = df.sort_values(x_key)

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

    if filename is None:
        filename = title
    dirname = os.path.join("draw", job_name)
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    output_png_name = os.path.join(dirname, "{}.png".format(filename))
    fig.savefig(output_png_name)
    output_json_name = os.path.join(dirname, "{}.json".format(filename))
    with open(output_json_name, 'w') as outfile:
        json.dump({"Time": lines, "Speedup": speedup_lines}, outfile)

def batch(df):

    df1_tmp = df[df.apply(lambda row:
                          row["name"] in ["lci", "mpi_sendimm", "mpi"] and
                          row["nnodes"] >= 2 and
                          row["max_level"] == 6,
                          axis=1)]
    df1 = df1_tmp.copy()
    label_dict = {
        "mpi": "mpi-nosendimm",
        "mpi_sendimm": "mpi"
    }
    plot(df1, "nnodes", "Total(s)", "name", "MPI parcelport v.s. LCI parcelport", filename="brief",
         base="mpi_sendimm", with_error=True, label_dict=label_dict)


if __name__ == "__main__":
    df = pd.read_csv(os.path.join(input_path, job_name + ".csv"))
    df = df[all_labels]
    # interactive(df)
    batch(df)
