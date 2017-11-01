import matplotlib.pyplot as plt
from random import randint
from battle.maptools.point import Point

xs = [x - 0.5 for x in range(5)]
ys = [y - 0.5 for y in range(5)]

z = []
for _ in range(5):
    z.append([randint(1, 5) for _ in range(5)])

print(z)

fig, ax = plt.subplots()

im = ax.pcolormesh(xs, ys, z, alpha=0.3)
fig.colorbar(im)

ax.axis('tight')


top_plot = ax.plot([1, 2, 3], [1, 2, 3], 'r-o')

ax.set_xticks(range(0, 4), minor=False)
ax.set_yticks(range(0, 4), minor=False)
ax.set_xticks(xs, minor=True)
ax.set_yticks(ys, minor=True)
ax.grid(True, which='minor', linewidth=2)

pts = [Point(x, 3- x) for x in range(4)]
names = 'abcd'

ax.scatter([p.x for p in pts], [p.y for p in pts])
for index, name in enumerate(names):
    pt = pts[index]
    ax.annotate(name, (pt.x, pt.y))


# scatter = ax.scatter([], [])
# annotations = []
#
# from random import random
# def animate(thing, ann_lst, scatter):
#     # for el in ann_lst:
#     #     el.remove()
#     # sloppy move. it assigns the originally referenced list to empty. basically cheater's global
#     # done because FuncAnimation is passing the two objects again and again as fargs. They must be mutable. ugh!
#     # ann_lst[:] = []
#     while ann_lst:
#         el = ann_lst.pop()
#         el.remove()
#     pts = [(4*random(), 4*random()) for _ in range(5)]
#     scatter.set_offsets(pts)
#     for index, xy in enumerate(pts):
#         ann = ax.annotate(str(index), xy)
#         ann_lst.append(ann)
#     return scatter
#
# from matplotlib.animation import FuncAnimation
#
# ani = FuncAnimation(fig, animate, fargs=(annotations, scatter), frames=10, interval=500)



plt.show()
