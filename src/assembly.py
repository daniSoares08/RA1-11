# Grupo: RA1 11
# Daniel Campos Soares - daniSoares08
# Giovanni Bandeira Malucelli - Giomalu
# Victor Vanini Meyer - VictorMeyer1

from __future__ import annotations

from src.tipos import EstadoPrograma, NoExpressao, PlanoLinha, TipoNo

ROTINAS_OPERADORES = {
    "+": "op_add_double",
    "-": "op_sub_double",
    "*": "op_mul_double",
    "/": "op_div_double",
    "//": "op_idiv_int",
    "%": "op_mod_int",
    "^": "op_pow_double",
}


def gerarProgramaAssembly(planos: list[PlanoLinha], estado_programa: EstadoPrograma) -> str:
    linhas: list[str] = []
    constantes = mapearConstantes(planos)

    emitirCabecalho(linhas)
    emitirSecaoDados(linhas, planos, estado_programa, constantes)
    emitirSecaoTexto(linhas, planos, constantes)
    emitirRotinasBase(linhas)

    return "\n".join(linhas) + "\n"


def gerarAssembly(
    tokens: list[str],
    codigoAssembly: list[str],
    plano: PlanoLinha | None = None,
    constantes: dict[str, str] | None = None,
) -> None:
    if plano is None:
        from src.executor import executarExpressao

        plano = executarExpressao(tokens, EstadoPrograma(), 1)

    if constantes is None:
        constantes = mapearConstantes([plano])

    emitirExpressao(plano.arvore, codigoAssembly, constantes, plano.indice_linha)
    codigoAssembly.append("    bl pop_d0")
    codigoAssembly.append("    ldr r0, ={0}".format(plano.rotulo_resultado))
    codigoAssembly.append("    vstr d0, [r0]")


def emitirCabecalho(linhas: list[str]) -> None:
    linhas.append(".syntax unified")
    linhas.append(".fpu vfpv3")
    linhas.append(".global _start")
    linhas.append("")


def emitirSecaoDados(
    linhas: list[str],
    planos: list[PlanoLinha],
    estado_programa: EstadoPrograma,
    constantes: dict[str, str],
) -> None:
    linhas.append(".data")
    linhas.append(".align 3")

    for valor, rotulo_constante in constantes.items():
        linhas.append("{0}: .double {1}".format(rotulo_constante, valor))

    linhas.append("const_zero_double: .double 0.0")
    linhas.append("const_one_double: .double 1.0")
    linhas.append("temp_pow_base: .double 0.0")

    for plano in planos:
        linhas.append("{0}: .double 0.0".format(plano.rotulo_resultado))

    for memoria in sorted(estado_programa.memorias):
        linhas.append("mem_{0}: .double 0.0".format(memoria))

    linhas.append("pilha_topo: .word 0")
    linhas.append("pilha_valores: .space 4096")
    linhas.append("")


def emitirSecaoTexto(
    linhas: list[str],
    planos: list[PlanoLinha],
    constantes: dict[str, str],
) -> None:
    linhas.append(".text")
    linhas.append("_start:")
    linhas.append("    ldr r0, =pilha_topo")
    linhas.append("    mov r1, #0")
    linhas.append("    str r1, [r0]")

    for plano in planos:
        linhas.append("")
        linhas.append("linha_{0}:".format(plano.indice_linha))
        gerarAssembly(plano.tokens, linhas, plano, constantes)

    linhas.append("")
    linhas.append("fim:")
    linhas.append("    b fim")
    linhas.append("")


