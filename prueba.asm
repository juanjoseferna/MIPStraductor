lui $s0 0x1000
ori $s0 $s0 0xF000
addi $s1 $zero 0
addi $t2 $zero 0x3E8
slt $t0 $s1 $t2
beq $t0 $zero 0x0007
sll $t0 $s1 2
add $t0 $t0 $s0
lw $t1 $t0 0
sll $t1 $t1 3
sw $t1 $t0 0
addi $s1 $s1 1
j 0x400010
jr $ra