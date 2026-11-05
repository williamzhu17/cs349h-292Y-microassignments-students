from delay_gates import *
from delay_circuit import *


def summarize_outputs(outputs):
    print("------")
    for (gate,port), value, settle, segment, abs_t, rel in outputs:
        print("%s port:%s = %s" % (gate,port,value))
        print("   settling time =\t%e" % (settle))
        print("   relative delay =\t%e" % (rel))
        print("   absolute delay =\t%e" % (abs_t))
        print("   segment time =\t%e" % (segment) )
        print("")


def test_input():
    circ = DelayBasedCircuit()
    inx = circ.add_gate(Input("X"))
    inx = circ.add_gate(Input("Y"))
    inx = circ.add_gate(Input("Z"))
    timing, traces = circ.simulate({"X":4, "Y":7, "Z":2})
    circ.render("test_input.png",timing,traces)
    circ.render_circuit("test_input_circ")
    summarize_outputs(circ.get_outputs(timing,traces))


def test_last_arrival_gate():
    circ = DelayBasedCircuit()
    inx = circ.add_gate(Input("X"))
    iny = circ.add_gate(Input("Y"))
    la = circ.add_gate(LastArrival())
    circ.add_wire(inx,la,"A")
    circ.add_wire(iny,la,"B")

    timing,traces = circ.simulate({"X":4,"Y":7})
    circ.render("test_la.png",timing,traces)
    circ.render_circuit("test_la_circ")
    summarize_outputs(circ.get_outputs(timing,traces))


def test_first_arrival_gate():
    circ = DelayBasedCircuit()
    inx = circ.add_gate(Input("X"))
    iny = circ.add_gate(Input("Y"))
    fa = circ.add_gate(FirstArrival())
    circ.add_wire(inx,fa,"A")
    circ.add_wire(iny,fa,"B")

    timing,traces = circ.simulate({"X":4,"Y":7})
    circ.render("test_fa.png",timing,traces)
    circ.render_circuit("test_fa_circ")
    summarize_outputs(circ.get_outputs(timing,traces))


def test_delay_gate():
    circ = DelayBasedCircuit()
    inx = circ.add_gate(Input("X"))
    delay = circ.add_gate(DelayGate(2*circ.segment_time))
    circ.add_wire(inx,delay,"A")

    circ.render_circuit("test_del_circ")
    timing,traces = circ.simulate({"X":4})
    circ.render("test_del1.png",timing,traces)
    summarize_outputs(circ.get_outputs(timing,traces))

    timing,traces = circ.simulate({"X":6})
    circ.render("test_del2.png",timing,traces)
    summarize_outputs(circ.get_outputs(timing,traces))


def test_inh_gate():
    circ = DelayBasedCircuit()
    inx = circ.add_gate(Input("X"))
    iny = circ.add_gate(Input("Y"))
    inh = circ.add_gate(Inhibition())
    circ.add_wire(inx,inh,"A")
    circ.add_wire(iny,inh,"B")

    circ.render_circuit("test_inh_circ")
    timing,traces = circ.simulate({"X":4,"Y":7})
    circ.render("test_inh1.png",timing,traces)
    summarize_outputs(circ.get_outputs(timing,traces))

    timing,traces = circ.simulate({"X":7,"Y":4})
    circ.render("test_inh2.png",timing,traces)
    summarize_outputs(circ.get_outputs(timing,traces))

def test_max():
    circ = DelayBasedCircuit()
    inx = circ.add_gate(Input("X"))
    iny = circ.add_gate(Input("Y"))
    max = circ.add_gate(LastArrival())
    circ.add_wire(inx, max, "A")
    circ.add_wire(iny, max, "B")

    five = circ.add_gate(Input("FIVE"))
    delay = circ.add_gate(DelayGate(0))
    circ.add_wire(five, delay, "A")

    inh = circ.add_gate(Inhibition())
    circ.add_wire(delay, inh, "A")
    circ.add_wire(max, inh, "B")

    circ.render_circuit("test_max_circ")
    timing, traces = circ.simulate({"X": 4, "Y": 7, "FIVE": 5})
    circ.render("test_max1.png", timing, traces)
    summarize_outputs(circ.get_outputs(timing, traces))

    timing, traces = circ.simulate({"X": 4, "Y": 3, "FIVE": 5})
    circ.render("test_max2.png", timing, traces)
    summarize_outputs(circ.get_outputs(timing, traces))

    timing, traces = circ.simulate({"X": 6, "Y": 7, "FIVE": 5})
    circ.render("test_max3.png", timing, traces)
    summarize_outputs(circ.get_outputs(timing, traces))

def test_max_flip():
    circ = DelayBasedCircuit()
    inx = circ.add_gate(Input("X"))
    iny = circ.add_gate(Input("Y"))
    max = circ.add_gate(LastArrival())
    circ.add_wire(inx, max, "A")
    circ.add_wire(iny, max, "B")

    five = circ.add_gate(Input("FIVE"))
    five_delay = circ.add_gate(DelayGate(0))
    circ.add_wire(five, five_delay, "A")

    inh = circ.add_gate(Inhibition())
    circ.add_wire(max, inh, "A")
    circ.add_wire(five_delay, inh, "B")

    max_delay = circ.add_gate(DelayGate(0))
    circ.add_wire(max, max_delay, "A")

    pass_through = circ.add_gate(LastArrival())
    circ.add_wire(max_delay, pass_through, "A")
    circ.add_wire(inh, pass_through, "B")

    circ.render_circuit("test_max_flip_circ")
    timing, traces = circ.simulate({"X": 4, "Y": 7, "FIVE": 5})
    circ.render("test_max_flip1.png", timing, traces)
    summarize_outputs(circ.get_outputs(timing, traces))

    timing, traces = circ.simulate({"X": 4, "Y": 3, "FIVE": 5})
    circ.render("test_max_flip2.png", timing, traces)
    summarize_outputs(circ.get_outputs(timing, traces))

    timing, traces = circ.simulate({"X": 6, "Y": 7, "FIVE": 5})
    circ.render("test_max_flip3.png", timing, traces)
    summarize_outputs(circ.get_outputs(timing, traces))

# test_input()
# test_first_arrival_gate()
# test_last_arrival_gate()
# test_inh_gate()
# test_delay_gate()
# test_max()
test_max_flip()