def emitirExpressao(
    no: NoExpressao,
    linhas: list[str],
    constantes: dict[str, str],
    indice_linha_atual: int,
) -> None:
    if no.tipo == TipoNo.NUMERO and no.valor is not None:
        rotulo = constantes[no.valor]
        linhas.append("    ldr r0, ={0}".format(rotulo))
        linhas.append("    vldr d0, [r0]")
        linhas.append("    bl push_d0")
        return

    if no.tipo == TipoNo.MEMORIA_LEITURA and no.valor is not None:
        linhas.append("    ldr r0, =mem_{0}".format(no.valor))
        linhas.append("    vldr d0, [r0]")
        linhas.append("    bl push_d0")
        return

    if no.tipo == TipoNo.RESULTADO_ANTERIOR and no.valor is not None:
        rotulo = "resultado_linha_{0}".format(indice_linha_atual - int(no.valor))
        linhas.append("    ldr r0, ={0}".format(rotulo))
        linhas.append("    vldr d0, [r0]")
        linhas.append("    bl push_d0")
        return

    if no.tipo == TipoNo.MEMORIA_ESCRITA and no.valor is not None and no.esquerda is not None:
        emitirExpressao(no.esquerda, linhas, constantes, indice_linha_atual)
        linhas.append("    bl pop_d0")
        linhas.append("    ldr r0, =mem_{0}".format(no.valor))
        linhas.append("    vstr d0, [r0]")
        linhas.append("    bl push_d0")
        return

    if (
        no.tipo == TipoNo.OPERACAO
        and no.operador is not None
        and no.esquerda is not None
        and no.direita is not None
    ):
        emitirExpressao(no.esquerda, linhas, constantes, indice_linha_atual)
        emitirExpressao(no.direita, linhas, constantes, indice_linha_atual)
        linhas.append("    bl {0}".format(ROTINAS_OPERADORES[no.operador]))
        return

    raise ValueError("No invalido para geracao de Assembly")


def mapearConstantes(planos: list[PlanoLinha]) -> dict[str, str]:
    constantes: dict[str, str] = {}

    for plano in planos:
        coletarConstantes(plano.arvore, constantes)

    return constantes


def coletarConstantes(no: NoExpressao, constantes: dict[str, str]) -> None:
    if no.tipo == TipoNo.NUMERO and no.valor is not None and no.valor not in constantes:
        constantes[no.valor] = "const_{0}".format(len(constantes))

    if no.esquerda is not None:
        coletarConstantes(no.esquerda, constantes)

    if no.direita is not None:
        coletarConstantes(no.direita, constantes)


