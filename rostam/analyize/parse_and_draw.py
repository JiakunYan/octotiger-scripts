import glob
import re
import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate

name="lci-dim8"
input_file = "run-{}/octotiger_trace.{}.0.log".format(name, name)
# input_file2 = "run-{}/slurm_output.default.n32-{}.*.out".format(name, name)
if __name__ == "__main__":
    # filenames = glob.glob(input_file2)
    # assert len(filenames) == 1
    # with open(filenames[0], "r") as infile:
    #     lines = infile.readlines()
    # pattern = "Time scope (?P<scope>\d+) (?P<action>\S+) at (?P<time>\S+) s"
    # time_scope = {}
    # for line in lines:
    #     m = re.match(pattern, line)
    #     if not m:
    #         continue
    #     scope = m.group("scope")
    #     action = m.group("action")
    #     time = float(m.group("time"))
    #     if scope not in time_scope:
    #         time_scope[scope] = []
    #     if action == "start":
    #         time_scope[scope].append([time])
    #     else:
    #         time_scope[scope][-1].append(time)

    with open(input_file, "r") as infile:
        lines = infile.readlines()

    pattern = ".* (?P<rank>\d+):(?P<start_time>\S+):send_connection\((?P<p>\S+)\) start:(?P<nzc_size>\d+):(?P<tchunk_size>\d+):(?P<zc_num>\d+):\[(?P<chunks>\S+)?\]"
    start_time_list = []
    nzc_size_list = []
    tchunk_size_list = []
    zc_num_list = []
    chunks_list = []
    total_size_list = []
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
        total_size = 0
        start_time_list.append(float(m.group("start_time")))
        nzc_size_list.append(int(m.group("nzc_size")))
        total_size += int(m.group("nzc_size"))
        if int(m.group("zc_num")) > 0:
            tchunk_size_list.append(int(m.group("tchunk_size")))
            total_size += int(m.group("tchunk_size"))
        zc_num_list.append(int(m.group("zc_num")))
        if m.group("chunks"):
            for chunk in m.group("chunks").split(","):
                chunks_list.append(int(chunk))
                total_size += int(chunk)
        total_size_list.append(total_size)

    def stat_and_draw(ax, name, data):
        if len(data) == 0:
            return [name, 0, 0, 0, 0, 0]
        data_np = np.array(data)
        ax.hist(data, bins=200)
        ax.set_title(name)
        return [name, len(data_np), data_np.mean(), data_np.std(), data_np.min(), data_np.max()]


    def draw_trend(ax, name, time, data):
        if len(data) == 0:
            return
        time_np = np.array(time)
        data_np = np.array(data)
        base_time = np.min(time_np)
        time_np -= base_time
        duration = np.max(time_np)
        print(duration)
        n, bins, patches = ax.hist(time_np, bins=int(duration / 0.1))
        trend_x = []
        trend_y = []
        start = 0
        for i in range(len(bins) - 1):
            print(bins[i])
            print(n[i])
            num = int(n[i])
            trend_x.append((bins[i] + bins[i+1]) / 2)
            trend_y.append(data_np[start:start + num - 1].sum())
            start += num
        print(trend_x)
        print(trend_y)
        ax2 = ax.twinx()
        ax2.plot(trend_x, trend_y, color="C1", label="total")
        ax.set_title(name)
    fig, axs = plt.subplots(2, 3, figsize=(20, 10))
    data = []
    draw_trend(axs[0][0], "message size trend", start_time_list, total_size_list)
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
    print(data)
    text = tabulate(data, headers=["Name", "Count", "Mean", "STD", "Min", "Max"])
    # text = format_text(["Name", "Count", "Mean", "STD", "Min", "Max"], data)
    print(text)
    axs[1][2].text(0, 0, text, fontsize = 10)
    plt.tight_layout()
    plt.savefig("draw/{}.png".format(name))


