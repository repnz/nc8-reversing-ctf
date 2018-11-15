jmp .jump_to_start

._start dw .start

.jump_to_start
    push [._start]
    pop pc

.a dw 1
.b dw 2
._a dw .a
._b dw .b

.start
	push [.a]
	pop r0
	
	push [.b]
	pop r1
	
	push [._compare]
	pop pc
	int 0

._compare dw .compare

.compare ; compare(char a, char b) if (a < b) r0 = 0;
	xor r2, r2
	add r2, r0

	xor r0, r0
	add r0, r2

	jz .return_zero

	push r1
	div r0, r1
	pop r1
	push r13 ; lr
	pop pc

.return_one
    mov r0, 1
    push r13
    pop pc

.return_zero
	xor r0, r0
	push r13
	pop pc