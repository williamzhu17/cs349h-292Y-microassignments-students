#### Part A: Stochastic Computing [2 pt/question, 8 points]

The provided scaffold code runs 10,000 trials of the `1/2*(0.8*0.4 + 0.6)` stochastic computation and plots the distribution of results. The `PART_A_example_computation` function executes the above numeric expression, and the `run_stochastic_computation` runs a stochastic computation for <ntrials> trials and plots the distribution + reports the mean and standard deviation of the stochastic executions. The vertical red line shows the expected result. Currently, the stochastic computing operations and value-to-bitstream / bitstream-to-value conversion routines are not implemented. 

Implement the stochastic computing paradigm by filling in the function stubs in the PosStochComputing class. Don't worry about supporting negative numbers just yet.

- `to_stoch` : convert a value in [0,1] to a stochastic bitstream.
- `from_stoch`: convert a stochastic bitstream to a numerical value
- `stoch_add`: perform scaled addition over two stochastic bitstreams.
- `stoch_mul`: perform multiplication over two stochastic bitstreams.

Execute the stochastic computation for bitstream lengths 10, 100, and 1000 with `stochastic.py`, and answer the following questions.

Q1. How does the mean change with increasing bitstream length? How does the variance change?

The mean stays relatively the same. However, in some trials, it becomes more accurate as the bitstream length increases. Variance, however, always consistently decreases as bitstream length increases. 

Q2. What is the smallest representable numeric value in a single 1000-bit stochastic bitstream? What happens when you try to generate a bitstream for this value -- do the bitstream values converge to the desired value?

The smallest representable numeric value is 0.001. If I try to generate a bitstream for this value, on average, it does converge to 0.001. I ran 10k trials converting 0.001 to stoch and then back to normal numbers. I get that the mean of all the results is 0.0009977 and the std is 0.00101.

Q3. What stochastic bitstream length L do we need to represent a rational number V accurately with a single bitstream, assuming V is in (0,1]? Write the equation. How does this L scale with V? Denote L' as the number bits needed to represent V accurately as an integer (removing the leading "0."). How does L' scale with V? 

We can accurately represent rational number V with a single bitstream of length L = 1/V. This is not the minimum, but ensures it is representable. This L scales linearly with the inverse of V. 

If we remove the leading 0., then L' = log_2(1/V). L' scales logarithmically. 

Q4. Design a stochastic computation for bitstreams with a length n=1000, such that the end result is not accurately representable by a single bitstream. You must accomplish this with stochastic operations, all initial values must be >= 0.1 and every constant must be a uniquely generated bitstream.

We can do (0.1)^4. We can generate four 0.1s. Then, by multiplying 0.1 four times, we should get 0.0001. With bitstreams of length n=1000, the end result should not be able to be represented. 

#### Part X: Non-Idealities Stochastic Computing [2 pt/question, 6 points]

Next, we'll experiment with introducing non-idealities into the stochastic computation `1/2*(0.8*0.4 + 0.6)`. We will introduce two kinds of non-idealities:

- bit-shift errors: this class of errors result from timing issues in circuits. This non-ideality causes one bitstream to lag behind the other during computation. For example, a bit shift error at index 1 of a bit stream would transform some stream 00101 to 00010 (the 0 at index 1 is replicated). We do not consider the case where more than one bit shift occurs at the same index, as it is unlikely to happen in practice.

- bit-flip errors: this class of errors result from bit flips in storage elements, or in the computational circuit. This non-ideality introduces bit flips in bitstreams. For example, a bit flip error at index 1 of a bit stream would transform some stream 00101 to 01101.

Fill in the `apply_bitshift` and `apply_bitflip` functions in the stochastic computing class and apply these non-idealities at the appropriate points in the stochastic computing model. Make sure these non-idealities are only enabled for this section of the homework.

Q1. What happens to the computational results when you introduce a per-bit bit-flip error probability of 0.0001? What happens when the per-bit bit flip error probability is 0.1?

If we introduce bit-flip error probability of 0.0001, the mean and std do not change significantly. Likewise, if we introduce probability of 0.1, the mean and std still stay relatively the same. 

Q2. What happens to the computational results when you introduce a per-bit bit-shift error probability of 0.0001? What happens when the per-bit bit shift error probability is 0.1?

If we introduce per-bit bit-shift error probability of 0.0001, the mean and std do not change significantly. Likewise, if we introduce probability of 0.1, the mean and std still stay relatively the same. 

Q3. In summary, is the computation affected by these non-idealities? Do you see any changes in behavior as the bitstream length grows?

