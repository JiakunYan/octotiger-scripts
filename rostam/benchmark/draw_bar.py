import re
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os, sys
import json

job_tag = "more"
job_name = "20230714-" + job_tag
input_path = "data/"
all_labels = ["nnodes", "name", "Total(s)", "Computation(s)", "Regrid(s)"]

def filter(strings, keys, exclude=[]):
    common = None
    for key in keys:
        if key == "":
            continue
        selected = [x.replace(key, "{}") for x in strings if key in x]
        if common == None:
            common = selected
        else:
            common = [x for x in common if x in selected]
    results = []
    for string in common:
        skip = False
        for key in keys:
            if string.replace("{}", key) not in strings:
                skip = True
        if skip:
            continue
        for key in keys:
            results.append(string.replace("{}", key))
    for exclude_key in exclude:
        results = [x for x in results if exclude_key not in x]
    return results


def draw_bar(df, x_key, y_keys, title, x_include=None, color_map=None, filename=None):
    if type(y_keys) != list:
        y_keys = [y_keys]

    if x_include:
        xs = list(x_include)
    else:
        xs = list(df[x_key].unique())

    ys_dict = {}
    errors_dict = {}
    colors_dict = {}
    for y_key in y_keys:
        ys = []
        errors = []
        colors = []
        for x in xs:
            y = df[df[x_key] == x].mean(numeric_only=True)[y_key]
            error = df[df[x_key] == x].std(numeric_only=True)[y_key]
            if y is np.nan:
                continue
            if y == 0:
                continue
            ys.append(float(y))
            if not np.isnan(error):
                errors.append(float(error))
            if color_map:
                colors.append(color_map[x])
        ys_dict[y_key] = ys
        if len(errors) > 0:
            errors_dict[y_key] = errors
        colors_dict[y_key] = colors

    fig, ax = plt.subplots(figsize=(10, len(xs) * 0.3 + 1))
    bottom = np.zeros(len(xs))

    bar = None
    for y_key in y_keys:
        if colors_dict[y_key]:
            if len(errors_dict) > 0:
                bar = ax.barh(xs, ys_dict[y_key], xerr=errors_dict[y_key], color=colors_dict[y_key], edgecolor="black", left=bottom)
            else:
                bar = ax.barh(xs, ys_dict[y_key], color=colors_dict[y_key], edgecolor="black", left=bottom)
        else:
            if len(errors_dict) > 0:
                bar = ax.barh(xs, ys_dict[y_key], xerr=errors_dict[y_key], edgecolor="black", left=bottom)
            else:
                bar = ax.barh(xs, ys_dict[y_key], edgecolor="black", left=bottom)
        bottom += ys_dict[y_key]

    # Add actual number to the bar
    for i, rect in enumerate(bar):
        text = []
        total = 0
        for y_key in y_keys:
            total += ys_dict[y_key][i]
            text.append(f'{ys_dict[y_key][i]:.2f}')
        if len(text) > 1:
            text.append(f'{total:.2f}')
        text = "/".join(text)
        ax.text(bottom[i], rect.get_y() + rect.get_height() / 2.0,
                text, ha='left', va='center')
    ax.set_title(title)
    ax.invert_yaxis()  # labels read top-to-bottom
    plt.tight_layout()

    if filename is None:
        filename = title
    dirname = os.path.join("draw", job_name)
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    output_png_name = os.path.join(dirname, "{}.png".format(filename))
    fig.savefig(output_png_name)
    output_json_name = os.path.join(dirname, "{}.json".format(filename))
    with open(output_json_name, 'w') as outfile:
        json.dump({"xs": xs, "ys": ys_dict, "errors": errors_dict}, outfile)

