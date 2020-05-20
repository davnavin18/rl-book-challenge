import numpy as np
from utils import gen_traj_ret

class GradientMC:
  def __init__(self, env, alpha, w_dim):
    self.env = env
    self.a = alpha
    self.d = w_dim
    self.reset()

  def seed(self, seed):
    self.env.seed(seed)
    np.random.seed(seed)

  def pol_eva(self, pi, vhat, nab_vhat, n_ep, gamma):
    for run in range(n_ep):
      if run > 0 and run % 1000 == 0:
        print(f"run #{run}")
      for (s, G) in gen_traj_ret(self.env, pi, gamma):
        self.mu[s] += 1
        self.w += self.a * (G - vhat(s, self.w)) * nab_vhat(s, self.w)
    self.mu /= self.mu.sum()

  def reset(self):
    self.w = np.zeros(self.d)
    self.mu = np.zeros(len(self.env.states))
