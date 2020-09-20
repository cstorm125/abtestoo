import numpy as np
import pandas as pd
from abtestoo.bayesian.proportions import value_remaining

__all__ = ['Arm', 'MusketeerEnv']


class Arm:
    def __init__(self, true_p):
        self.true_p = true_p
        self.reset()

    def reset(self):
        self.impressions = 0
        self.actions = 0

    def get_state(self):
        return self.impressions, self.actions

    def get_rate(self):
        return self.actions / self.impressions if self.impressions > 0 else 0.

    def pull(self):
        self.impressions += 1
        res = 1 if np.random.random() < self.true_p else 0
        self.actions += res
        return res


class MusketeerEnv:
    def __init__(self, true_ps, avg_impressions, a_list=None, b_list=None):
        self.true_ps = true_ps
        self.avg_impressions = avg_impressions
        self.nb_arms = len(true_ps)
        self.a_list, self.b_list = a_list, b_list
        if self.a_list is None:
            self.a_list = [1 for i in range(self.nb_arms)]
        if self.b_list is None:
            self.b_list = [1 for i in range(self.nb_arms)]
        self.reset()

    def reset(self):
        self.t = -1
        self.ds = []
        self.arms = [Arm(p) for p in self.true_ps]
        return self.get_state()

    def get_state(self):
        return [self.arms[i].get_state() for i in range(self.nb_arms)]

    def get_rates(self):
        return [self.arms[i].get_rate() for i in range(self.nb_arms)]

    def get_impressions(self):
        return int(np.random.triangular(self.avg_impressions / 2,
                                        self.avg_impressions,
                                        self.avg_impressions * 1.5))

    def step(self, ps):
        self.t += 1
        impressions = self.get_impressions()
        for i in np.random.choice(a=self.nb_arms, size=impressions, p=ps):
            self.arms[i].pull()
        self.record()
        return self.get_state()

    def record(self):
        d = {'t': self.t, 'max_rate': 0, 'opt_impressions': 0}
        for i in range(self.nb_arms):
            d[f'impressions_{i}'], d[f'actions_{i}'] = self.arms[i].get_state()
            d[f'rate_{i}'] = self.arms[i].get_rate()
            if d[f'rate_{i}'] > d['max_rate']:
                d['max_rate'] = d[f'rate_{i}']
                d['opt_impressions'] = d[f'impressions_{i}']
        d['total_impressions'] = sum([self.arms[i].impressions for i in range(self.nb_arms)])
        d['opt_impressions_rate'] = d['opt_impressions'] / d['total_impressions']
        d['total_actions'] = sum([self.arms[i].actions for i in range(self.nb_arms)])
        d['total_rate'] = d['total_actions'] / d['total_impressions']
        d['regret_rate'] = d['max_rate'] - d['total_rate']
        d['regret'] = d['regret_rate'] * d['total_impressions']
        c_list, n_list = [i[1] for i in self.get_state()], [i[0] for i in self.get_state()]
        d['value_remaining'] = value_remaining(c_list, n_list, self.a_list, self.b_list)
        self.ds.append(d)

    def show_df(self):
        df = pd.DataFrame(self.ds)
        cols = ['t'] + [f'rate_{i}' for i in range(self.nb_arms)] + \
               [f'impressions_{i}' for i in range(self.nb_arms)] + \
               [f'actions_{i}' for i in range(self.nb_arms)] + \
               ['total_impressions', 'total_actions', 'total_rate'] + \
               ['opt_impressions', 'opt_impressions_rate'] + \
               ['regret_rate', 'regret', 'value_remaining']
        df = df[cols]
        return df
