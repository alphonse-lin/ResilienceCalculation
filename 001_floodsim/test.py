import numpy as np
import matplotlib.pyplot as plt

def logistic(r, x):
    return r * x * (1 - x)

n = 10000
r = np.linspace(2.5, 4.0, n)

iterations = 1000
last = 100

x = 1e-5 * np.ones(n)

lyapunov = np.zeros(n)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 9),
                               sharex=True)

for i in range(iterations)[:20]:
    x = logistic(r, x)
    lyapunov += np.log(abs(r - 2 * r * x))
    ax1.plot(r, x, ',k', alpha=.25)
    # if i >= (iterations - last):
    #     ax1.plot(r, x, ',k', alpha=.25)

ax1.set_xlim(2.5, 4)
ax1.set_title("Bifurcation diagram")

divergence = lyapunov / iterations

ax2.plot(r[divergence < 0], divergence[divergence < 0], ',k')
ax2.set_xlim(2.5, 4)
ax2.set_ylim(-2, 1)
ax2.set_title("Lyapunov exponent")

plt.tight_layout()
plt.show()