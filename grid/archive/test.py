import grid as gd

import matplotlib.pyplot as plt
from matplotlib import patches
from matplotlib.lines import Line2D

import warnings
warnings.filterwarnings("ignore")

grid = gd.GRID()
grid.run(pathImg="/Users/jameschen/Dropbox/James_Git/FN/data/demo.png",
         lsSelect=[0, 1], valShad=0, valSmth=5,
         nRow=11, nCol=7, plot=True)


grid = gd.GRID()
grid.loadData("/Users/jameschen/Dropbox/James_Git/FN/data/demo.png", plot=True)
grid.binarizeImg(lsSelect=[0, 1], valShad=0, valSmth=5, plot=True)
grid.findPlots(nRow=11, nCol=7, plot=True)
grid.cpuSeg(plot=True)

# display seg
# Create figure and axes
fig, ax = plt.subplots(1)
# Display the image
ax.imshow(grid.imgs.get('visSeg'))
for row in range(11):
    for col in range(7):
        recAg = grid.agents.get(row=row, col=col).getQRect()
        rect = patches.Rectangle(
            (recAg.x(), recAg.y()), recAg.width(), recAg.height(),
            linewidth=1, edgecolor='r', facecolor='none')
        ax.add_patch(rect)

plt.show()

# preview for fin
fig, ax = plt.subplots()
ax.imshow(grid.imgs.get('visSeg'))
for row in range(11):
    for col in range(7):
        agent = grid.agents.get(row=row, col=col)
        recAg = agent.getQRect()
        line1, line2 = pltCross(agent.x, agent.y, width=1)
        rect = patches.Rectangle(
            (recAg.x(), recAg.y()), recAg.width(), recAg.height(),
            linewidth=1, edgecolor='r', facecolor='none')
        ax.add_line(line1)
        ax.add_line(line2)
        ax.add_patch(rect)

plt.show()

plt.imshow(grid.imgs.get("raw"))

pltImShow(grid.imgs.get("raw"))

pltSegPlot(grid.agents, grid.imgs.get("visSeg"))