def batch(df):
    df1_tmp = df[df.apply(lambda row:
                          row["nnodes"] == 15,
                          axis=1)]
    df1 = df1_tmp.copy()
    draw_bar(df1, "name", "Total(s)", "all")

    # keys = ["mpi", "lci_putva_queue_rp_sendimm"]
    # draw_bar(df, "name", "Total(s)", "mpi-lci", x_include=keys)
    #
    # keys = filter(list(df["name"]), ["_sendrecv", "_putsendrecv"])
    # print(keys)
    # color_map = {**{x: "C0" for x in keys if "_sendrecv" in x},
    #              **{x: "C1" for x in keys if "_putsendrecv" in x}}
    # draw_bar(df, "name", "Total(s)", "protocol", x_include=keys, color_map=color_map)
    #
    # keys = filter(list(df["name"]), ["sync", "queue"])
    # print(keys)
    # color_map = {**{x: "C0" for x in keys if "sync" in x},
    #              **{x: "C1" for x in keys if "queue" in x}}
    # draw_bar(df, "name", "Total(s)", "comp_type", x_include=keys, color_map=color_map)
    #
    # keys = filter(list(df["name"]), ["worker", "rp", "pthread"])
    # print(keys)
    # color_map = {**{x: "C0" for x in keys if "worker" in x},
    #              **{x: "C1" for x in keys if "rp" in x},
    #              **{x: "C2" for x in keys if "pthread" in x}}
    # draw_bar(df, "name", "Total(s)", "progress_type", x_include=keys, color_map=color_map)
    #
    # keys = filter(list(df["name"]), ["worker", "rp"])
    # print(keys)
    # color_map = {**{x: "C0" for x in keys if "worker" in x},
    #              **{x: "C1" for x in keys if "rp" in x}}
    # draw_bar(df, "name", "Total(s)", "progress_type2", x_include=keys, color_map=color_map)
    #
    # keys = filter(list(df["name"]), ["", "_sendimm"])
    # print(keys)
    # color_map = {**{x: "C0" for x in keys if "" in x},
    #              **{x: "C1" for x in keys if "_sendimm" in x}}
    # draw_bar(df, "name", "Total(s)", "sendimm", x_include=keys, color_map=color_map)
    #
    # keys = filter(list(df["name"]), ["", "_bq"])
    # print(keys)
    # color_map = {**{x: "C0" for x in keys if "" in x},
    #              **{x: "C1" for x in keys if "_bq" in x}}
    # draw_bar(df, "name", "Total(s)", "backlog_queue", x_include=keys, color_map=color_map)
    #
    # keys = filter(list(df["name"]), ["", "_post8"])
    # print(keys)
    # color_map = {**{x: "C0" for x in keys if "" in x},
    #              **{x: "C1" for x in keys if "_post8" in x}}
    # draw_bar(df, "name", "Total(s)", "prepost8", x_include=keys, color_map=color_map)

    # keys = filter(list(df["name"]), ["putsendrecv", "putva"])
    # print(keys)
    # color_map = {**{x: "C0" for x in keys if "putsendrecv" in x},
    #              **{x: "C1" for x in keys if "putva" in x}}
    # draw_bar(df, "name", "Total(s)", "iovec", x_include=keys, color_map=color_map)

    # keys = filter(list(df["name"]), ["", "_nozcr"])
    # print(keys)
    # color_map = {**{x: "C0" for x in keys if "" in x},
    #              **{x: "C1" for x in keys if "_nozcr" in x}}
    # draw_bar(df, "name", "Total(s)", "zero-copy receives", x_include=keys, color_map=color_map)
    #
    # keys = filter(list(df["name"]), ["", "_hash", "_mqueue"])
    # print(keys)
    # color_map = {**{x: "C0" for x in keys if "" in x},
    #              **{x: "C1" for x in keys if "_hash" in x},
    #              **{x: "C2" for x in keys if "_mqueue" in x}}
    # draw_bar(df, "name", "Total(s)", "match_table", x_include=keys, color_map=color_map)
    #
    # keys = [
    #     "mpi",
    #     "lci_sendrecv_sync_worker",
    #     "lci_putsendrecv_sync_worker",
    #     "lci_putva_sync_worker",
    #     "lci_sendrecv_queue_worker",
    #     "lci_sendrecv_sync_pthread",
    #     "lci_sendrecv_sync_rp",
    #     "lci_sendrecv_sync_worker_sendimm",
    # ]
    # print(keys)
    # draw_bar(df, "name", "Total(s)", "changeOne0", x_include=keys)
    #
    # keys = [
    #     "mpi",
    #     "lci_sendrecv_sync_worker_sendimm",
    #     "lci_putsendrecv_sync_worker_sendimm",
    #     "lci_putva_sync_worker_sendimm",
    #     "lci_sendrecv_queue_worker_sendimm",
    #     "lci_sendrecv_sync_pthread_sendimm",
    #     "lci_sendrecv_sync_rp_sendimm",
    #     "lci_sendrecv_sync_worker",
    # ]
    # print(keys)
    # draw_bar(df, "name", "Total(s)", "changeOne1", x_include=keys)
    #
    # keys = [
    #     "mpi",
    #     "lci_putsendrecv_queue_rp_sendimm",
    #     "lci_sendrecv_queue_rp_sendimm",
    #     "lci_putva_queue_rp_sendimm",
    #     "lci_putsendrecv_sync_rp_sendimm",
    #     "lci_putsendrecv_queue_worker_sendimm",
    #     "lci_putsendrecv_queue_pthread_sendimm",
    #     "lci_putsendrecv_queue_rp",
    # ]
    # print(keys)
    # draw_bar(df, "name", "Total(s)", "changeOne2", x_include=keys)
    # key_map = list_to_dict([
    #     "mpi",
    #     "lci_putva_queue_rp_sendimm",
    #     "lci_sendrecv_sync_worker",
    #     "lci_sendrecv_queue_worker",
    #     "lci_sendrecv_sync_rp",
    #     "lci_sendrecv_queue_rp",
    #     "lci_sendrecv_sync_rp_sendimm",
    #     "lci_sendrecv_queue_rp_sendimm",
    # ])
    # draw_bar(data, key_map, "comp_type")
    #
    # key_map = list_to_dict([
    #     "mpi",
    #     "lci_sendrecv_queue_rp_sendimm",
    #     "lci_putsendrecv_queue_rp_sendimm",
    #     "lci_putva_queue_rp_sendimm",
    # ])
    # draw_bar(data, key_map, "protocol")
    #
    # key_map = list_to_dict([
    #     "mpi",
    #     "lci_sendrecv_sync_worker",
    #     "lci_sendrecv_sync_worker_post8",
    #     "lci_sendrecv_queue_worker",
    #     "lci_sendrecv_queue_worker_post8",
    # ])
    # draw_bar(data, key_map, "prepost")


if __name__ == "__main__":
    df = pd.read_csv(os.path.join(input_path, job_name + ".csv"))
    df = df[all_labels]
    # interactive(df)
    batch(df)
