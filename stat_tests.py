import numpy as np
import scipy as sp

def proportion_test(c1, c2, n1, n2, mode = 'two_sided'):
    p = (c1+c2) / (n1+n2)
    p1 = c1 / n1
    p2 = c2 / n2
    z = (p1-p2) / np.sqrt(p*(1-p)*(1/n1 + 1/n2))
    if mode=='two_sided':
        p = 2*(1-sp.stats.norm.cdf(abs(z)))
    elif mode=='one_sided':
        p = 1-sp.stats.norm.cdf(abs(z))
    else:
        raise ValueError('Available modes are `one_sided` and `two_sided`')
    return z, p

def proportion_ci(c,n, p_value=0.05):
    p = c/n
    se = np.sqrt(p*(1-p)/n)
    z = sp.stats.norm.ppf(1-p_value/2)
    return p-z*se, p, p+z*se