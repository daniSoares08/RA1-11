.syntax unified
.fpu vfpv3
.global _start

.data
.align 3
const_0: .double 3.14
const_1: .double 2.0
const_2: .double 10.0
const_3: .double 4.0
const_4: .double 3.0
const_5: .double 6.0
const_6: .double 7.0
const_7: .double 8.0
const_8: .double 9
const_9: .double 4
const_10: .double 3
const_11: .double 7.5
const_12: .double 2.5
const_zero_double: .double 0.0
const_one_double: .double 1.0
temp_pow_base: .double 0.0
resultado_linha_1: .double 0.0
resultado_linha_2: .double 0.0
resultado_linha_3: .double 0.0
resultado_linha_4: .double 0.0
resultado_linha_5: .double 0.0
resultado_linha_6: .double 0.0
resultado_linha_7: .double 0.0
resultado_linha_8: .double 0.0
resultado_linha_9: .double 0.0
resultado_linha_10: .double 0.0
mem_X: .double 0.0
pilha_topo: .word 0
pilha_valores: .space 4096

.text
_start:
    ldr r0, =pilha_topo
    mov r1, #0
    str r1, [r0]

linha_1:
    ldr r0, =const_0
    vldr d0, [r0]
    bl push_d0
    ldr r0, =const_1
    vldr d0, [r0]
    bl push_d0
    bl op_add_double
    bl pop_d0
    ldr r0, =resultado_linha_1
    vstr d0, [r0]

linha_2:
    ldr r0, =const_2
    vldr d0, [r0]
    bl push_d0
    ldr r0, =const_3
    vldr d0, [r0]
    bl push_d0
    bl op_sub_double
    ldr r0, =const_1
    vldr d0, [r0]
    bl push_d0
    ldr r0, =const_4
    vldr d0, [r0]
    bl push_d0
    bl op_add_double
    bl op_mul_double
    bl pop_d0
    ldr r0, =resultado_linha_2
    vstr d0, [r0]

linha_3:
    ldr r0, =const_5
    vldr d0, [r0]
    bl push_d0
    ldr r0, =const_6
    vldr d0, [r0]
    bl push_d0
    bl op_mul_double
    ldr r0, =const_7
    vldr d0, [r0]
    bl push_d0
    ldr r0, =const_1
    vldr d0, [r0]
    bl push_d0
    bl op_div_double
    bl op_add_double
    bl pop_d0
    ldr r0, =resultado_linha_3
    vstr d0, [r0]

linha_4:
    ldr r0, =const_8
    vldr d0, [r0]
    bl push_d0
    ldr r0, =const_9
    vldr d0, [r0]
    bl push_d0
    bl op_idiv_int
    bl pop_d0
    ldr r0, =resultado_linha_4
    vstr d0, [r0]

linha_5:
    ldr r0, =const_8
    vldr d0, [r0]
    bl push_d0
    ldr r0, =const_9
    vldr d0, [r0]
    bl push_d0
    bl op_mod_int
    bl pop_d0
    ldr r0, =resultado_linha_5
    vstr d0, [r0]

linha_6:
    ldr r0, =const_1
    vldr d0, [r0]
    bl push_d0
    ldr r0, =const_10
    vldr d0, [r0]
    bl push_d0
    bl op_pow_double
    bl pop_d0
    ldr r0, =resultado_linha_6
    vstr d0, [r0]

linha_7:
    ldr r0, =const_11
    vldr d0, [r0]
    bl push_d0
    bl pop_d0
    ldr r0, =mem_X
    vstr d0, [r0]
    bl push_d0
    bl pop_d0
    ldr r0, =resultado_linha_7
    vstr d0, [r0]

linha_8:
    ldr r0, =mem_X
    vldr d0, [r0]
    bl push_d0
    ldr r0, =const_12
    vldr d0, [r0]
    bl push_d0
    bl op_add_double
    bl pop_d0
    ldr r0, =resultado_linha_8
    vstr d0, [r0]

linha_9:
    ldr r0, =resultado_linha_7
    vldr d0, [r0]
    bl push_d0
    bl pop_d0
    ldr r0, =resultado_linha_9
    vstr d0, [r0]

linha_10:
    ldr r0, =resultado_linha_9
    vldr d0, [r0]
    bl push_d0
    ldr r0, =mem_X
    vldr d0, [r0]
    bl push_d0
    bl op_add_double
    ldr r0, =const_8
    vldr d0, [r0]
    bl push_d0
    ldr r0, =const_9
    vldr d0, [r0]
    bl push_d0
    bl op_mod_int
    ldr r0, =const_1
    vldr d0, [r0]
    bl push_d0
    bl op_mul_double
    bl op_div_double
    bl pop_d0
    ldr r0, =resultado_linha_10
    vstr d0, [r0]

