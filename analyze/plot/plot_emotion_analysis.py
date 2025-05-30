import matplotlib.pyplot as plt

labels = ['neutral', 'happy', 'sad', 'angry', 'surprise', 'fear', 'disgust', 'question']
sizes = [48.29, 9.02, 14.88, 5.37, 3.17, 14.15, 1.46, 3.66]
colors = ['#AEC6CF', '#FFD1DC', '#FFB347', '#77DD77', '#CFCFC4', '#FF6961', '#B39EB5', '#FDFD96']
explode = [0.03] * len(labels)

with plt.xkcd():
    fig, ax = plt.subplots(figsize=(6, 6), dpi=100)
    wedges, texts, autotexts = ax.pie(
        sizes,
        explode=explode,
        autopct='%1.2f%%',
        startangle=90,
        colors=colors,
        pctdistance=0.75,
        labeldistance=1.1,
        wedgeprops={'linewidth': 1, 'edgecolor': 'white'},
        textprops={'fontsize': 12}
    )
    ax.set_title('Emotion Distribution in Successful Prompts', fontsize=14)

    ax.legend(
        wedges,
        labels,
        title="Emotions",
        loc="center left",
        bbox_to_anchor=(1, 0.5),
        fontsize=11
    )

    ax.axis('equal')
    plt.tight_layout()
    plt.show()
