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

## Divisao inicial do trabalho

- Daniel: administracao do repositorio, `parseExpressao`, `gerarAssembly` e `lerArquivo`
- Victor: `executarExpressao`, memoria, `RES` e testes do executor
- Giovanni: `main`, `exibirResultados`, integracao e testes de fluxo

## Estrutura prevista

- `main.py`: ponto de entrada
- `src/lexer.py`: `parseExpressao` e estados do AFD
- `src/executor.py`: `executarExpressao`
- `src/assembly.py`: `gerarAssembly`
- `src/arquivos.py`: leitura de arquivo e persistencia das saidas
- `src/exibicao.py`: exibicao dos resultados
- `src/tipos.py`: estruturas compartilhadas
- `tests/`: testes unitarios e de integracao

## Proximos passos

- fechar assinaturas das funcoes obrigatorias
- subir o primeiro conjunto de testes
- integrar o fluxo por partes sem misturar responsabilidades