fim:
    b fim

push_d0:
    ldr r1, =pilha_topo
    ldr r2, [r1]
    ldr r3, =pilha_valores
    add r3, r3, r2
    vstr d0, [r3]
    add r2, r2, #8
    str r2, [r1]
    bx lr

pop_d0:
    ldr r1, =pilha_topo
    ldr r2, [r1]
    cmp r2, #0
    beq pop_d0_vazio
    sub r2, r2, #8
    str r2, [r1]
    ldr r3, =pilha_valores
    add r3, r3, r2
    vldr d0, [r3]
    bx lr
pop_d0_vazio:
    ldr r0, =const_zero_double
    vldr d0, [r0]
    bx lr

pop_d1:
    ldr r1, =pilha_topo
    ldr r2, [r1]
    cmp r2, #0
    beq pop_d1_vazio
    sub r2, r2, #8
    str r2, [r1]
    ldr r3, =pilha_valores
    add r3, r3, r2
    vldr d1, [r3]
    bx lr
pop_d1_vazio:
    ldr r0, =const_zero_double
    vldr d1, [r0]
    bx lr

op_add_double:
    bl pop_d1
    bl pop_d0
    vadd.f64 d0, d0, d1
    bl push_d0
    bx lr

op_sub_double:
    bl pop_d1
    bl pop_d0
    vsub.f64 d0, d0, d1
    bl push_d0
    bx lr

op_mul_double:
    bl pop_d1
    bl pop_d0
    vmul.f64 d0, d0, d1
    bl push_d0
    bx lr

op_div_double:
    bl pop_d1
    bl pop_d0
    vdiv.f64 d0, d0, d1
    bl push_d0
    bx lr

op_idiv_int:
    bl pop_d1
    bl pop_d0
    vcvt.s32.f64 s0, d0
    vcvt.s32.f64 s1, d1
    vmov r0, s0
    vmov r1, s1
    cmp r1, #0
    beq op_idiv_zero
    bl dividir_inteiros_assinados
    vmov s0, r2
    vcvt.f64.s32 d0, s0
    bl push_d0
    bx lr
op_idiv_zero:
    ldr r0, =const_zero_double
    vldr d0, [r0]
    bl push_d0
    bx lr

op_mod_int:
    bl pop_d1
    bl pop_d0
    vcvt.s32.f64 s0, d0
    vcvt.s32.f64 s1, d1
    vmov r0, s0
    vmov r1, s1
    cmp r1, #0
    beq op_mod_zero
    bl dividir_inteiros_assinados
    vmov s0, r3
    vcvt.f64.s32 d0, s0
    bl push_d0
    bx lr
op_mod_zero:
    ldr r0, =const_zero_double
    vldr d0, [r0]
    bl push_d0
    bx lr

op_pow_double:
    bl pop_d1
    bl pop_d0
    vcvt.s32.f64 s0, d1
    vmov r0, s0
    ldr r1, =temp_pow_base
    vstr d0, [r1]
    ldr r1, =const_one_double
    vldr d0, [r1]
    cmp r0, #0
    beq op_pow_done
op_pow_loop:
    ldr r1, =temp_pow_base
    vldr d2, [r1]
    vmul.f64 d0, d0, d2
    subs r0, r0, #1
    bne op_pow_loop
op_pow_done:
    bl push_d0
    bx lr

dividir_inteiros_assinados:
    mov r2, #0
    mov r3, #0
    cmp r0, #0
    bge dividir_assinados_dividendo_ok
    rsb r0, r0, #0
    eor r2, r2, #1
    mov r3, #1
dividir_assinados_dividendo_ok:
    cmp r1, #0
    bge dividir_assinados_divisor_ok
    rsb r1, r1, #0
    eor r2, r2, #1
dividir_assinados_divisor_ok:
    mov r12, #0
dividir_assinados_loop:
    cmp r0, r1
    blt dividir_assinados_fim_loop
    sub r0, r0, r1
    add r12, r12, #1
    b dividir_assinados_loop
dividir_assinados_fim_loop:
    cmp r2, #0
    beq dividir_assinados_sinal_quociente_ok
    rsb r12, r12, #0
dividir_assinados_sinal_quociente_ok:
    cmp r3, #0
    beq dividir_assinados_sinal_resto_ok
    rsb r0, r0, #0
dividir_assinados_sinal_resto_ok:
    mov r2, r12
    mov r3, r0
    bx lr
