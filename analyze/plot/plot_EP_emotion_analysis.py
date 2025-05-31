import matplotlib.pyplot as plt
import numpy as np

phase_labels = ['neutral', 'happy', 'sad', 'angry', 'surprise', 'fear', 'disgust', 'question']
early_pct  = [79/156*100, 12/156*100, 20/156*100, 8/156*100, 5/156*100, 26/156*100, 2/156*100, 4/156*100]
mid_pct    = [56/134*100, 20/134*100, 16/134*100, 8/134*100, 2/134*100, 21/134*100, 3/134*100, 8/134*100]
late_pct   = [63/120*100, 5/120*100, 25/120*100, 6/120*100, 6/120*100, 11/120*100, 1/120*100, 3/120*100]

colors = ['#AEC6CF', '#FFD1DC', '#FFB347', '#77DD77', '#CFCFC4', '#FF6961', '#B39EB5', '#FDFD96']
explode = [0.02] * len(phase_labels)

with plt.xkcd():
    fig, axes = plt.subplots(1, 3, figsize=(15, 5), dpi=100)
    phases = ['Early (156 msgs)', 'Mid (134 msgs)', 'Late (120 msgs)']
    all_pct = [early_pct, mid_pct, late_pct]

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
            textprops={'fontsize': 10}
        )
        ax.set_title(phase, fontsize=14)
        ax.axis('equal')

    fig.suptitle('Emotion Analysis by Phase (Successful Attacks)', fontsize=18, y=0.92)

    fig.legend(
        wedges, phase_labels,
        title="Emotions",
        loc="lower center",
        ncol=8,
        fontsize=11,
        frameon=False,
        bbox_to_anchor=(0.5, 0.02)
    )

    plt.tight_layout(rect=[0, 0.05, 1, 0.88])
    plt.show()
