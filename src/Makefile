SIM ?= ghdl
TOPLEVEL_LANG ?= vhdl

PWD := $(shell pwd)

VHDL_SOURCES := $(shell find "$(PWD)" -type f \( -name '*.vhd' -o -name '*.vhdl' \) 2>/dev/null)

COCOTB_TOPLEVEL ?= lwdf
COCOTB_TEST_MODULES ?= tb

include $(shell cocotb-config --makefiles)/Makefile.sim
