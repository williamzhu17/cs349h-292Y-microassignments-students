# Assignment: Delay-Based Computing

In this assignment, we will implement numerous delay-based computing gates in `delay_gates.py`. To implement each gate, you need to fill in the `reset` and the `execute` functions:

 - The `reset` function should reset the state of the gate before execution. Recall delay-based computing gates are stateful and "remember" pulse information, and pulses are stored during a loading stage then released during execution. The reset function should define and reset whatever flags are necessary to correctly implement the operation of the gate.
 - The `execute` function should determine if the gate produces a pulse at a given timestep. The execute function takes as input the current time step (in nanoseconds), and a dictionary of input-value pairs. In this implementation, each port may have two values: PULSE (1) or NO_PULSE (0).

A `delay_circuit.py` Python file is provided to simulate a delay-based computing circuit and render the results, and a `delay_tester.py` Python file is provided to construct some simple single-gate circuits and simulate them for you. Each test function in the `delay_tester.py` produces a visualization of each simulation and a visualization of the circuit architecture. The measured time window is shaded.

## Part X: Understanding Delay-Based Encodings [8 points]

Execute the `delay_tester.py` file as is to investigate the behavior of delay-based input over time. The `test_input` function simulates the propagation of three constant delay-based values with labels ('X', 'Y', 'Z') through an empty circuit and outputs a pulse trace (`test_input.png`) and a summary of all the pulse arrivals/departures to console.

1. What does each numbered segment in the input image represent? What does it mean when a pulse (vertical line) is contained within a numbered segment?

Each numbered segment in the input image represents a particular encoding of the value. When the pulse is contained within that numbered segment, that means that the pulse represents that particular encoding. For example, for IN.X.out, it's pulse is in segment 4. This means that X has a value of 4. 

2. What kind of value does an earlier pulse encode, what kind of value does a later pulse encode?

In this configuration, an earlier pulse encodes a smaller value while a later pulse encodes a larger value. 

3. Run the simulation multiple times. Do you observe any variations in the plots from execution to execution?

Yes, I observe variations in the plts from execution to execution. 

4. Look at the pulse summary printed to console. How is a gate's numerical values computed from the relative delay and segment time? How is the relative delay computed from the absolute delay and the gate's settling time? The settling time for a given port is the time required for the pulse to reach a particular port.

The numerical value is computed by floor(relative delay / segment time). The relative delay is computed by absolute delay - settling time. 

# Part Y: Implementing the Delay Gates [8 pts]

Next, we will implement the simulations of first arrival, last arrival, delay, and inhibition gates associated with delay-based computing. Each delay gate is reset before execution, and then "executed" at each time step. The reset and execute functions may instantiate and change the gate's internal state, feel free to instantiate any internal variables needed.

1. Implement the reset and execute functions for the first arrival (`FirstArrival`) gate. Describe any internal state maintained by the gate, and what the reset operation and execution functions do for this gate. Uncomment the `test_first_arrival_gate` function in `delay_tester.py` to test the operation of the first arrival gate.

As part of my FirstArrival gate, I maintained a seen state. This is a flag that turns on whenever we see the first pulse and remains high until reset. Reset lowers this flag back down. In the execute function, when we see a pulse on the input, we first check to see if we have already seen a pulse already. If we have not, it is our first pulse we seen and we emit a pulse out and raise our seen flag. However, if we already saw a pulse, we will not emit it out. 

2. Implement the reset and execute functions for the last arrival (`LastArrival`) gate. Describe any internal state maintained by the gate, and what the reset operation and execution functions do for this gate. Uncomment the `test_last_arrival_gate` function in `delay_tester.py` to test the operation of the last arrival gate.

Similar to the prior gate, the only internal state I maintained was a seen flag. This flag will raise when we see the first pulse. Reset lowers this flag back down. In the execute function, when we see a pulse on the input, we first check if we have already seen a pulse. If we have not, we will raise our seen flag and not emit a pulse out. However, if we have already seen a pulse, we will then emit a pulse out. However, there is an edge case when we have a pulse at the same time. When this happens, we just output a pulse. 

3. Implement the reset and execute functions for the delay (`Delay`) gate. Describe any internal state maintained by the gate, and what the reset operation and execution functions do for this gate. Uncomment the `test_delay_gate` function in `delay_tester.py` to test the operation of the delay gate. What does the circuit described in the `test_delay_gate` function do to the input value? 

