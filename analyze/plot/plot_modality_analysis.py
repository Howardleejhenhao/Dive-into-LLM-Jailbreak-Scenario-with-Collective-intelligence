import matplotlib.pyplot as plt
import numpy as np

modality_labels = ['factual', 'suggestion', 'hypothetical', 'conditional']
succ_counts = [2, 16, 0, 392]
succ_total = 410
fail_counts = [9, 150, 5, 1184]
fail_total = 1348

succ_pct = [c / succ_total * 100 for c in succ_counts]
fail_pct = [c / fail_total * 100 for c in fail_counts]

colors = ['#AEC6CF', '#FFB347', '#77DD77', '#FF6961']
explode = [0.02] * len(modality_labels)

with plt.xkcd():
    fig, axes = plt.subplots(1, 2, figsize=(12, 6), dpi=100)
    phases = [f'Successful ({succ_total})', f'Failed ({fail_total})']
    all_pct = [succ_pct, fail_pct]

    for ax, phase, pct in zip(axes, phases, all_pct):
        wedges, texts, autotexts = ax.pie(
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

    fig.suptitle('Modality Distribution: Successful vs Failed Attacks', fontsize=18, y=0.92)

    fig.legend(
        wedges, modality_labels,
        title="Modalities",
        loc="lower center",
        ncol=4,
        fontsize=12,
        frameon=False,
        bbox_to_anchor=(0.5, 0.05)
    )

    plt.tight_layout(rect=[0, 0.1, 1, 0.88])
    plt.show()
