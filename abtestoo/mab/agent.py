import numpy as np

__all__ = ['BanditAgent']


class BanditAgent:
    def __init__(self, a=1, b=1):
        self.a = a
        self.b = b

    # baselines
    def equal_weights(self, state):
        res = np.array([1 / len(state) for i in range(len(state))])
        return res

    def randomize(self, state):
        res = np.random.rand(len(state))
        res /= res.sum()
        return res

    # stochastic policies
    def eps_greedy(self, state, t, start_eps=0.3, end_eps=0.01, gamma=0.99):
        eps = max(end_eps, start_eps * gamma**t)
        res = np.array([eps / len(state) for i in range(len(state))])
        best_idx = np.argmax([i[1] / i[0] for i in state]) if t > 0 else np.random.choice(range(len(state)))
        res[best_idx] += 1 - eps
        return res

    def softmax(self, state, t, start_tau=1e-1, end_tau=1e-4, gamma=0.9):
        tau = max(end_tau, start_tau * gamma**t)
        sum_exp = sum([np.exp(i[1] / (i[0] + 1e6) / tau) for i in state])
        res = np.array([np.exp(i[1] / (i[0] + 1e6) / tau) / sum_exp for i in state])
        return res

    # deterministic policies
    def ucb(self, state, t):
        for i in state:
            if i[0] == 0:
                return self.equal_weights(state)
        res = [(i[1] / i[0] + np.sqrt(2 * np.log(t + 1) / i[0])) for i in state]
        res = np.array(res)
        res_d = np.zeros(len(state))
        res_d[np.argmax(res)] = 1
        return res_d

    def thompson_deterministic(self, state):
        res = [np.random.beta(i[1] + self.a, i[0] - i[1] + self.b) for i in state]
        res = np.array(res)
        res_d = np.zeros(len(state))
        res_d[np.argmax(res)] = 1
        return res_d

    # thompson stochastic
    def thompson_one(self, state):
        res = [np.random.beta(i[1] + self.a, i[0] - i[1] + self.b) for i in state]
        res = np.array(res)
        return res

    def thompson_stochastic(self, state, n=1000):
        l = []
        for i in range(n):
            l.append(self.thompson_one(state)[None, :])
        l = np.concatenate(l, 0)
        is_max = l.max(1)[:, None] == l
        return is_max.mean(0)
