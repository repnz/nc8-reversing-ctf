; This is used to move the value in 0x1000 to a readable address (0x0)
jmp .start

.source_address dw 0x1000
.dest_address   dw 0x00
.bytes_to_copy  dw 0x20


.start
    #define source_address r3
    #define dest_address r2
    #define end_address r1


    push [.source_address]
    pop $source_address

    push [.dest_address]
    pop $dest_address

    push [.bytes_to_copy]
    pop $end_address
    add $end_address, $source_address

    .loop_start
        mov r0, [$source_address]
        mov [$dest_address], r0
        mov r0, 1
        add $source_address, r0
        add $dest_address, r0
        push $end_address
        pop r0
        xor r0, $source_address
        jz .end
        jmp .jmp_to_start
    .end
        push r13
        pop pc
        ._loop_start dw .loop_start

     .jmp_to_start
        push [._loop_start]
        pop pc