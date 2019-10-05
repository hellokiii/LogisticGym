from baselines.common import plot_util as pu
import matplotlib.pyplot as plt
import numpy as np

num = input()
results = pu.load_results('logs/single_ppo_092901')


r = results[0]
print(r.monitor.r)

plt.plot(np.cumsum(r.monitor['l']), pu.smooth(r.monitor['r'], radius=10))
plt.show()


# # plt.plot(r.progress.total_timesteps, r.progress.eprewmean)

