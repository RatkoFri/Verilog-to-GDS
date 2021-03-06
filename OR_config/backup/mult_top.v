module mult_top(
    // Clock and reset
    input clk,
    // Input X has a form x_i%d where %d denotes the bit number
    input  [15:0] x,
    // Input Y has a form y_i%d where %d denotes the bit number
    input  [15:0] y,
    // Output P has a form p_out%d where %d denotes the bit number
    output reg [31:0] p
    );

    reg [15:0] X_vec;
    reg [15:0] Y_vec;
    // Now we have X_vec and Y_vec signal
    // Then we do processing with these signals and store the
    // intermidiate result in P_vec
    // For example purposes X_vec and Y_vec are concanated and stored in P_vec
    wire [31:0] P_vec;

        ADaPT_shift_w4Q8_v2 mult(.x(X_vec),.y(Y_vec),.p(P_vec));


    always @(posedge clk)
    begin
        X_vec = x;
        Y_vec = y;
        p = P_vec;
    end

endmodule