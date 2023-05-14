import re
import matplotlib.pyplot as plt
import numpy as np

input = '''
run/slurm_output.default.n32-lci_putsendrecv_queue_pthread.j22294200.out:   Total: 19.3064
run/slurm_output.default.n32-lci_putsendrecv_queue_pthread_sendimm.j22294203.out:   Total: 11.7135
run/slurm_output.default.n32-lci_putsendrecv_queue_rp.j22294201.out:   Total: 16.0902
run/slurm_output.default.n32-lci_putsendrecv_queue_rp_sendimm_bq.j22294210.out:   Total: 11.9239
run/slurm_output.default.n32-lci_putsendrecv_queue_rp_sendimm.j22294204.out:   Total: 11.4
run/slurm_output.default.n32-lci_putsendrecv_queue_rp_sendimm_nozcr.j22294215.out:   Total: 10.6841
run/slurm_output.default.n32-lci_putsendrecv_queue_worker.j22294199.out:   Total: 16.1692
run/slurm_output.default.n32-lci_putsendrecv_queue_worker_sendimm.j22294202.out:   Total: 10.6734
run/slurm_output.default.n32-lci_putsendrecv_sync_pthread.j22294194.out:   Total: 16.6097
run/slurm_output.default.n32-lci_putsendrecv_sync_pthread_sendimm.j22294197.out:   Total: 12.1827
run/slurm_output.default.n32-lci_putsendrecv_sync_rp.j22294195.out:   Total: 16.3188
run/slurm_output.default.n32-lci_putsendrecv_sync_rp_sendimm.j22294198.out:   Total: 11.304
run/slurm_output.default.n32-lci_putsendrecv_sync_worker.j22294193.out:   Total: 16.211
run/slurm_output.default.n32-lci_putsendrecv_sync_worker_sendimm.j22294196.out:   Total: 10.6275
run/slurm_output.default.n32-lci_putva_queue_rp_sendimm_2dev.j22294211.out:   Total: 11.0783
run/slurm_output.default.n32-lci_putva_queue_rp_sendimm.j22294207.out:   Total: 11.2634
run/slurm_output.default.n32-lci_putva_queue_worker_sendimm_2dev.j22294439.out:   Total: 11.4839
run/slurm_output.default.n32-lci_putva_queue_worker_sendimm.j22294438.out:   Total: 11.1414
run/slurm_output.default.n32-lci_putva_sync_worker.j22294205.out:   Total: 15.6771
run/slurm_output.default.n32-lci_putva_sync_worker_sendimm.j22294206.out:   Total: 11.3063
run/slurm_output.default.n32-lci_sendrecv_queue_pthread.j22294188.out:   Total: 19.4395
run/slurm_output.default.n32-lci_sendrecv_queue_pthread_sendimm.j22294191.out:   Total: 11.5432
run/slurm_output.default.n32-lci_sendrecv_queue_rp.j22294189.out:   Total: 15.5597
run/slurm_output.default.n32-lci_sendrecv_queue_rp_sendimm.j22294192.out:   Total: 11.3374
run/slurm_output.default.n32-lci_sendrecv_queue_worker.j22294187.out:   Total: 16.0377
run/slurm_output.default.n32-lci_sendrecv_queue_worker_post8.j22294518.out:   Total: 16.2777
run/slurm_output.default.n32-lci_sendrecv_queue_worker_sendimm.j22296941.out:   Total: 15.9905
run/slurm_output.default.n32-lci_sendrecv_queue_worker_sendimm_post8.j22294214.out:   Total: 13.2598
run/slurm_output.default.n32-lci_sendrecv_sync_pthread.j22294182.out:   Total: 17.4351
run/slurm_output.default.n32-lci_sendrecv_sync_pthread_sendimm.j22294185.out:   Total: 12.425
run/slurm_output.default.n32-lci_sendrecv_sync_rp.j22294183.out:   Total: 15.8255
run/slurm_output.default.n32-lci_sendrecv_sync_rp_sendimm.j22294186.out:   Total: 11.2372
run/slurm_output.default.n32-lci_sendrecv_sync_worker_bq.j22294208.out:   Total: 16.2953
run/slurm_output.default.n32-lci_sendrecv_sync_worker.j22294181.out:   Total: 15.0034
run/slurm_output.default.n32-lci_sendrecv_sync_worker_post8.j22294212.out:   Total: 16.0932
run/slurm_output.default.n32-lci_sendrecv_sync_worker_sendimm_bq.j22294209.out:   Total: 14.2505
run/slurm_output.default.n32-lci_sendrecv_sync_worker_sendimm.j22294184.out:   Total: 14.9211
run/slurm_output.default.n32-lci_sendrecv_sync_worker_sendimm_post8.j22294213.out:   Total: 14.3137
run/slurm_output.default.n32-mpi.j22294178.out:   Total: 13.9767
run/slurm_output.default.n32-mpi_nozcr.j22294180.out:   Total: 13.959
run/slurm_output.default.n32-mpi_sendimm.j22294179.out:   Total: 71.9159
'''

