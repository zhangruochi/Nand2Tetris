// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.


//m * n = m + m + m + ... + m


// @sum
// M=0
// @i
// M=1

// (LOOP)
// @i
// D=M
// @R0
// D=M-D
// @END
// D;JGT
// @R1
// sum=sum+M
// @i
// M=M+1
// @LOOP
// 0;JMP
// (END)
// @sum
// D=M
// @R2
// M=D




@sum
M=0   //sum=0
@i    //i=1
M=1
(LOOP)
@i    //D=i
D=M
@R0   
D=D-M  //D=I-R0
@END
D;JGT  // if(i-R0) > 0 goto END
@R1
D=M     //D=R1
@sum
M=D+M
@i
M=M+1
@LOOP
0;JMP   //Goto LOOP
(END)
@sum
D=M
@R2
M=D