For the delay gate, the internal states I kept tracked of was a seen flag, a seen_time count, and a pulsed flag. The seen flag is to indicate when we see the pulse. The seen_time count indicates the time when we saw the pulse. The pulsed flag is to remember if we have emitted a pulse out yet. Reset lowers all flags and resets seen_time to be 0. In the execute function, if we get an input pulse, we first check to see if we have already gotten a pulse. If not, we will mark the seen flag and update the time we saw this pulse. Then, after delay_ns, we will then output a pulse and mark that we have completed the delay so that the next time we check, we do not output another pulse. 

4. Implement the reset and execute functions for the inhibition (`Inhibition`) gate. If two pulses arrive at the same time (which is unlikely in practice), you can assume that the gate emits a pulse with 50% probability. Describe any internal state maintained by the gate, and what the reset operation and execution functions do for this gate. Uncomment the `test_inh_gate` function in `delay_tester.py` to test the operation of the inhibition gate.

For the inhibition gate, I maintained three states: seen_a, seen_b, and suppress. seen_a is a sticky flag to flag when a pulse at input A was seen. seen_b is also a sticky flag to flag when a pulse at input B was seen. suppress is a flag that is raised when we see that we saw a pulse, but no b pulse so we need to suppress b. Reset lowers all of these flags. In the execute function, when we see an input pulse, we first update our corresponding seen_X flags. Then, if there is a case where we already saw a pulse in input A but not a pulse in input B, we will raise our suppress flag, indicating that we need to suppress B. Then, if we see an input B pulse, if we are suppressing, we do not pass it through, but if we are not suppressing, we pass the pulse through. There is one edge case where two pulses arrive at the same time. In this case, we just do a coin flip of pulsing or not. 

# Part Z: Using Delay-Based Computing [6 pts + 6 extra credit]

Implement a circuit that computes the numerical function.

    if max(X,Y) < 5:
        return max(X,Y)
    else:
        <no pulse>

You can use the `add_wire(src_gate,dst_gate,port)` function to add wires between gates, and the `add_gate(gate)` function to add a gate to the circuit. Feel free to use the `render_circuit("filename")` function to visualize the circuit that you built. As a reminder, in the simulation, the wire does not incur any delay but the gate introduces delay, and you need to make sure the inputs to the same gate have aligned delays. Reference the functions in `delay_tester.py` for examples of how to build and render a circuit. You do not need to worry about the `max(X,Y)=5` case. Test your circuit on a few values to verify that it computes the function correctly.

1. What is the structure of the circuit you implemented? Include a diagram of the circuit in your writeup. [4 pts]

See test_max_circ.png for the diagram of the circuit. We first find the max of X and Y by using an LA gate. The last arrived will be the larger value and we will pass this through. Then, we will use an inhibition gate with a constant 5. Thus, when max(X, Y) < 5, we will pass on max(X, Y), otherwise no pulse. Another thing to note is that we had to add a delay gate between the constant five and inhibition gate. Otherwise, it would not line up with the timing of the LA gate. 

2. What if the `<` operation is replaced with `>`? What is the structure of the circuit you implemented? Include a diagram of the circuit in your writeup. [4 extra credit]

See test_max_flip_circ.png for the diagram of the circuit. Similar to the prior circuit, we find the max(X, Y) using an LA circuit. Then, we also delay the constant 5 with a delay gate and then feed that into the inhibition gate as the A input. The output of the max(X, Y) will now be the B input. This inhibition gate will pass through a 5 if max(X, Y) > 5. Then, we use this as a turn on signal for the output. We take a delayed version of the max output with the inhibition output and drive it into another LA gate. As a result, if we see a pulse from the inhibition gate, we know that the output will be max(X, Y) since the pulse tells us when max(X, Y) > 5. However, if we do not see a pulse, this means we did not get an inhibition output and the LA gate blocked the passing of max(X, Y). 

Researchers have recently explored using delay-based computing in the log domain. With this method, instead of computing directly over numeric values, a value `x` is encoded into `x'=-ln(x)` as a delay (you need not worry about encoding of negative values in this question), delay-based computing is used to implement the computation, and then you raise the delay-based value `x=e^{-x'}` to recover the original value. This method can encode a broader value range using the same delay range, and obtain results faster compared to naive encoding, especially when dealing with large values.

2. The log domain encoding also enables operations that are difficult to implement in the original value domain. Describe how you can implement multiplication and constant value scaling in log domain. [2 pts]

