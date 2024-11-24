import matplotlib.pyplot as plt

from animations.draw import DrawBoard


db = DrawBoard(None)

test = db.ax.text(1,1,"hei")
test.set_fontweight("bold")
test.set_fontsize(14)

plt.show()
