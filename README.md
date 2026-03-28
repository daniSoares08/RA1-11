# RA1 11 - Fase 1

## Integrantes

- Daniel Campos Soares - `daniSoares08`
- Giovanni Bandeira Malucelli - `Giomalu`
- Victor Vanini Meyer - `VictorMeyer1`

## Informacoes da disciplina

- Instituicao: PUCPR
- Disciplina: Linguagens Formais e Compiladores
- Professor: Frank Coelho de Alcantara
- Grupo: RA1 11

## Objetivo

Implementar a fase 1 do trabalho de Compiladores:

- leitura de arquivo texto com expressoes em RPN
- analise lexica com AFD implementado por funcoes
- montagem da estrutura sintatica minima necessaria para gerar o codigo
- geracao de codigo Assembly para ARMv7 DEC1-SOC(v16.1)
- persistencia do ultimo arquivo de tokens gerado
- persistencia do ultimo codigo Assembly gerado

O codigo Python nao realiza os calculos das expressoes. Ele le o arquivo, valida os tokens e gera o Assembly que representa as operacoes.

## Estrutura

- `main.py`: ponto de entrada do programa
- `src/arquivos.py`: leitura do arquivo de entrada e persistencia das saidas
- `src/lexer.py`: `parseExpressao` e estados do AFD
- `src/executor.py`: `executarExpressao` e montagem da arvore de cada linha
- `src/assembly.py`: `gerarAssembly` e geracao do programa Assembly completo
- `src/exibicao.py`: `exibirResultados`
- `src/tipos.py`: estruturas de apoio
- `tests/`: testes unitarios e de integracao
- `saidas/`: artefatos da ultima execucao

## Requisitos

- Python 3.8 ou superior
- Execucao alvo do Assembly: Cpulator ARMv7 DEC1-SOC(v16.1)

## Como executar

```bash
python main.py teste1.txt
```

O programa processa um unico arquivo por execucao, sem menus interativos, e atualiza:

- `saidas/ultimo_tokens.txt`
- `saidas/ultimo_programa_armv7.s`

## Como testar

```bash
python -m unittest discover -s tests -v
```

## Arquivos de teste

Os arquivos `teste1.txt`, `teste2.txt` e `teste3.txt` contem pelo menos 10 linhas cada e cobrem:

- `+`, `-`, `*`, `/`, `//`, `%`, `^`
- escrita e leitura de memoria
- uso de `RES`
- expressoes aninhadas

## Saidas geradas

- `saidas/ultimo_tokens.txt`: tokens da ultima execucao
- `saidas/ultimo_programa_armv7.s`: Assembly gerado para a ultima execucao
