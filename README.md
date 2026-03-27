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

## Estado atual

- estrutura do projeto organizada
- leitura de arquivo e `main` sem menu interativo funcionando
- AFD de `parseExpressao` implementado por funcoes
- `executarExpressao` com memoria, `RES` e expressoes aninhadas integrado
- arquivos de teste e testes unitarios iniciais adicionados
- geracao final de Assembly segue em consolidacao

## Estrutura

- `main.py`: ponto de entrada do programa
- `src/arquivos.py`: leitura do arquivo de entrada
- `src/lexer.py`: `parseExpressao` e estados do AFD
- `src/executor.py`: `executarExpressao` e montagem da arvore de cada linha
- `src/assembly.py`: geracao do programa Assembly
- `src/exibicao.py`: `exibirResultados`
- `src/tipos.py`: estruturas de apoio
- `tests/`: testes unitarios e de integracao
