from matplotlib.figure import Figure
from matplotlib.patches import Circle


def create_figure_user_donut(user_count, options):
    colormap = [
        "#FF6384CC",
        "#36A2EBCC",
        "#4BC0C0CC",
        "#9966FFCC",
        "#FF9F40CC",
        "#FFCE56CC"
    ] # move to global properties further!
    fig = Figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.pie(
        user_count,
        explode=[0.005 for i in options],
        labels=[str(i) + '\n' + f"{j:,d}" for i,j in zip(options, user_count)],
        colors=[colormap[i] for i,j in enumerate(options)],
        labeldistance=1.1,
        autopct='%3.1f%%',
        pctdistance=0.5,
        textprops={"fontsize": 12}
    )
    ax.axis("equal")
    ax.legend(options, loc=3, fontsize=12)
    # add total:
    ax.text(-0.15, -0.1, f" Total \n{sum(user_count):,d}", size=13)
    # add white circle
    tmp_circle = Circle( (0,0), 0.7, color='white')
    ax.add_artist(tmp_circle)
    return fig