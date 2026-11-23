# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.triggers import Timer


@cocotb.test()
async def walk_upstairs_and_back(dut):
    dut.ena.value = 1
    dut.clk.value = 0
    dut.rst_n.value = 1
    dut.uio_in.value = 0

    # Each step flips one switch. The light changes at every step.
    for downstairs, upstairs, light in [
        (0, 0, 0),
        (1, 0, 1),
        (1, 1, 0),
        (0, 1, 1),
    ]:
        dut.ui_in.value = (upstairs << 1) | downstairs
        await Timer(1, unit="us")
        assert int(dut.uo_out.value) == light, (
            f"Downstairs={downstairs}, upstairs={upstairs}: expected light={light}"
        )
        assert int(dut.uio_oe.value) == 0
        assert int(dut.uio_out.value) == 0