One can use log tricks to accomplish multiplication and constant value scaling in log domain. For example, let's say you wanted to multiply X and Y. To do this in the log domain, you first convert X and Y into log domain: X'=-ln(X) and Y'=-ln(Y). Then, you can add them to get -ln(XY). Then, if we raise this value, we can uncover the muliptiplied result and only had to do a delay based add. 

For constant value scaling, it is of similar manner. Let's say you want to achieve cX. First, let's convert to log domain c'=-ln(c) and X'=-ln(X). Then, if we add them, we get -ln(c)-ln(X) which is just -ln(cX). If we unlog it, we can then just recover cX. This allows us to do scaling by only addition. 

3. One downside of computing in log domain though is that addition and substraction become more difficult. However, there are effective appraoches to approximate them. For example, substraction of two values `z=x-y` is `z'=-ln(e^{-x'}-e^{-y'})` in the log domain, but it can be approximated using delay logic as `z'=min(inhibit(x'+E0,y'+F0), ...,inhibit(x'+En,y'+Fn))`, where `Ei`'s and `Fi`'s are specially picked constants. Refer to `nLDE_approximation.png` in the folder for a visualization where `x'+y'=0`. Could you devise a similar approximation approach for addition? You may also focus on the case where `x'+y'=0`. Write the expression you use for the approximation, using only `min`, `max`, `inhibit` operations. Include a figure to show how good the approximation is in your writeup. [2 extra credit]

# Part W: Digital Logic with Delay-Based Computing [14 pts]

Move to the `delay_digital.py` file. The file uses race-based computing to execute `(X | not Y) and (Z | X) and (Z | Y)`. I have already implemented the scaffold for this part of the project which builds the logic circuit, and convenience functions for performing the dual-rail encoding. The delay-signal visualization in this part may be too dense to read due to many number of gates, but you may read the text output for debugging.

1. Implement the `and` gate using delay logic. How did you implement this gate?

I implemented the and gate by using a combination of both the LastArrival and FirstArrival gate. For the Rp case, we know that we need to have both Ap and Bp to have pulses. As a result, I wire the Ap and Bp into an LastArrival since it requires both pulses to pass a pulse through. For the Rn case, we know that as long as one An or Bn is pulsed, we need to pulse Rn. As a result, we use a FirstArrival gate since whenever we first see a pulse in An or Bn, then we will pass a pulse through. 

2. Implement the `or` gate using delay logic. How did you implement this gate?

The or gate will be the opposite of the and gate. For the Rp case, we know that we need to have either Ap or Bp to have pulses. As a result, I wire the Ap and Bp into a FirstArrival gate, which passes a pulse through on the first seen pulse. For the Rn case, we need to know that both An and Bn both have pulses. As a result, I use a LastArrival gate to ensure both pulses exist before sending a pulse through. 

3. Implement the `not` gate using delay logic. How did you implement this gate?

To implement the not gate, we just simply use delay gates and wire the Ap to output to Rn through a delay and wire the An to output to Rp. This just flips the bit. 

4. Implement the digital readout gate in `delay_gates.py` (see class `DigitalReadOutGate`). This gate should remember if it saw a pulse or not.

5. Execute the completed implementation on a few digital values. What delay-based encoding does a digital "1" output correspond to? What delay-based encoding does the digital "0" output correspond to? What states are invalid in the current digital value encoding?
 
The encoding for a digital "1" is when the positive line pulses (Xp). The encoding for a digital "0" is when the negative line pulses (Xn). The state that is invalid is if both positive and negative lines pulse or if none of them pulse. 

6. Currently, the implementation creates a fresh input signal for every usage of every variable instead of re-using the input signal. Why is this necessary? What would happen if you build the same circuit, but then reuse the same input for multiple gates?

In this implementation, it creates a fresh input signal for every usage of every variable since the DelayBasedCircuit class is not able to handle wire splitting. As a result, whenever we get an output of a gate, we can only wire it to one destination. If we try to wire it to multiple destinations, the current class will overwrite the prior wiring. 

7. What would happen if you don't reset the circuit between executions? Why is a circuit reset operation necessary for delay-based digital logic, but not necessary for conventional digital logic?

If you do not reset the circuit between executions, we will either forget things or have flags that have been raised to high that are not lowered. For example, let's look at FirstArrived. We run an operation and now our seen flag in our FirstArrived gate is now high. If we try to run another operation without resetting, we will never be able to send a pulse through since the FirstArrived gate thinks it already saw a pulse. 

This is necessary for delay-based digital logic because each foundational gate holds state. However, for conventional digital logic, there is no state being held for foundational gates, as they all evaluate combinationally. 
