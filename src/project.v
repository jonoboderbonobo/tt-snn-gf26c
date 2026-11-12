/*
 * Copyright (c) 2026 Jonas Boerschmann
 * SPDX-License-Identifier: Apache-2.0
 *
 * Pipeline test: 8-bit up/down counter. Not a real design; it only checks
 * that the Tiny Tapeout flow (simulation, hardening, precheck) runs end to end.
 */

`default_nettype none

module tt_um_pipetest_counter (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

  wire en    = ui_in[0];  // count enable
  wire down  = ui_in[1];  // 0: count up, 1: count down
  wire clear = ui_in[2];  // synchronous clear

  reg [7:0] count;

  always @(posedge clk) begin
    if (!rst_n || clear) count <= 8'd0;
    else if (en) count <= down ? count - 8'd1 : count + 8'd1;
  end

  assign uo_out  = count;
  assign uio_out = 8'd0;
  assign uio_oe  = 8'd0;

  // List all unused inputs to prevent warnings
  wire _unused = &{ena, ui_in[7:3], uio_in, 1'b0};

endmodule
