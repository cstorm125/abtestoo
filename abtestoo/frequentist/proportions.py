from typing import Tuple
import numpy as np
import scipy as sp
import pandas as pd
from plotnine import *
from mizani import *

__all__ = [
    'proportion_samples',
    'proportion_test',
    'proportion_ci',
    'proportion_plot'
]


def proportion_samples(mde: float, p: float, m: float = 1,
                       alpha: float = 0.05, mode: str = 'one_sided') -> float:
    '''
    :meth: get number of required sample based on minimum detectable difference (in absolute terms)
    :param float mde: minimum detectable difference
    :param float p: pooled probability of both groups
    :param float m: multiplier of number of samples; groups are n and nm
    :param float alpha: alpha
    :param str mode: mode of test; `one_sided` or `two_sided`
    :return: estimated number of samples to get significance
    '''
    variance = p * (1 - p)
    if mode == 'two_sided':
        z = sp.stats.norm.ppf(1 - alpha / 2)
    elif mode == 'one_sided':
        z = sp.stats.norm.ppf(1 - alpha)
    else:
        raise ValueError('Available modes are `one_sided` and `two_sided`')
    return (m + 1 / m) * variance * (z / mde)**2


def proportion_test(c1: int, c2: int,
                    n1: int, n2: int,
                    mode: str = 'one_sided') -> Tuple[float, float]:
    '''
    :meth: Z-test for difference in proportion
    :param int c1: conversions for group 1
    :param int c2: conversions for group 2
    :param int n1: impressions for group 1
    :param int n2: impressions for group 2
    :param str mode: mode of test; `one_sided` or `two_sided`
    :return: Z-score, p-value
    '''
    p = (c1 + c2) / (n1 + n2)
    p1 = c1 / n1
    p2 = c2 / n2
    z = (p1 - p2) / np.sqrt(p * (1 - p) * (1 / n1 + 1 / n2))
    if mode == 'two_sided':
        p = 2 * (1 - sp.stats.norm.cdf(abs(z)))
    elif mode == 'one_sided':
        p = 1 - sp.stats.norm.cdf(abs(z))
    else:
        raise ValueError('Available modes are `one_sided` and `two_sided`')
    return z, p


def proportion_ci(c: int, n: int, alpha: float = 0.05) -> Tuple[float, float]:
    '''
    :meth: calculate confidence interval at alpha
    :param int c: conversions 
    :param int n: impressions 
    :param float alpha: alpha
    :return: confidence interval at alpha
    '''
    p = c / n
    se = np.sqrt(p * (1 - p) / n)
    z = sp.stats.norm.ppf(1 - alpha / 2)
    return p - z * se, p + z * se


def proportion_plot(c1: int, c2: int,
                    n1: int, n2: int, alpha: float = 0.05,
                    mode: str = 'one_sided') -> None:
    '''
    :meth: plot Z-test for difference in proportion and confidence intervals for each campaign
    :param int c1: conversions for group 1
    :param int c2: conversions for group 2
    :param int n1: impressions for group 1
    :param int n2: impressions for group 2
    :param float alpha: alpha
    :param str mode: mode of test; `one_sided` or `two_sided`
    :return: None
    '''
    p = (c1 + c2) / (n1 + n2)
    p1 = c1 / n1
    p2 = c2 / n2
    se1 = np.sqrt(p1 * (1 - p1) / n1)
    se2 = np.sqrt(p2 * (1 - p2) / n2)
    z = sp.stats.norm.ppf(1 - alpha / 2)
    x1 = np.arange(p1 - 3 * se1, p1 + 3 * se1, 1e-4)
    x2 = np.arange(p2 - 3 * se2, p2 + 3 * se2, 1e-4)
    y1 = np.array([sp.stats.norm.pdf(i, loc=p1, scale=np.sqrt(p1 * (1 - p1) / n1)) for i in x1])
    y2 = np.array([sp.stats.norm.pdf(i, loc=p2, scale=np.sqrt(p2 * (1 - p2) / n2)) for i in x2])
    sm_df = pd.DataFrame({'campaign_id': ['Campaign A'] * len(x1) + ['Campaign B'] * len(x2),
                          'x': np.concatenate([x1, x2]), 'y': np.concatenate([y1, y2])})

    z_value, p_value = proportion_test(c1, c2, n1, n2, mode)
    print(f'Z-value: {z_value}; p-value: {p_value}')

    g = (ggplot(sm_df, aes(x='x', y='y', fill='campaign_id')) +
         geom_area(alpha=0.5)
         + theme_minimal() + xlab('Sample Mean Distribution of Each Campaign')
         + ylab('Probability Density Function')
         + geom_vline(xintercept=[p1 + se1 * z, p1 - se1 * z], colour='red')
         + geom_vline(xintercept=[p2+se2*z, p2-se2*z], colour='blue')
         + ggtitle(f'Confident Intervals at alpha={alpha}'))
    g.draw()
