<!---
Datasheet source, built by the Tiny Tapeout docs action.
-->

## How it works

An 8-bit counter, `uo[7:0]`, clocked by `clk`. Reset (`rst_n` low) or `ui[2]` (synchronous clear) sets it to 0.
While `ui[0]` is high it counts: up when `ui[1]` is low, down when it is high. It wraps at 255 and 0.
All bidirectional pins are unused inputs.

This is a pipeline test for GF26c (GlobalFoundries 180 nm): it exists to check simulation, hardening and precheck, not to be useful.

## How to test

Apply a clock (any rate up to 100 kHz is fine), pulse `rst_n` low, set `ui[0]` high and watch `uo[7:0]` count.

## External hardware

None. A logic analyser or LEDs on `uo[7:0]`.