def emitirRotinasBase(linhas: list[str]) -> None:
    linhas.extend(
        [
            "push_d0:",
            "    ldr r1, =pilha_topo",
            "    ldr r2, [r1]",
            "    ldr r3, =pilha_valores",
            "    add r3, r3, r2",
            "    vstr d0, [r3]",
            "    add r2, r2, #8",
            "    str r2, [r1]",
            "    bx lr",
            "",
            "pop_d0:",
            "    ldr r1, =pilha_topo",
            "    ldr r2, [r1]",
            "    cmp r2, #0",
            "    beq pop_d0_vazio",
            "    sub r2, r2, #8",
            "    str r2, [r1]",
            "    ldr r3, =pilha_valores",
            "    add r3, r3, r2",
            "    vldr d0, [r3]",
            "    bx lr",
            "pop_d0_vazio:",
            "    ldr r0, =const_zero_double",
            "    vldr d0, [r0]",
            "    bx lr",
            "",
            "pop_d1:",
            "    ldr r1, =pilha_topo",
            "    ldr r2, [r1]",
            "    cmp r2, #0",
            "    beq pop_d1_vazio",
            "    sub r2, r2, #8",
            "    str r2, [r1]",
            "    ldr r3, =pilha_valores",
            "    add r3, r3, r2",
            "    vldr d1, [r3]",
            "    bx lr",
            "pop_d1_vazio:",
            "    ldr r0, =const_zero_double",
            "    vldr d1, [r0]",
            "    bx lr",
            "",
            "op_add_double:",
            "    bl pop_d1",
            "    bl pop_d0",
            "    vadd.f64 d0, d0, d1",
            "    bl push_d0",
            "    bx lr",
            "",
            "op_sub_double:",
            "    bl pop_d1",
            "    bl pop_d0",
            "    vsub.f64 d0, d0, d1",
            "    bl push_d0",
            "    bx lr",
            "",
            "op_mul_double:",
            "    bl pop_d1",
            "    bl pop_d0",
            "    vmul.f64 d0, d0, d1",
            "    bl push_d0",
            "    bx lr",
            "",
            "op_div_double:",
            "    bl pop_d1",
            "    bl pop_d0",
            "    vdiv.f64 d0, d0, d1",
            "    bl push_d0",
            "    bx lr",
            "",
            "op_idiv_int:",
            "    bl pop_d1",
            "    bl pop_d0",
            "    vcvt.s32.f64 s0, d0",
            "    vcvt.s32.f64 s1, d1",
            "    vmov r0, s0",
            "    vmov r1, s1",
            "    cmp r1, #0",
            "    beq op_idiv_zero",
            "    bl dividir_inteiros_assinados",
            "    vmov s0, r2",
            "    vcvt.f64.s32 d0, s0",
            "    bl push_d0",
            "    bx lr",
            "op_idiv_zero:",
            "    ldr r0, =const_zero_double",
            "    vldr d0, [r0]",
            "    bl push_d0",
            "    bx lr",
            "",
            "op_mod_int:",
            "    bl pop_d1",
            "    bl pop_d0",
            "    vcvt.s32.f64 s0, d0",
            "    vcvt.s32.f64 s1, d1",
            "    vmov r0, s0",
            "    vmov r1, s1",
            "    cmp r1, #0",
            "    beq op_mod_zero",
            "    bl dividir_inteiros_assinados",
            "    vmov s0, r3",
            "    vcvt.f64.s32 d0, s0",
            "    bl push_d0",
            "    bx lr",
            "op_mod_zero:",
            "    ldr r0, =const_zero_double",
            "    vldr d0, [r0]",
            "    bl push_d0",
            "    bx lr",
            "",
            "op_pow_double:",
            "    bl pop_d1",
            "    bl pop_d0",
            "    vcvt.s32.f64 s0, d1",
            "    vmov r0, s0",
            "    ldr r1, =temp_pow_base",
            "    vstr d0, [r1]",
            "    ldr r1, =const_one_double",
            "    vldr d0, [r1]",
            "    cmp r0, #0",
            "    beq op_pow_done",
            "op_pow_loop:",
            "    ldr r1, =temp_pow_base",
            "    vldr d2, [r1]",
            "    vmul.f64 d0, d0, d2",
            "    subs r0, r0, #1",
            "    bne op_pow_loop",
            "op_pow_done:",
            "    bl push_d0",
            "    bx lr",
            "",
            "dividir_inteiros_assinados:",
            "    mov r2, #0",
            "    mov r3, #0",
            "    cmp r0, #0",
            "    bge dividir_assinados_dividendo_ok",
            "    rsb r0, r0, #0",
            "    eor r2, r2, #1",
            "    mov r3, #1",
            "dividir_assinados_dividendo_ok:",
            "    cmp r1, #0",
            "    bge dividir_assinados_divisor_ok",
            "    rsb r1, r1, #0",
            "    eor r2, r2, #1",
            "dividir_assinados_divisor_ok:",
            "    mov r12, #0",
            "dividir_assinados_loop:",
            "    cmp r0, r1",
            "    blt dividir_assinados_fim_loop",
            "    sub r0, r0, r1",
            "    add r12, r12, #1",
            "    b dividir_assinados_loop",
            "dividir_assinados_fim_loop:",
            "    cmp r2, #0",
            "    beq dividir_assinados_sinal_quociente_ok",
            "    rsb r12, r12, #0",
            "dividir_assinados_sinal_quociente_ok:",
            "    cmp r3, #0",
            "    beq dividir_assinados_sinal_resto_ok",
            "    rsb r0, r0, #0",
            "dividir_assinados_sinal_resto_ok:",
            "    mov r2, r12",
            "    mov r3, r0",
            "    bx lr",
        ]
    )