The computation seems to not be affected by these non-idealities. As the bitstream length grows, the mean remains relatively the same, but std goes down. 

#### Part Y: Statically Analyzing Stochastic Computations [2 pt/question, 6 points]

Next, we'll build a simple static analysis for stochastic computations. A _static analysis_ is a type of analysis that is able to infer information about a program without ever running the computation. The analysis we will be building determines the minimum bitstream size necessary for a computation, given a set of precisions for each of the arguments. We define a bitstream size V to be sufficient if for any possible values t generated during the computation, V*t>=1. For example, to compute the bitstream length for the following expression:

    (x + y) + z

We will set up the static analyzer as follows:

    `analysis = StochasticComputingStaticAnalysis()`
    `analysis.stoch_add(analysis.stoch_add(prec_x, prec_y), prec_z)`
    `N = analysis.get_size()`

where `prec_x`, `prec_y`, and `prec_z` are the precisions of x, y, and z respectively. Precision of a variable is defined as the smallest value of the variable. If the precision of x is 0.01, the precision of y is 0.02 and the precision of z is 0.03, then the minimum bitstream length is 100. In this exercise, you will be populating the `StochasticComputingStaticAnalysis` class, which offers the following functions:

    - `stoch_var`, given a variable with a desired precision `prec`, update the static analyzer to incorporate this information.
    - `stoch_add`, given two stochastic bitstreams that can represent values with precision `prec1` and `prec2` respectively, figure out the precision required for the result stochastic bitstream given an addition operation is performed. Update the static analyzer to incorporate any new information.
    - `stoch_mul`, given two stochastic bitstreams that can represent values with precision `prec1` and `prec2` respectively, figure out the precision required for the result stochastic bitstream given a multiplication operation is performed. Update the static analyzer to incorporate any new information.
    - `get_size`, given all of the operations and variables analyzed so far, return the smallest possible bitstream size that accurately executes all operations, and can accurately represent all values.

We will use this static analysis to figure out what stochastic bistream length to use for the computation 1/2*(w*x + b), where the precision of w is 0.01, the precision of x is 0.1, and the precision of b is 0.1. For convenience, the scaffold file provides helper functions `PART_Y_analyze_wxb_function` for analyzing the `1/2*(w*x+b)` function, given a dictionary of precisions for variables `w`, `x`, and `b`, a `PART_Y_execute_wxb_function` which executes the `1/2*(w*x+b)` function using stochastic computing given a dictionary of variable values for `w`, `x`, and `b`, and a `PART_Y_test_analysis` function which uses the static analysis to find the best bitstream size for the `1/2*(w*x+b)` expresison, and then uses the size returned by the static analyzer to execute the `1/2*(w*x+b)` for ten random variable values that have the promised precisions.

Q1. Describe how your precision analysis works. Specifically, how do you propagate the precisions through the entire computation? How do you determine the final size?

Q2. What bitstream length did your analysis return?

Q3. How did the random executions perform when parametrized with the analyzer-selected bitstream length?
 
#### Part Z: Sources of Error in Stochastic Computing [2 pt/question, 4 points]

Next, we will investigate the `PART_Z_execute_rng_efficient_computation` stochastic computaton. This computation implements `1/2*(x*x+x)`, and implements an optimization (`save_rngs=True`) that reuses the bitstream for x to reduce the number of random number generators.

Q1. Does the accuracy of the computation change when the `save_rngs` optimization is enabled? Why or why not?

Q2. Devise an alternate method for implementing $x*x+x$ from a single stochastic bitstream. There is a way to do this with a single (N+k)-bit bitstream, where k is a small constant value.

 
#### Part W: Extend the Stochastic Computing Paradigm [15 points]

Come up with your own extension, application, or analysis tool for the stochastic computing paradigm. This is your chance to be creative. Describe what task you chose, how it was implemented, and describe any interesting results that were observed. There is no need to pursue great results, e.g., beating some state-of-the-art approaches. It is fine to obtain minimum results just to show that your idea works. Here are some ideas to get you started:

- Implement a variant of stochastic computing, such as deterministic stochastic computing or bipolar stochastic computing. You may also modify the existing stochastic computing paradigm to incorporate a new source of hardware error -- you will need to justify your hardware error model. 

- Build an stochastic computing analysis of your choosing. You may build up the existing bitstream size analysis to work with abstract syntax trees, or you may devise a new analysis that studies some other property of the computation, such as error propagation or correlation.

- Implement an application using the stochastic computing paradigm. Examples from literature include image processing, ML inference, and LDPC decoding.