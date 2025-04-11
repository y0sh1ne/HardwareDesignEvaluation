module ExactMul(CLK,a,b,y);
    input CLK;
    input [8:1] a, b;
    output [8*2:1] y;
    assign y = a * b;
endmodule