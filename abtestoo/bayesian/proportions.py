from typing import Tuple, Collection
import numpy as np
import scipy as sp
import pandas as pd
from plotnine import *
from mizani import *

__all__ = [
    'sample_proportion',
    'proportion_test_b',
    'proportion_ratio',
    'proportion_diff',
    'proportion_ci_b',
    'value_remaining'
]


def sample_proportion(c: int, n: int,
                      a: float = 1, b: float = 1,
                      sim_size: int = 100000) -> np.array:
    '''
    :meth: sample proportions from a posterior 
    :param int c: number of conversions
    :param int n: number of impressions
    :param float a: alpha of prior
    :param float b: beta of prior
    :param int sim_size: times to run simulation
    :return: proportions sampled from the posterior
    '''
    return np.random.beta(c + a, n - c + b, sim_size)


def proportion_test_b(c1: int, c2: int, n1: int, n2: int,
                      a1: float = 1, a2: float = 1,
                      b1: float = 1, b2: float = 1,
                      sim_size: int = 100000) -> float:
    '''
    :meth: test proportions based on Monte Carlo simulation of the posteriors
    :param int c1: number of conversions from group 1
    :param int c2: number of conversions from group 2
    :param int n1: number of impressions from group 1
    :param int n2: number of impressions from group 2
    :param float a: alpha of prior from group 1
    :param float a: alpha of prior from group 2
    :param float b: beta of prior from group 1
    :param float b: beta of prior from group 2
    :param int sim_size: times to run simulation
    :return: probability that A is superior to B according to Monte Carlo simulation
    '''
    p1 = sample_proportion(c1, n1, a1, b1, sim_size)
    p2 = sample_proportion(c2, n2, a2, b2, sim_size)
    return (p1 > p2).mean()


def proportion_ratio(c1: int, c2: int,
                     n1: int, n2: int,
                     a1: float = 1, a2: float = 1,
                     b1: float = 1, b2: float = 1,
                     sim_size: int = 100000) -> float:
    '''
    :meth: ratio of the proportions based on Monte Carlo simulation of the posteriors
    :param int c1: number of conversions from group 1
    :param int c2: number of conversions from group 2
    :param int n1: number of impressions from group 1
    :param int n2: number of impressions from group 2
    :param float a: alpha of prior from group 1
    :param float a: alpha of prior from group 2
    :param float b: beta of prior from group 1
    :param float b: beta of prior from group 2
    :param int sim_size: times to run simulation
    :return: an array containing simulated ratios drawn from the posteriors of group 1 over group 2
    '''
    p1 = sample_proportion(c1, n1, a1, b1, sim_size)
    p2 = sample_proportion(c2, n2, a2, b2, sim_size)
    return p1 / p2


def proportion_diff(c1: int, c2: int,
                    n1: int, n2: int,
                    a1: float = 1, a2: float = 1,
                    b1: float = 1, b2: float = 1,
                    sim_size: int = 100000) -> float:
    '''
    :meth: difference in p based on Monte Carlo simulation of the posteriors
    :param int c1: number of conversions from group 1
    :param int c2: number of conversions from group 2
    :param int n1: number of impressions from group 1
    :param int n2: number of impressions from group 2
    :param float a: alpha of prior from group 1
    :param float a: alpha of prior from group 2
    :param float b: beta of prior from group 1
    :param float b: beta of prior from group 2
    :param int sim_size: times to run simulation
    :return: an array containing simulated differences drawn from the posteriors of group 1 over group 2
    '''
    p1 = sample_proportion(c1, n1, a1, b1, sim_size)
    p2 = sample_proportion(c2, n2, a2, b2, sim_size)
    return p1 - p2


def proportion_plot_b(c1: int, c2: int,
                      n1: int, n2: int, alpha: float = 0.05,
                      mode: str = 'ratio',
                      a1: float = 1, a2: float = 1,
                      b1: float = 1, b2: float = 1,
                      sim_size: int = 100000) -> None:
    '''
    :meth: plot Bayesian test for proportions and credible campaigns for ratio or difference
    :param int c1: number of conversions from group 1
    :param int c2: number of conversions from group 2
    :param int n1: number of impressions from group 1
    :param int n2: number of impressions from group 2
    :param float alpha: alpha
    :param str mode: plot `ratio` or `difference` between conversion rates of group 1 and group 2
    :param float a: alpha of prior from group 1
    :param float a: alpha of prior from group 2
    :param float b: beta of prior from group 1
    :param float b: beta of prior from group 2
    :param int sim_size: times to run simulation
    :return: value remaining in the experi
    '''
    if mode == 'ratio':
        ps = proportion_ratio(c1, c2, n1, n2, a1, a2, b1, b2, sim_size)
    elif mode == 'difference':
        ps = proportion_diff(c1, c2, n1, n2, a1, a2, b1, b2, sim_size)
    else:
        raise ValueError('Available modes are `ratio` and `difference`')

    ci = np.quantile(ps, [alpha / 2, 1 - alpha / 2])
    print(f'Probability that A is better than B: {proportion_test_b(c1,c2,n1,n2,a1,a2,b1,b2,sim_size)}')
    print(f'Average {mode} of A and B: {np.mean(ps)}')
    print(f'Credible interval: {ci}')

    g = (ggplot(pd.DataFrame({'value': [np.percentile(ps, i) for i in range(101)], 'percentile': range(101)}), aes(x='value', y='percentile')) +
         geom_line() +
         geom_vline(xintercept=ci, color='green') +
         theme_minimal() + ylab('Cumulative Distribution Function') + xlab(f'{mode} of A and B')
         )
    if mode == 'ratio':
        g = g + geom_vline(xintercept=1, color='red')
    elif mode == 'difference':
        g = g + geom_vline(xintercept=0, color='red')
    else:
        raise ValueError('Available modes are `ratio` and `difference`')
    g.draw()


def value_remaining(c_list: Collection[int],
                    n_list: Collection[int],
                    a_list: Collection[float], b_list: Collection[float],
                    q: int = 95, sim_size: int = 100000) -> float:
    '''
    :meth: calculate `q`th percentile of value remaining based experiments
    :param int c_list: a list of number of conversions
    :param int n_list: a list of number of impressions
    :param float a_list: a list of alphas of priors 
    :param float b_list: a list of betas of priors
    :param int q: which quantile of value remaining to output
    :param int sim_size: times to run simulation
    :return: `q`th percentile  of value remaining in the experiment
    '''
    p = np.concatenate([sample_proportion(*x, sim_size)[:, None] for x in zip(c_list, n_list, a_list, b_list)], 1)
    p_max = p.max(1)
    best_idx = np.argmax(p.mean(0))
    p_best = p[:, best_idx]
    vs = (p_max - p_best) / p_best
    return np.percentile(vs, q)
