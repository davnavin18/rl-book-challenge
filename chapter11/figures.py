import argparse

from baird import BairdMDP
from baird_utils import b_baird, nab_vhat_baird, pi_baird, vhat_baird
import matplotlib.pyplot as plt
import numpy as np
from semi_grad_dp import SemiGradDP
from semi_grad_off_pol_td import SemiGradOffPolTD

plt.switch_backend('Qt5Agg')

BIG_FONT = 20
MED_FONT = 15

N_TIL = 4096
N_TLGS = 8

FIG_11_2_G = 0.99
FIG_11_2_ALP = 0.01
FIG_11_2_W_0 = [1, 1, 1, 1, 1, 1, 10, 1]
FIG_11_2_N_STEPS = 1000
FIG_11_2_BATCH = 10
FIG_11_2_N_RUNS_L = [1, 1]


def save_plot(filename, dpi=None):
  plt.savefig('plots/' + filename + '.png', dpi=dpi)


def plot_figure(ax, title, xticks, xnames, xlabel, yticks, ynames, ylabel,
                labelpad=15, font=MED_FONT, loc='upper left'):
  ax.set_title(title, fontsize=font)
  ax.set_xticks(xticks)
  ax.set_xticklabels(xnames)
  ax.set_yticks(yticks)
  ax.set_yticklabels(ynames)
  ax.set_xlim([min(xticks), max(xticks)])
  ax.set_ylim([min(yticks), max(yticks)])
  ax.set_xlabel(xlabel, fontsize=font)
  ax.set_ylabel(ylabel, rotation=0, fontsize=font, labelpad=labelpad)
  plt.legend(loc=loc)


def fig_11_2():
  fig = plt.figure()
  fig.set_size_inches(20, 28)
  fig.suptitle('Figure 11.2')
  env = BairdMDP()
  b, pi = [{(a, s): f(a, s) for a in env.moves for s in env.states}
           for f in [b_baird, pi_baird]]
  w_0 = np.array(FIG_11_2_W_0)
  baird_params = (w_0.shape[0], FIG_11_2_ALP, FIG_11_2_G, vhat_baird,
                  nab_vhat_baird)
  alg1 = SemiGradOffPolTD(env, pi, b, *baird_params)
  alg2 = SemiGradDP(env, pi, *baird_params)
  n_batches = FIG_11_2_N_STEPS // FIG_11_2_BATCH
  batch_ticks = FIG_11_2_BATCH * (np.arange(n_batches) + 1)
  for (i, alg) in enumerate([alg1, alg2]):
    ax = fig.add_subplot(f'12{i+1}')
    w_log = np.zeros((len(env.states) + 1, n_batches))
    for seed in range(FIG_11_2_N_RUNS_L[i]):
      if seed > 0 and seed % 10 == 0:
        print(f"[RUN #{seed}]")
      alg.w = w_0
      if i == 0:
        alg.seed(seed)
      for n_iter in range(n_batches):
        alg.pol_eva(FIG_11_2_BATCH)
        w_log[:, n_iter] = w_log[:, n_iter] + alg.w
    for (j, w_j) in enumerate(w_log):
      ax.plot(batch_ticks, w_j / FIG_11_2_N_RUNS_L[i], label=f'w_{j + 1}')
    xticks, yticks = [0, 1000], [1, 10, 100, 200, 300]
    ax_title = (f'Semi-gradient Off-Policy TD ({FIG_11_2_N_RUNS_L[i]} runs)'
                if i == 0 else 'Semi-Gradient DP')
    plot_figure(ax, ax_title, xticks, xticks, 'Steps' if i == 0 else 'Sweeps',
                yticks, yticks, '', labelpad=30)
    ax.legend()
  save_plot('fig11.2', dpi=100)
  plt.show()


PLOT_FUNCTION = {
  '11.2': fig_11_2,
}


def main():
  parser = argparse.ArgumentParser()

  parser.add_argument('figure', type=str, default=None,
                      help='Figure to reproduce.',
                      choices=list(PLOT_FUNCTION.keys()) + ['all'])
  args = parser.parse_args()
  if args.figure == 'all':
    for key, f in PLOT_FUNCTION.items():
      print(f"[{key}]")
      f()
  else:
    print(f"[{args.figure}]")
    PLOT_FUNCTION[args.figure]()


if __name__ == '__main__':
  main()
