#!/usr/bin/env python3

import pandas as pd
import os,sys, json
from matplotlib import pyplot as plt
sys.path.append("../../include")
from draw_simple import *
import numpy as np
import itertools

job_name = "20231004-final"
input_path = "data/"
output_path = "draw/"

def plot(df, x_key, y_key, tag_key, title,
         filename = None, base = None, smaller_is_better = True, label_dict=None,
         with_error=True, sort_key=None, x_label=None, y_label=None, position="all"):
    if label_dict is None:
        label_dict = {}
    if x_label is None:
        x_label = x_key
    if y_label is None:
        y_label = y_key

    df = df.sort_values(x_key)

    fig, ax = plt.subplots(figsize=(4.8, 3.6))
    lines = parse_tag(df, x_key, y_key, tag_key)
    # update labels
    if label_dict:
        for line in lines:
            label = line["label"]
            if label in label_dict:
                line["label"] = label_dict[line["label"]]
        if base in label_dict:
            base = label_dict[base]

    if sort_key:
        lines.sort(key=sort_key)

    markers = itertools.cycle(('D', 'o', 'v', ',', '+'))
    # time
    for line in lines:
        print(line)
        line["marker"] = next(markers)
        if with_error:
            ax.errorbar(line["x"], line["y"], line["error"], label=line["label"], marker=line["marker"], markerfacecolor='white', capsize=3, markersize=8, linewidth=2)
        else:
            ax.plot(line["x"], line["y"], label=line["label"], marker=line["marker"], markerfacecolor='white', markersize=8, linewidth=2)
    ax.set_xlabel(x_label)
    if position == "left" or position == "all":
        ax.set_ylabel(y_label)
    ax.set_title(title)
    # ax.legend(bbox_to_anchor = (1.05, 0.6))
    # ax.legend()

    # speedup
    baseline = None
    ax2 = None
    speedup_lines = None
    for line in lines:
        if base == line["label"]:
            baseline = line
            break
    if baseline:
        ax2 = ax.twinx()
        speedup_lines = []
        for line in lines:
            if line['label'] == baseline['label']:
                ax2.plot(line["x"], [1 for x in range(len(line["x"]))], linestyle='dotted')
                continue
            if smaller_is_better:
                speedup = [float(x) / float(b) for x, b in zip(line["y"], baseline["y"])]
                label = "{} / {}".format(line['label'], baseline['label'])
            else:
                speedup = [float(b) / float(x) for x, b in zip(line["y"], baseline["y"])]
                label = "{} / {}".format(baseline['label'], line['label'])
            speedup_lines.append({"label": line["label"], "x": line["x"], "y": speedup})
            ax2.plot(line["x"], speedup, label=label, marker=line["marker"], markerfacecolor='white', linestyle='dotted', markersize=8, linewidth=2)
        if position == "right" or position == "all":
            ax2.set_ylabel("Speedup")
    # ax2.legend()

    # ask matplotlib for the plotted objects and their labels
    if ax2:
        lines1, labels1 = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax2.legend(lines1 + lines2, labels1 + labels2, loc=0)
    else:
        ax.legend()
    plt.tight_layout()

    if filename is None:
        filename = title

    if not os.path.exists(output_path):
        os.mkdir(output_path)
    dirname = os.path.join(output_path, job_name)
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    output_png_name = os.path.join(dirname, "{}.png".format(filename))
    fig.savefig(output_png_name, bbox_inches='tight')
    output_json_name = os.path.join(dirname, "{}.json".format(filename))
    with open(output_json_name, 'w') as outfile:
        json.dump({"Time": lines, "Speedup": speedup_lines}, outfile)

def batch(df):
    # Basic LCI v.s. MPI
    df1_tmp = df[df.apply(lambda row:
                          row["name"] in ["lci", "mpi_i", "mpi"] and
                          2 <= row["nnodes"] <= 32 and
                          row["max_level"] == 5,
                          axis=1)]
    df1 = df1_tmp.copy()
    label_dict = {
        "lci": "lci",
        "mpi_i": "mpi_i",
        "mpi": "mpi",
    }
    def sort_key(x):
        ordering = {
            "lci": 0,
            "mpi": 1,
            "mpi_i": 2,
        }
        return ordering[x["label"]]
    plot(df1, "nnodes", "Total(s)", "name", None, filename="brief",
         base="lci", with_error=True, label_dict=label_dict, sort_key=sort_key,
         x_label="Node Count", y_label="Time to Solution (s)", position="left")

    # Problem Size
    df1_tmp = df[df.apply(lambda row:
                          (row["name"] in ["lci", "mpi_i", "mpi"] or
                           "grid" in row["name"]) and
                          row["nnodes"] == 32 and
                          row["max_level"] == 5,
                          axis=1)]
    df1 = df1_tmp.copy()
    df1["name"] = df1.apply(lambda row: row["name"].split("-")[0],
                             axis=1)
    plot(df1, "griddim", "Total(s)", "name", None, filename="problem_size",
         base="lci", with_error=True, sort_key=sort_key,
         x_label="Grid Dimension", y_label="Time to Solution (s)", position="left")
    #
    # df1_tmp = df[df.apply(lambda row:
    #                       row["name"] in ["lci_worker_d2", "lci_wo_i", "lci_sendrecv", "lci_sync"] and
    #                       2 <= row["nnodes"] <= 32 and
    #                       row["max_level"] == 6,
    #                       axis=1)]
    # df1 = df1_tmp.copy()
    # label_dict = {
    #     "lci_worker_d2": "lci",
    # }
    # plot(df1, "nnodes", "Total(s)", "name", "Octo-Tiger on SDSC Expanse", filename="basic_variants",
    #      base="lci_worker_d2", with_error=True, label_dict=label_dict,
    #      x_label="Node Count", y_label="Time to Solution (s)")
    #
    # df1_tmp = df[df.apply(lambda row:
    #                       row["name"] in ["lci"] or "_d" in row["name"] and
    #                       2 <= row["nnodes"] <= 32 and
    #                       row["max_level"] == 6,
    #                       axis=1)]
    # df1 = df1_tmp.copy()
    # labels = ["lci_{}_d{}".format(t, n) for t in ["worker", "rp"] for n in [1, 2, 4]]
    # def sort_key(x):
    #     for i in range(len(labels)):
    #         if labels[i] == x["label"]:
    #             return i
    #     print("cannot find {} in {}".format(x, labels))
    #     exit(1)
    # plot(df1, "nnodes", "Total(s)", "name", "Octo-Tiger on SDSC Expanse", filename="device_prg",
    #      base="lci_worker_d2", with_error=True, sort_key=sort_key,
    #      x_label="Node Count", y_label="Time to Solution (s)")


if __name__ == "__main__":
    df = pd.read_csv(os.path.join(input_path, job_name + ".csv"))
    # interactive(df)
    batch(df)
