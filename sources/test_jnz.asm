jmp .jump_to_start

._start dw .start

.jump_to_start
    push [._start]
    pop pc

.r0 dw 0
.r1 dw 0

.start
	push [.r0]
	pop r0

	push [.r1]
	pop r1

mov r3, 1

.loop
    add r1, r3
    jnz .hello
    jmp .loop

    .hello
    int 1