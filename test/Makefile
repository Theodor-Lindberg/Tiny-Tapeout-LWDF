# Makefile
# See https://docs.cocotb.org/en/stable/quickstart.html for more info

# List your source files here:
SOURCE_FILES =  in0.vhdl out0.vhdl memory0.vhdl memory1.vhdl memory2.vhdl memory3.vhdl memory4.vhdl sym2p0.vhdl sym2p1.vhdl lwdf.vhdl top.vhdl

# Toplevel name of your VHDL project
COCOTB_TOPLEVEL = tt_um_lwdf_top

# Common
WAVES = 1
SRC_DIR = $(PWD)/../src

ifeq ($(LIU), yes)
$(info ************ Running simulation on LiU computer ************)
ifeq ($(GATES),yes)
$(warning ************ Gate level simulation selected but currently not set up on LiU computers ************)
endif

TOPLEVEL_LANG = vhdl
SIM = ghdl
VHDL_SOURCES = $(addprefix $(SRC_DIR)/,$(SOURCE_FILES))
SIM_BUILD = sim_build
SIM_ARGS += --vcd=$(SIM_BUILD)/tb.vcd
EXTRA_ARGS += --workdir=$(SIM_BUILD) --work=work

else

# defaults
SIM ?= icarus
TOPLEVEL_LANG ?= verilog

# Change file extension from .vhdl to .v
PROJECT_TARGETS_V = $(SOURCE_FILES:.vhdl=.v)
# Prepend path for generated files
PROJECT_SOURCES = $(addprefix generated/, $(PROJECT_TARGETS_V))

ifneq ($(GATES),yes)

# RTL simulation:
SIM_BUILD				= sim_build/rtl
VERILOG_SOURCES += $(addprefix $(SRC_DIR)/,$(PROJECT_SOURCES))

else

# Gate level simulation:
SIM_BUILD				= sim_build/gl
COMPILE_ARGS    += -DGL_TEST
COMPILE_ARGS    += -DFUNCTIONAL
COMPILE_ARGS    += -DUSE_POWER_PINS
COMPILE_ARGS    += -DSIM
COMPILE_ARGS    += -DUNIT_DELAY=\#1
VERILOG_SOURCES += $(PDK_ROOT)/sky130A/libs.ref/sky130_fd_sc_hd/verilog/primitives.v
VERILOG_SOURCES += $(PDK_ROOT)/sky130A/libs.ref/sky130_fd_sc_hd/verilog/sky130_fd_sc_hd.v

# this gets copied in by the GDS action workflow
VERILOG_SOURCES += $(PWD)/gate_level_netlist.v

endif

# Allow sharing configuration between design and testbench via `include`:
COMPILE_ARGS 		+= -I$(SRC_DIR)

# Include the testbench sources:
VERILOG_SOURCES += $(PWD)/tb.v
TOPLEVEL = tb

endif # !LIU

# List test modules to run, separated by commas and without the .py suffix:
COCOTB_TEST_MODULES = test

# include cocotb's make rules to take care of the simulator setup
include $(shell cocotb-config --makefiles)/Makefile.sim
