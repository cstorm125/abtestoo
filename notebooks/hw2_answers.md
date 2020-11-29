# Homework #2 - A/B Testing in the Wild

1. The Law of Large Numbers (LLN) says that sample mean will converge to expectation as sample size grows. Assuming that this is true, prove that sample variance will converge to variance as sample size grows. 

\begin{align}
s^2 &= \frac{1}{n}\sum_{i=1}^{n}(X_i - \bar{X}^2) \\
&= \frac{1}{n}\sum_{i=1}^{n}(X_i - \mu)^2 \text{; as }n\rightarrow\infty\text{ }\bar{X}\rightarrow\mu\\
&=\frac{1}{n}(\sum_{i=1}^{n}{X_i}^2 - 2\mu\sum_{i=1}^{n}X_i + n\mu^2) \\
&=\frac{\sum_{i=1}^{n}{X_i}^2}{n} - \frac{2\mu\sum_{i=1}^{n}X_i}{n} + \mu^2 \\
&= \frac{\sum_{i=1}^{n}{X_i}^2}{n} - 2\mu\bar{X} + \mu^2\text{; as }\frac{\sum_{i=1}^{n}X_i}{n} = \bar{X}\\
&= \frac{\sum_{i=1}^{n}{X_i}^2}{n} - 2\mu^2 + \mu^2 = \frac{\sum_{i=1}^{n}{X_i}^2}{n} - \mu^2 \text{; as }n\rightarrow\infty\text{ }\bar{X}\rightarrow\mu\\
&= E[{X_i}^2] - E[X_i]^2 = Var(X_i) = \sigma^2
\end{align}

2. What is p-value? (Choose one or more)

* [x] Assuming that the null hypothesis is true, what is the probability of observing the current data.

* [ ] Based on the observed data, what is the probability of the null hypothesis being true.

* [ ] Based on the observed data, what is the probability of the null hypothesis being false.

* [ ] Assuming that our hypothesis is true, what is the chance that we reject the null hypothesis.

3. If we conduct a frequentist statistical test at 5% significance level repeatedly for 4,000 times, how many times can we expect to have statistically significant results even if group A and B are exactly the same? - 200 times as false positive rate is expected to be 5%

4. Hamster Inc. once again wants to test the conversion rates between package colors of its sunflower seeds; this time it is Red Package vs Gold Package. The Red Package is the existing group with average conversion rate of 11%. If they think the minimum detectable effect is 1% and want to make a 80/20 control/test split, how many unique users should see each package color before we decide which one performs better? Assume that they are testing at significance level of 15%. Show your work.

\begin{align}
Z_{\alpha} &= \frac{\text{MDE}-\mu}{\sqrt{\sigma^2 * (\frac{1}{n} + \frac{1}{mn})}} \\
\frac{(m+1)\sigma^2}{mn} &= (\frac{\text{MDE}}{Z_{\alpha}})^2 \\
n &= \frac{m+1}{m}(\frac{Z_{\alpha} \sigma}{\text{MDE}})^2 \\
n &= \frac{5}{4}(\frac{Z_{\alpha} \sigma}{\text{MDE}})^2; m=4 \text{ due to 80/20 split} \\
n &= \frac{5}{4}(\frac{1.03643 \sigma}{\text{MDE}})^2; Z_{0.15, one-tailed}=1.03643 \text{ at 15% significance, find out which one is better} \\
n &= \frac{5}{4}(\frac{1.03643}{\text{MDE}})^2 * 0.0979; \sigma^2 = p*(1-p) = 0.11*(1-0.11) = 0.0979 \text{ assuming sample variance of control is equal to pooled variance} \\
n &= \frac{5}{4}(\frac{1.03643}{0.01})^2 * 0.0979; MDE = 0.01 \\
n &= 4469.424163142676
\end{align}

We will need a test group of 4,470 unique visitors and 17,880 unique visitors for the control group.

5. Let us say Hamster Inc. ran the experiment and got the following results. 

| campaign_id | clicks | conv_cnt | conv_per |
|------------:|-------:|---------:|---------:|
|         Red |  59504 |     5901 | 0.099170 |
|        Gold |  58944 |     6012 | 0.101995 |

5.1 At significance level of 7%, which variation should be chosen to run at 100% traffic? Show your work.

Null hypothesis is that the conversion rate of Red package is higher than the conversion rate of Gold package. We run a one-tailed Z-test at 7% significance level and reject the null hypothesis. We should run the Gold package at 100% traffic.

\begin{align}
p_\text{pooled} &= \frac{5901+6012}{59504+58944} \\
&= 0.10057578008915305 \\
\sigma^2_\text{pooled} &= p_\text{pooled} * (1-p_\text{pooled}) \\
&= 0.10057578008915305 * (1-0.10057578008915305) \\ 
&= 0.09046029254861138 \\
\bar{X_\Delta} &= 0.101995 - 0.099170 = 0.002825\\
Z_\Delta &= \frac{\bar{X_\Delta}-\mu}{\sqrt{\frac{\sigma^2_\text{A}}{n_\text{A}} + \frac{\sigma^2_\text{B}}{n_\text{B}}}} \\
&= \frac{0.002825-0}{\sqrt{0.09046029254861138 * (\frac{1}{59504} + \frac{1}{58944})}} \\
&= 1.6162869810704354 \\
p_\Delta &= 0.053026 < 0.07
\end{align}

5.2 What are the confidence intervals at 7% significance of conversion rates for Red and Gold? Show your work.

\begin{align}
CI &= \bar{x} \pm Z_{0.07,one-tailed} * \sqrt{\frac{\sigma^2}{n}} \\
CI &= \bar{x} \pm 1.475791 * \sqrt{\frac{\sigma^2}{n}} \\
CI_{red} &= 0.099170 \pm 1.475791 * \sqrt{\frac{(0.099170)*(1-0.099170)}{59504}} \\
&=(0.09736172968006342, 0.10097827031993657) \\
CI_{gold} &= 0.101995 \pm 1.475791 * \sqrt{\frac{(0.101995)*(1-0.101995)}{58944}} \\
&=(0.10015535563734503, 0.10383464436265498)
\end{align}

6. Which of the following are true about frequentist A/B tests? (True/False)

* [T] It does not tell us the magnitude of the difference between control and test groups. - we can only incorporate the concept of minimum detectable effect to say what is the minimum magnitude of the difference we want

* [F] We can never know when to stop the experiments. - we know the required samples via minimum detectable effect

* [T] We can never determine if the null hypothesis being true. - we always assume the null hypothesis is true when calculating p-value

* [F] We can run one or as many experiments as we want using the same significance level. - this will lead to https://xkcd.com/882/

* [T] If we have too many samples in each group, the validity of the test can be jeopardized. - thus we need to give minimum detectable effect

* [T] If you have set up the experiment based on desired minimum detectable effect and significance level, statististical significance is the only factor in determining which group is the better one. - since we already incorporate the power we needed via those assumptions

* [F] We can only test difference between two proportions. - there are other tests such as t-tests for continuous variables 

* [F] More samples in control and test groups are always better. - as it leads to statistical significance when there is none