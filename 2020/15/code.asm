%define target 30000000

global _start

SYS_READ    equ 0
SYS_WRITE   equ 1
SYS_EXIT    equ 60

STDIN       equ 0
STDOUT      equ 1


SECTION .bss
    c                         resq 1         ; input char
    n                         resq 1         ; current input number
    t                         resq 1         ; current turn
    turns                     resq target    ; turn array


SECTION .text

read:
    push    rbx

    mov     rdx, 1
    lea     rsi, [c]
    mov     rdi, STDIN
    .one_more:
    mov     rax, SYS_READ
    syscall
    cmp     rax, 0
    je      .done

    cmp     BYTE [c], ','
    je      .next_num
    cmp     BYTE [c], 10
    je      .done

    imul    rbx, QWORD [n], 10
    add     rbx, QWORD [c]
    sub     rbx, '0'
    mov     QWORD [n], rbx

    jmp     .one_more

    .next_num:
    mov     rbx, QWORD [n]
    lea     rbx, [turns + rbx * 8]
    push    QWORD [t]
    pop     QWORD [rbx]

    mov     QWORD [n], 0
    inc     QWORD [t]
    jmp     .one_more

    .done:
    pop     rbx
    ret


_start:
    push    rbx

    mov     QWORD [t], 1
    mov     QWORD [n], 0

    call    read

    .again:
    mov     rbx, [n]
    lea     rbx, [turns + rbx * 8]
    mov     rax, [rbx]
    push    QWORD [t]    ; |
    pop     QWORD [rbx]  ; | turns[n] = t
    cmp     rax, 0
    jne     .seen

    mov     QWORD [n], 0  ; n = 0
    jmp     .check

    .seen:
    mov     rdi, rax  ; |
    mov     rax, [t]  ; |
    sub     rax, rdi  ; | n = t - turns[n]
    mov     [n], rax  ; |

    .check:
    inc     QWORD [t]
    cmp     QWORD [t], target
    jl      .again

    .done:
    mov     rdx, 8
    lea     rsi, [n]
    mov     rdi, STDOUT
    mov     rax, SYS_WRITE
    syscall

    pop     rbx

    mov     rdi, [n]
    mov     rax, SYS_EXIT
    syscall