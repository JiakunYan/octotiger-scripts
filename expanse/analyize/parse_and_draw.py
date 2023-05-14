import glob
import re
import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate

name="lci_sendrecv_sync_worker_sendimm"
input_file = "run-lci_sendrecv_sync_worker_sendimm/octotiger_trace.lci_sendrecv_sync_worker_sendimm.0.log"
if __name__ == "__main__":
    with open(input_file, "r") as infile:
        lines = infile.readlines()

    pattern = "(?P<rank>\d+):(?P<start_time>\S+):send_connection\((?P<p>\S+)\) start:(?P<nzc_size>\d+):(?P<tchunk_size>\d+):(?P<zc_num>\d+):\[(?P<chunks>\S+)?\]"
    start_time_list = []
    nzc_size_list = []
    tchunk_size_list = []
    zc_num_list = []
    chunks_list = []
    count = 0
    percent = 0
    for line in lines:
        if float(len(lines)) * percent / 10 <= count:
            percent += 1
            print("{}/{}".format(count, len(lines)))
        count += 1
        m = re.match(pattern, line)
        if not m:
            continue
        start_time_list.append(float(m.group("start_time")))
        nzc_size_list.append(int(m.group("nzc_size")))
        if int(m.group("zc_num")) > 0:
            tchunk_size_list.append(int(m.group("tchunk_size")))
        zc_num_list.append(int(m.group("zc_num")))
        if m.group("chunks"):
            for chunk in m.group("chunks").split(","):
                chunks_list.append(int(chunk))

    def stat_and_draw(ax, name, data):
        if len(data) == 0:
            return
        data_np = np.array(data)
        ax.hist(data, bins=200)
        ax.set_title(name)
        return [name, len(data_np), data_np.mean(), data_np.std(), data_np.min(), data_np.max()]
    fig, axs = plt.subplots(2, 3, figsize=(20, 10))
    data = []
    data.append(stat_and_draw(axs[0][0], "start time", start_time_list))
    data.append(stat_and_draw(axs[0][1], "nzc chunk size", nzc_size_list))
    data.append(stat_and_draw(axs[0][2], "tchunk size", tchunk_size_list))
    data.append(stat_and_draw(axs[1][0], "zc chunk number", zc_num_list))
    data.append(stat_and_draw(axs[1][1], "zc chunk size", chunks_list))
    axs[1][2].set_axis_off()

    # def format_text(headers, data):
    #     format_row = "{:>12}" * (len(headers) + 1) + "\n"
    #     text = format_row.format("", *headers)
    #     for entry in data:
    #         text += format_row.format("", *entry)
    #     return text
    text = tabulate(data, headers=["Name", "Count", "Mean", "STD", "Min", "Max"])
    # text = format_text(["Name", "Count", "Mean", "STD", "Min", "Max"], data)
    print(text)
    axs[1][2].text(0, 0, text, fontsize = 10)
    plt.tight_layout()
    plt.savefig("draw/{}.png".format(name))


