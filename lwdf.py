# %%

from b_asic.sfg_generators import wdf_allpass
from b_asic.special_operations import Input, Output
from b_asic.sfg import SFG
from b_asic.core_operations import SymmetricTwoportAdaptor
from b_asic.schedule import Schedule
from b_asic.quantization import QuantizationMode

import apytypes as apy

wl0 = 1
wl1 = 6

a10 = float(apy.fx(0.4573, wl0, wl1))
a11 = float(apy.fx(-0.2098, wl0, wl1))
a12 = float(apy.fx(0.5695, wl0, wl1))
a13 = float(apy.fx(-0.2123, wl0, wl1))
a14 = float(apy.fx(0.0952, wl0, wl1))
a15 = float(apy.fx(-0.2258, wl0, wl1))
a16 = float(apy.fx(-0.4490, wl0, wl1))

a1 = float(apy.fx(-0.068129, wl0, wl1))
a3 = float(apy.fx(-0.242429, wl0, wl1))
a5 = float(apy.fx(-0.461024, wl0, wl1))
a7 = float(apy.fx(-0.678715, wl0, wl1))
a9 = float(apy.fx(-0.888980, wl0, wl1))

allpass1 = wdf_allpass([a10, 0, a11, a12, a13, a14, a15, a16], name="Allpass 1")
allpass1 = allpass1.remove_operation("t0") # This removes the name for some reason
allpass1.name = "Allpass 1"

allpass2 = wdf_allpass([a1, 0, a5, 0, a9, 0])
allpass2 = allpass2.remove_operation("t0")
allpass2 = allpass2.remove_operation("t2")
allpass2 = allpass2.remove_operation("t4")

allpass3 = wdf_allpass([a3, 0, a7, 0])
allpass3 = allpass3.remove_operation("t0")
allpass3 = allpass3.remove_operation("t2")

#
# Create lowpass 1 and 2
in0 = Input()
allpass2 <<= in0
allpass3 <<= in0

out0 = Output(allpass2)
out1 = Output(allpass3)

lowpass1 = SFG([in0], [out0, out1])


allpass2.connect_external_signals_to_components()
allpass3.connect_external_signals_to_components()
lowpass1 = SFG([in0], [out0, out1], name="Lowpass 1")

lowpass2 = lowpass1.unfold(2)
lowpass2.name = "Lowpass 2"

#
# Connect lowpass 1 and 2
in0 = Input()
lowpass1.input(0).connect(in0)

lowpass2.input(0).connect(lowpass1.output(0))
lowpass2.input(1).connect(lowpass1.output(1))

out0 = Output(lowpass2.output(0))
out1 = Output(lowpass2.output(1))
out2 = Output(lowpass2.output(2))
out3 = Output(lowpass2.output(3))

lowpass1.connect_external_signals_to_components()
lowpass2.connect_external_signals_to_components()

sfg = SFG([in0], [out0, out1, out2, out3], name="Lowpass 1 and 2")



# Connect allpass 1 with lowpass 1 and 2
 
in0 = Input()
allpass1 <<= in0

sfg.input(0).connect(allpass1.output(0))

out0 = Output(sfg.output(0))
out1 = Output(sfg.output(1))
out2 = Output(sfg.output(2))
out3 = Output(sfg.output(3))

allpass1.connect_external_signals_to_components()
sfg.connect_external_signals_to_components()

lwdf = SFG([in0], [out0, out1, out2, out3], name="LWDF")
lwdf

# %%
from b_asic import Simulation, interleave, VhdlDataType
from b_asic.signal_generator import Sinusoid

dt = VhdlDataType(wl=(2, 6))#, quantization_mode=QuantizationMode.UNBIASED_ROUNDING)
sim = Simulation(lwdf, [0.25*Sinusoid(0.1)], dt)
sim.run_for(500)

import matplotlib.pyplot as plt  # noqa: E402

out = interleave(
    sim.results["out0"],
    sim.results["out1"],
    sim.results["out2"],
    sim.results["out3"],
)

plt.stem(sim.results["in0"][460:500])
plt.show()
plt.stem(out[450*4:490*4])

# plt.plot(results[0])
# plt.plot(results[1])
# plt.legend()
# plt.show()

# for i in range(4):


