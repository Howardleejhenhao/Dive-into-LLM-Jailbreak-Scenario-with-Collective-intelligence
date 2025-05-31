import matplotlib.pyplot as plt
import numpy as np

# Data
modality_labels = ['factual', 'suggestion', 'hypothetical', 'conditional']
early_counts = [0, 3, 0, 153]
mid_counts   = [2, 6, 0, 126]
late_counts  = [0, 7, 0, 113]

early_pct = [c / 156 * 100 for c in early_counts]
mid_pct   = [c / 134 * 100 for c in mid_counts]
late_pct  = [c / 120 * 100 for c in late_counts]

colors = ['#AEC6CF', '#FFB347', '#77DD77', '#FF6961']
explode = [0.02] * len(modality_labels)

with plt.xkcd():
    fig, axes = plt.subplots(1, 3, figsize=(15, 5), dpi=100)
    phases = ['Early (n=156)', 'Mid (n=134)', 'Late (n=120)']
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
        ax.set_title(f'Modality: {phase}', fontsize=14)
        ax.axis('equal')
    
    fig.suptitle('Modality Distribution by Phase', fontsize=18, y=0.92)
    
    fig.legend(
        wedges, modality_labels,
        title="Modalities",
        loc="lower center",
        ncol=4,
        fontsize=12,
        frameon=False,
        bbox_to_anchor=(0.5, 0.02)
    )
    
    plt.tight_layout(rect=[0, 0.05, 1, 0.88])
    plt.show()
