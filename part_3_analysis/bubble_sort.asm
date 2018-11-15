;.length_of_challenge

; TODO: SORT EACH BYTE OF THE CHALLENGE DATA
;       NOTE THAT ANY INTERRUPT DONE BETWEEN int 10 AND int 11 WILL RESET THE
;       INTERNAL CHALLENGE DATA.


push [._start]
pop pc
._start dw .start

.challenge_data db '\x00' * 32
.challenge_length dw 32
._challenge_data1 dw .challenge_data

.start	

    push [.challenge_length]
    pop r7

    push [._challenge_data1] ; WHERE THE CHALLENGE DATA IS WRITTEN
    pop r0
    int 10 ; GET CHALLENGE DATA, 32 BYTES WRITTEN TO R0 ADDRESS

    push r7 ; len
    push r0 ; buffer
	push [._sort]
	pop pc
	jmp .validate

._sort dw .sort
._challenge_data2 dw .challenge_data

.validate
	push [._challenge_data2] ; WHERE THE CHALLENGE DATA IS LOCATED
	pop r0
	int 11 ; VALIDATE THE CHALLENGE DATA IS SORTED. CHALLENGE DATA IS LOCATED AT R0,
		   ; ; AND IF SUCCESFUL, THE SECURITY CODE WILL BE WRITTEN AT R0.
	int 0

.sort ; (buffer, length)
	#define buffer r5
	#define i r11
	#define j r10
	#define first_address r9
	#define second_address r8
	#define buf_length r7
	#define n_min_i r6
    #define lr r4

	push r13
	pop $lr
	
	pop $buffer ; the buffer
	pop $buf_length ; len
	

	xor r3, r3
	push r3
	pop $i
	
	.first_loop
		.second_loop_initialize
			; j = 1
			mov r1, 1
			push r1
			pop $j
			
			; r6 = n - i
			push $i
			pop r0 ; i
			mov r1, -1
			mul r0, r1 ; -i
			push $buf_length
			pop r1
			add r0, r1
			push r0
			pop $n_min_i
			jmp .second_loop_condition
	
	._compare1 dw .compare
	
		.second_loop_condition
			push $j ; j
			pop r0
			
			push $n_min_i ; (n-1)
			pop r1
			
			push [._compare1]
			pop pc
			
			; if j < (n-1) goto loop body
			jz .second_loop_body
			
			; finish inner loop
			push [._first_loop_increment]
			pop pc
		
		._first_loop_increment dw .first_loop_increment
			
		.second_loop_body
		; first_address = arr+j
			push $j
			pop r0
			push $buffer
			pop r1
			add r0, r1 
			push r0
			pop $first_address
		
		; second_address = arr+[j-1]
			mov r1, -1
			add r0, r1
			push r0
			pop $second_address
		
		; if *first_address < *second_address
			push $first_address
			pop r0
			mov r0, [r0]
			
			push $second_address
			pop r1
			mov r1, [r1]

			push [._compare2]
			pop pc

			jz .jump_to_swap_elements

			push [._second_loop_increment]
			pop pc

		._compare2 dw .compare

		.jump_to_swap_elements
		    jmp .swap_elements

		._second_loop_increment dw .second_loop_increment
		._swap dw .swap
		
		.swap_elements
			push $first_address
			pop r0
			push $second_address
			pop r1
			push [._swap]
			pop pc

		.second_loop_increment
			push $j
			pop r0
			mov r1, 1
			add r0, r1
			push r0
			pop $j
			push [._second_loop_condition]
			pop pc
			
		._second_loop_condition dw .second_loop_condition

	.first_loop_increment
		; i++
		push $i
		pop r0
		mov r1, 1
		add r0, r1
		push r0
		pop $i

	.first_loop_condition
		; if (i == 32) end
		push $i ; i
		pop r0
		
		push $buf_length ; len
		pop r1
		
		xor r0, r1 
		jz .end_sort
		
		push [._first_loop]
		pop pc

    ._first_loop dw .first_loop
	.end_sort
		push $lr
		pop pc
		
		
.swap ; (char* r0, char* r1)
	push r1
	mov r1, [r1]
	mov r2, [r0]
	mov [r0], r1
	pop r0
	mov [r0], r2
	push r13
	pop pc
	


.compare ; compare(char a, char b) if (a < b) r0 = 0;
	xor r2, r2
	add r2, r0

	xor r0, r0
	add r0, r1

	jz .return_one

    xor r0, r0
    add r0, r2

	div r0, r1

	push r13 ; lr
	pop pc

.return_one
    mov r0, 1
    push r13
    pop pc
	
	
	
	
	
	
	

