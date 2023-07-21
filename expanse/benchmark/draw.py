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

def plot(df, x_key, y_key, tag_key, title,
         filename = None, base = "mpi", label_dict=None,
         with_error=True, sort_key=None, x_label=None, y_label=None):
    if label_dict is None:
        label_dict = {}
    if x_label is None:
        x_label = x_key
    if y_label is None:
        y_label = y_key

    df = df.sort_values(x_key)

    fig, ax = plt.subplots()
    lines = parse_tag(df, x_key, y_key, tag_key)
    # update labels
    if label_dict:
        for line in lines:
            print(line)
            label = line["label"]
            if label in label_dict:
                line["label"] = label_dict[line["label"]]
        if base in label_dict:
            base = label_dict[base]

    if sort_key:
        lines.sort(key=sort_key)

    # time
    for line in lines:
        if with_error:
            ax.errorbar(line["x"], line["y"], line["error"], label=line["label"], marker='.', markerfacecolor='white', capsize=3)
        else:
            ax.plot(line["x"], line["y"], label=line["label"], marker='.', markerfacecolor='white')
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title)
    # ax.legend(bbox_to_anchor = (1.05, 0.6))
    # ax.legend()

    # speedup
    ax2 = ax.twinx()
    for line in lines:
        if base == line["label"]:
            baseline = line
            break
    speedup_lines = []
    for line in lines:
        if line['label'] == baseline['label']:
            continue
        speedup = [float(x) / float(b) for x, b in zip(line["y"], baseline["y"])]
        speedup_lines.append({"label": line["label"], "x": line["x"], "y": speedup})
        ax2.plot(line["x"], speedup, label="{} / {}".format(line['label'], baseline['label']), marker='.', markerfacecolor='white', linestyle='dashed')
    ax2.set_ylabel("Speedup")
    # ax2.legend()

    # ask matplotlib for the plotted objects and their labels
    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines1 + lines2, labels1 + labels2, loc=0)

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
        "mpi": "mpi-a",
        "mpi_sendimm": "mpi-i"
    }
    def sort_key(x):
        ordering = {
            "mpi-i": 0,
            "mpi-a": 1,
            "lci": 2,
        }
        return ordering[x["label"]]
    plot(df1, "nnodes", "Total(s)", "name", "Octo-Tiger on SDSC Expanse", filename="brief",
         base="lci", with_error=True, label_dict=label_dict, sort_key=sort_key,
         x_label="Node Count", y_label="Time to Solution (s)")


if __name__ == "__main__":
    df = pd.read_csv(os.path.join(input_path, job_name + ".csv"))
    df = df[all_labels]
    # interactive(df)
    batch(df)
