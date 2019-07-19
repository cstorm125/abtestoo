# abtest
A/B testing from scratch

## Frequentist Approach

See interactive notebook `frequentist.ipynb` / [Colab](https://colab.research.google.com/github/cstorm125/abtest/blob/master/frequentist_colab.ipynb) / [Kaggle Kernel](https://www.kaggle.com/cstorm3000/frequestist-a-b-testing-from-scratch?scriptVersionId=13219640)

Frequentist A/B testing is one of the most used and abused statistical methods in the world. This article starts with a simple problem of comparing two online ads campaigns (or teatments, user interfaces or slot machines). It outlines several useful statistical concepts and how we exploit them to solve our problem. At the end, it acknowledges some common pitfalls we face when doing a frequentist A/B test and proposes some possible solutions to a more robust A/B testing. Readers are encouraged to tinker with the widgets provided in order to explore the impacts of each parameter.

## Bayesian Approach

See interactive notebook `bayesian.ipynb` / [Kaggle Kernel](https://www.kaggle.com/cstorm3000/bayesian-a-b-testing-from-scratch)

We reuse the simple problem of comparing two online ads campaigns (or teatments, user interfaces or slot machines). We details how Bayesian A/B test is conducted and highlights the differences between it and the frequentist approaches. Readers are encouraged to tinker with the widgets provided in order to explore the impacts of each parameter.

## Multi-armed Bandits

See interactive notebook `mab.ipynb` / [Kaggle Kernel](https://www.kaggle.com/cstorm3000/multi-armed-bandits-from-scratch)

Frequentist and Bayesian A/B tests require you to divide your traffic into arbitrary groups for a period of time, then perform statistical tests based on the results. By definition, this forces us to divert out traffic to suboptimal variations during the test period, resulting in lower overall conversion rates. On the other hand, multi-barmed bandit appraoch (MAB) dynamically adjusts the percentage of traffic shown to each variation according to how they have performed so far during the test, resulting in smaller loss in conversion rates.

## Scripts
`stat_tests.py` - scripts containing some useful statistical functions

## Resources
* [N=10^9: Automated Experimentation at Scale](https://www.slideshare.net/optimizely/opti-con-2014-automated-experimentation-at-scale)
* [Big experiments: Big data’s friend for making decisions](https://www.facebook.com/notes/facebook-data-science/big-experiments-big-datas-friend-for-making-decisions/10152160441298859/)
* [Designing and Deploying Online Field Experiments](https://research.fb.com/publications/designing-and-deploying-online-field-experiments/)

## Thanks
* [korakot](https://github.com/korakot) for notebook conversion to run in Colab