data = {}
pattern = "run\S+n32-(\S+)\.j.+Total\: (\S+)"
for line in input.split("\n"):
    print(line)
    m = re.match(pattern, line)
    if m:
        print(m.groups())
        task = m.groups()[0]
        time = float(m.groups()[1])
        data[task] = time
print(data)

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


def draw_bar(data, key_map, title, color_map=None, figsize=(10, 10)):
    x = []
    y = []
    color = []
    for key, name in key_map.items():
        if key not in data:
            print("{} is not in data!".format(key))
            exit(1)
        x.append(name)
        y.append(data[key])
        if color_map:
            color.append(color_map[name])
    fig, ax = plt.subplots(figsize=figsize)
    if color:
        bar = ax.barh(x, y, color=color)
    else:
        bar = ax.barh(x, y)
    for i, rect in enumerate(bar):
        ax.text(rect.get_width(), rect.get_y() + rect.get_height() / 2.0, f'{y[i]:.2f}', ha='left', va='center')
    ax.set_title(title)
    ax.invert_yaxis()  # labels read top-to-bottom
    # plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig("tmp/{}.png".format(title))


def list_to_dict(l):
    return {x: x for x in l}


key_map = list_to_dict(data.keys())
draw_bar(data, key_map, "all")

key_map = list_to_dict(["mpi", "lci_putva_queue_rp_sendimm"])
draw_bar(data, key_map, "mpi-lci")

keys = filter(data.keys(), ["_sendrecv", "_putsendrecv"])
color_map = {**{x: "C0" for x in keys if "_sendrecv" in x},
             **{x: "C1" for x in keys if "_putsendrecv" in x}}
draw_bar(data, list_to_dict(keys), "protocol", color_map=color_map)

keys = filter(data.keys(), ["sync", "queue"])
color_map = {**{x: "C0" for x in keys if "sync" in x},
             **{x: "C1" for x in keys if "queue" in x}}
draw_bar(data, list_to_dict(keys), "comp_type", color_map=color_map)

keys = filter(data.keys(), ["worker", "pthread", "rp"])
color_map = {**{x: "C0" for x in keys if "worker" in x},
             **{x: "C1" for x in keys if "pthread" in x},
             **{x: "C2" for x in keys if "rp" in x}}
draw_bar(data, list_to_dict(keys), "progress_type", color_map=color_map)

keys = filter(data.keys(), ["", "_sendimm"])
print(keys)
color_map = {**{x: "C0" for x in keys if "" in x},
             **{x: "C1" for x in keys if "_sendimm" in x}}
draw_bar(data, list_to_dict(keys), "sendimm", color_map=color_map)

keys = filter(data.keys(), ["", "_bq"])
print(keys)
color_map = {**{x: "C0" for x in keys if "" in x},
             **{x: "C1" for x in keys if "_bq" in x}}
draw_bar(data, list_to_dict(keys), "backlog_queue", color_map=color_map)

keys = filter(data.keys(), ["", "_post8"])
print(keys)
color_map = {**{x: "C0" for x in keys if "" in x},
             **{x: "C1" for x in keys if "_post8" in x}}
draw_bar(data, list_to_dict(keys), "prepost8", color_map=color_map)

keys = filter(data.keys(), ["putsendrecv", "putva"])
print(keys)
color_map = {**{x: "C0" for x in keys if "putsendrecv" in x},
             **{x: "C1" for x in keys if "putva" in x}}
draw_bar(data, list_to_dict(keys), "iovec", color_map=color_map)

keys = filter(data.keys(), ["", "_2dev"])
print(keys)
color_map = {**{x: "C0" for x in keys if "" in x},
             **{x: "C1" for x in keys if "_2dev" in x}}
draw_bar(data, list_to_dict(keys), "2dev", color_map=color_map)

keys = filter(data.keys(), ["", "_nozcr"])
print(keys)
color_map = {**{x: "C0" for x in keys if "" in x},
             **{x: "C1" for x in keys if "_nozcr" in x}}
draw_bar(data, list_to_dict(keys), "zero-copy receives", color_map=color_map)
#
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
