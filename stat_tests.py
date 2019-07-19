import numpy as np
import scipy as sp

#frequentist
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

#bayesian
def sample_proportion(c,n,a=1,b=1,sim_size=100000): 
    return np.random.beta(c+a,n-c+b,sim_size)

def proportion_test_b(c1,c2,n1,n2,a1=1,a2=1,b1=1,b2=1,sim_size=100000):
    p1 = sample_proportion(c1,n1,a1,b1,sim_size)
    p2 = sample_proportion(c2,n2,a2,b2,sim_size)
    return (p1 > p2).mean()

def proportion_ratio(c1,c2,n1,n2,a1=1,a2=1,b1=1,b2=1,sim_size=100000):
    p1 = sample_proportion(c1,n1,a1,b1,sim_size)
    p2 = sample_proportion(c2,n2,a2,b2,sim_size)
    return p1/p2

def proportion_ci_b(c1,c2,n1,n2,p_value=0.05,a1=1,a2=1,b1=1,b2=1,sim_size=100000):
    ratios = proportion_ratio(c1,c2,n1,n2,a1,a2,b1,b2,sim_size)
    return np.quantile(ratios,[p_value/2,1-p_value/2])

def value_remaining(c1,c2,n1,n2,q=95,sim_size=100000,a1=1,a2=1,b1=9,b2=9):
    p1 = sample_proportion(c1,n1,a1,b1,sim_size)[:,None]
    p2 = sample_proportion(c2,n2,a2,b2,sim_size)[:,None]
    p = np.concatenate([p1,p2],1)
    p_max = p.max(1)
    best_idx = np.argmax([p1.mean(),p2.mean()])
    p_best = p[:,best_idx]
    vs = (p_max-p_best)/p_best
    return np.percentile(vs,q)