# %%
lwdf.set_latency_of_type(SymmetricTwoportAdaptor, 3)
lwdf.set_execution_time_of_type(SymmetricTwoportAdaptor, 1)

schedule = Schedule(lwdf, cyclic=True)

# schedule.move_operation('out2', 5)
# schedule.move_operation('out2', 29)
# schedule.move_operation('sym2p2_1', 15)
# schedule.move_operation('sym2p2_1', 12)
# schedule.move_operation('out3', 4)
# schedule.move_operation('out3', 7)
# schedule.move_operation('out2', 7)
# schedule.move_y_location('out2', 25, True)
# schedule.move_operation('sym2p4_1', 11)
# schedule.move_y_location('sym2p4_1', 24, True)
# schedule.move_operation('out0', 7)
# schedule.move_operation('sym2p2_0', 7)
# schedule.move_operation('sym2p1_1', 10)
# schedule.move_operation('sym2p1_1', 17)
# schedule.move_operation('sym2p3_1', 11)
# schedule.move_y_location('sym2p3_1', 19, True)
# schedule.move_operation('out1', 10)
# schedule.move_operation('sym2p4_0', 10)
# schedule.move_operation('sym2p0_1', 23)
# schedule.move_operation('sym2p0_1', 4)
# schedule.move_operation('sym2p1_0', 7)
# schedule.move_operation('sym2p1_0', -7)
# schedule.set_schedule_time(27)

# schedule = schedule.edit()


# %%
from b_asic.scheduler import RecursiveListScheduler

lwdf.set_latency_of_type(SymmetricTwoportAdaptor, 3)
lwdf.set_execution_time_of_type(SymmetricTwoportAdaptor, 1)

resources = {"sym2p": 3, "in": 1, "out": 1}
schedule = Schedule(
    lwdf,
    scheduler=RecursiveListScheduler(
        sort_order=((1, True), (3, False), (4, False)),
        max_resources=resources
    ),
    # schedule_time=6,
    cyclic=True,
)

schedule.move_operation('out3', -6)
schedule.move_operation('out2', -6)
schedule.move_operation('out0', -1)
schedule.move_operation('out3', 2)
schedule.move_y_location('out3', 23, True)
schedule.move_operation('out0', -2)
schedule.move_operation('out1', 1)
schedule.move_operation('out3', 1)
schedule.move_operation('out1', -1)
schedule.move_operation('out0', 2)
schedule.move_operation('out1', 2)
schedule.move_operation('out3', -2)
schedule.move_operation('out3', 1)

schedule.move_operation('sym2p1', 1)
schedule.move_operation('sym2p4_0', -1)
schedule.move_operation('sym2p0_0', -1)
schedule.move_operation('sym2p1_0', 1)
schedule.move_operation('sym2p8', -1)

# %% Resource Assignment
from b_asic.resource_assigner import assign_processing_elements_and_memories
from b_asic.architecture import Architecture

pes, mems, direct = assign_processing_elements_and_memories(
    schedule.get_operations(),
    schedule.get_memory_variables(),
    strategy="ilp_graph_color",
    memory_read_ports=1,
    memory_write_ports=1,
    memory_total_ports=2,
)

# %%
arch = Architecture(pes, mems, "lwdf", direct)
arch

# %%
from b_asic import Simulation, interleave, VhdlDataType
from b_asic.signal_generator import Sinusoid

dt = VhdlDataType(wl=(2, 6))#, quantization_mode=QuantizationMode.UNBIASED_ROUNDING)
sim2 = Simulation(schedule.sfg, [0.25*Sinusoid(0.1)], dt)
sim2.run_for(500)

# %%
from b_asic.code_printer import VhdlPrinter

printer = VhdlPrinter(dt)
printer.print(arch, path="src")


# %% Test bench generation
from b_asic.tb_printer import CocotbPrinter

tb_printer = CocotbPrinter(sim2.results)
tb_printer.print(arch, path="src", gui=True, csv=True)

# %%
import apytypes as apy

a = apy.APyFixed(106, 2, 15)
b = apy.APyFixed(0, 2, 15)
value = apy.APyFixed(-31, 2, 7)

u0 = b - a
mul_res = u0 * value

b0 = mul_res + a
b1 = mul_res + b

out0 = b1.cast(2, 15)
out1 = b0.cast(2, 15)

print("out0:", out0.to_bits(), "out1:", out1.to_bits())
