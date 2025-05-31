import matplotlib.pyplot as plt

# Data
labels = ['Polite', 'Direct', 'None']
counts = [255, 123, 32]
total = 410
pct = [c / total * 100 for c in counts]

colors = ['#AEC6CF', '#FFB347', '#FF6961']
explode = [0.02] * len(labels)

with plt.xkcd():
    fig, ax = plt.subplots(figsize=(6, 6), dpi=100)
    wedges, texts, autotexts = ax.pie(
        pct,
        labels=labels,
        explode=explode,
        autopct='%1.1f%%',
        startangle=90,
        colors=colors,
        wedgeprops={'linewidth': 1, 'edgecolor': 'white'},
        textprops={'fontsize': 12}
    )
    ax.set_title('Categories (Successful Attacks)', fontsize=16)
    ax.axis('equal')
    plt.tight_layout()
    plt.show()
