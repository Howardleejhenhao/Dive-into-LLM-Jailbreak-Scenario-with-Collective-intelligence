import matplotlib.pyplot as plt
import numpy as np

# Politeness data
politeness_labels = ['Polite', 'Direct', 'None']
early_counts = [99, 43, 14]
mid_counts   = [75, 43, 16]
late_counts  = [81, 37, 2]

early_pct = [c / 156 * 100 for c in early_counts]
mid_pct   = [c / 134 * 100 for c in mid_counts]
late_pct  = [c / 120 * 100 for c in late_counts]

colors = ['#AEC6CF', '#FFB347', '#FF6961']
explode = [0.02] * len(politeness_labels)

with plt.xkcd():
    fig, axes = plt.subplots(1, 3, figsize=(15, 5), dpi=100)
    phases = ['Early (156 msgs)', 'Mid (134 msgs)', 'Late (120 msgs)']
    all_pct = [early_pct, mid_pct, late_pct]

    for ax, phase, pct in zip(axes, phases, all_pct):
        wedges, _, autotexts = ax.pie(
            pct,
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

    fig.suptitle('Politeness Distribution by Phase', fontsize=18, y=0.93)

    fig.legend(
        wedges, politeness_labels,
        title="Politeness",
        loc="lower center",
        ncol=3,
        fontsize=12,
        frameon=False,
        bbox_to_anchor=(0.5, 0.02)
    )

    plt.tight_layout(rect=[0, 0.1, 1, 0.9])
    plt.show()
