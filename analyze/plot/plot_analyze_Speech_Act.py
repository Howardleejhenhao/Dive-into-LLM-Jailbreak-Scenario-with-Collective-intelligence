import matplotlib.pyplot as plt

labels = ['declarative', 'question', 'command', 'exclamation']
sizes = [48.8, 36.3, 7.6, 7.3]

with plt.xkcd():
    fig, ax = plt.subplots(figsize=(6, 6), dpi=100)
    wedges, texts, autotexts = ax.pie(
        sizes, 
        labels=labels, 
        autopct='%1.1f%%', 
        startangle=90, 
        colors=['#AEC6CF', '#FFB347', '#77DD77', '#FF6961'],
        textprops={'fontsize': 12}
    )
    ax.set_title('Sentence Type Distribution (Successful Attacks)', fontsize=14)
    ax.axis('equal')
    plt.tight_layout()
    plt.show()
