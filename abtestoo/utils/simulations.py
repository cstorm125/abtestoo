import numpy as np
import pandas as pd
from typing import Collection

__all__ = ['gen_bernoulli_campaign']


def gen_bernoulli_campaign(p1: float, p2: float,
                           lmh: Collection = [500, 1000, 1500],
                           timesteps: int = 60,
                           scaler: float = 300, seed: int = 1412) -> pd.DataFrame:
    '''
    :meth: generate fake impression-conversion campaign based on specified parameters
    :param float p1: true conversion rate of group 1
    :param float p2: true conversion rate of group 2
    :param Collection lmh: low-, mid-, and high-points for the triangular distribution of clicks
    :param int nb_days: number of timesteps the campaigns run for
    :param float scaler: scaler for Gaussian noise
    :param int seed: seed for Gaussian noise
    :return: dataframe containing campaign results
    '''

    np.random.seed(seed)
    ns = np.random.triangular(*lmh, size=timesteps * 2).astype(int)
    np.random.seed(seed)
    es = np.random.randn(timesteps * 2) / scaler

    n1 = ns[:timesteps]
    c1 = ((p1 + es[:timesteps]) * n1).astype(int)
    n2 = ns[timesteps:]
    c2 = ((p2 + es[timesteps:]) * n2).astype(int)
    result = pd.DataFrame({'timesteps': range(timesteps), 'impression_a': n1, 'conv_a': c1, 'impression_b': n2, 'conv_b': c2})

    result = result[['timesteps', 'impression_a', 'impression_b', 'conv_a', 'conv_b']]
    result['cumu_impression_a'] = result.impression_a.cumsum()
    result['cumu_impression_b'] = result.impression_b.cumsum()
    result['cumu_conv_a'] = result.conv_a.cumsum()
    result['cumu_conv_b'] = result.conv_b.cumsum()
    result['cumu_rate_a'] = result.cumu_conv_a / result.cumu_impression_a
    result['cumu_rate_b'] = result.cumu_conv_b / result.cumu_impression_b
    return result
