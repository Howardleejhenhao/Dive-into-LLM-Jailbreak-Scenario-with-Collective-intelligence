import matplotlib.pyplot as plt
import numpy as np

# 三個階段的數據
phase_labels = ['declarative', 'question', 'command', 'exclamation']
early_sizes = [48.7, 39.7, 7.1, 4.5]
mid_sizes   = [43.3, 41.0, 6.7, 9.0]
late_sizes  = [55.0, 26.7, 9.2, 9.2]

colors = ['#AEC6CF', '#FFB347', '#77DD77', '#FF6961']
explode = [0.03] * 4

with plt.xkcd():
    fig, axes = plt.subplots(1, 3, figsize=(15, 5), dpi=100)
    phases = ['EARLY Phase', 'MID Phase', 'LATE Phase']
    all_sizes = [early_sizes, mid_sizes, late_sizes]

    for ax, phase, sizes in zip(axes, phases, all_sizes):
        wedges, texts, autotexts = ax.pie(
            sizes,
            explode=explode,
            autopct='%1.1f%%',
            startangle=90,
            colors=colors,
            pctdistance=0.75,
            labeldistance=1.1,
            wedgeprops={'linewidth': 1, 'edgecolor': 'white'},
            textprops={'fontsize': 11}
        )
        ax.set_title(phase, fontsize=14)
        ax.axis('equal')

    fig.suptitle('Sentence Type Distribution Across Phases', fontsize=18, y=0.95)

    fig.legend(
        wedges, phase_labels,
        title="Sentence Types",
        loc="lower center",
        ncol=4,
        fontsize=12,
        frameon=False,
        bbox_to_anchor=(0.5, -0.02)
    )

    plt.tight_layout(rect=[0, 0.05, 1, 0.93])
    plt.show()
