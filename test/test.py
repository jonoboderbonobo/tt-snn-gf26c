# SPDX-FileCopyrightText: © 2026 Jonas Boerschmann
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, FallingEdge

EN, DOWN, CLEAR = 0x01, 0x02, 0x04


async def ticks(dut, n):
    """Wait n rising edges, then to the falling edge so registered outputs have settled."""
    await ClockCycles(dut.clk, n)
    await FallingEdge(dut.clk)


async def start(dut):
    cocotb.start_soon(Clock(dut.clk, 10, unit="us").start())
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1
    await ticks(dut, 1)


@cocotb.test()
async def test_reset_and_hold(dut):
    await start(dut)
    assert dut.uo_out.value == 0
    await ticks(dut, 10)  # not enabled: must hold
    assert dut.uo_out.value == 0
    assert dut.uio_oe.value == 0


@cocotb.test()
async def test_count_up_down_clear(dut):
    await start(dut)
    dut.ui_in.value = EN
    await ticks(dut, 5)
    assert dut.uo_out.value == 5
    dut.ui_in.value = 0
    await ticks(dut, 3)
    assert dut.uo_out.value == 5  # hold
    dut.ui_in.value = EN | DOWN
    await ticks(dut, 2)
    assert dut.uo_out.value == 3
    dut.ui_in.value = EN | CLEAR
    await ticks(dut, 1)
    assert dut.uo_out.value == 0


@cocotb.test()
async def test_wrap(dut):
    await start(dut)
    dut.ui_in.value = EN | DOWN
    await ticks(dut, 1)
    assert dut.uo_out.value == 255  # 0 - 1 wraps
    dut.ui_in.value = EN
    await ticks(dut, 1)
    assert dut.uo_out.value == 0  # 255 + 1 wraps
