# Homework #2 - A/B Testing in the Wild

1. The Law of Large Numbers (LLN) says that sample mean will converge to expectation as sample size grows. Assuming that this is true, prove that sample variance will converge to variance as sample size grows. 

2. What is p-value? (Choose one or more)

* [ ] Assuming that the null hypothesis is true, what is the probability of observing the current data.

* [ ] Given the observed data, what is the probability of the null hypothesis being true.

* [ ] Given the observed data, what is the probability of the null hypothesis being false.

* [ ] Assuming that our hypothesis is true, what is the chance that we reject the null hypothesis.

3. If we conduct a frequentist statistical test at 5% significance level repeatedly for 4,000 times, how many times can we expect to have statistically significant results even if variant A and B are exactly the same?

4. Hamster Inc. once again wants to test the conversion rates between package colors of its sunflower seeds; this time it is Red Package vs Gold Package. The Red Package is the existing variant with average conversion rate of 11%. If they think the minimum detectable effect is 1% and want to make a 80/20 control/test split, how many unique users should see each package color before we decide which one performs better? Assume that they are testing at significance level of 15%. Show your work.

5. Let us say Hamster Inc. ran the experiment and got the following results. 

| campaign_id | clicks | conv_cnt | conv_per |
|------------:|-------:|---------:|---------:|
|         Red |  59504 |     5901 | 0.099170 |
|        Gold |  58944 |     6012 | 0.101995 |

5.1 At significance level of 7%, which variation should be chosen to run at 100% traffic? Show your work.

5.2 What are the confidence intervals of conversion rates for Red and Gold? Show your work.


6. Which of the following are true about frequentist A/B tests? (True/False)

* [ ] It does not tell us the magnitude of the difference between control and test groups.

* [ ] We can never know when to stop the experiments.

* [ ] We can never determine if the null hypothesis being true.

* [ ] We can run one or as many experiments as we want using the same significance level.

* [ ] If we have too many samples in each group, the validity of the test can be jeopardized.

* [ ] We should always use the variant that has better performance at statistically significant level.

* [ ] We can only test difference between two proportions.

* [ ] More samples in control and test groups are always better.
