import networkx as nx
import csv
from enum import Enum

class Cor(Enum):
    BRANCO = 0
    CINZA = 1
    PRETO = 2

def ler_grafo_csv(caminho_csv: str):
    grafo = nx.DiGraph()

    with open(caminho_csv, mode='r', newline='') as arquivo_csv:
        leitor = csv.reader(arquivo_csv)
        next(leitor)

        for linha in leitor:
            origem, destino = linha
            grafo.add_edge(origem, destino)

    return grafo

def limpar_grafo(grafo: nx.DiGraph):
    nos = nos_ordenados(grafo)
    for no in nos:
        grafo.nodes[no]['cor'] = Cor.BRANCO

def exibir_grafo(grafo):
    nos = nos_ordenados(grafo, data=True)
    for no, atributos in nos:
        print(f"Nó: {no}, Atributos: {atributos}")
    print()

def nos_ordenados(grafo, data=False):
    if data:
        return sorted(grafo.nodes(data=True), key=lambda x: x[0])
    else:
        return sorted(grafo.nodes())

def verificarCiclo(grafo):
    limpar_grafo(grafo)
    nos = nos_ordenados(grafo)
    for no in nos:
        if (grafo.nodes[no]['cor'] == Cor.BRANCO):
            if (verificarCicloAuxiliar(grafo, no)):
                return True
    return False

# Retorna se existe um ciclo ou não
def verificarCicloAuxiliar(grafo, atual):
    noAtual = grafo.nodes[atual]
    noAtual['cor'] = Cor.CINZA

    sucessores = list(grafo.successors(atual))

    for no in sucessores:
        if (grafo.nodes[no]['cor'] == Cor.CINZA):
            return True

        if (grafo.nodes[no]['cor'] == Cor.PRETO):
            continue

        # Se for branco continua a busca
        if (verificarCicloAuxiliar(grafo, no)):
            return True

    noAtual['cor'] = Cor.PRETO
    return False


if __name__ == '__main__':
    nome_grafo = "grafo1000.csv"
    caminho_csv = f'grafos/{nome_grafo}'
    grafo = ler_grafo_csv(caminho_csv)

    # exibir_grafo(grafo)

    if (verificarCiclo(grafo)):
        print("Existe ciclo\n")
    else:
        print("Não existe ciclo\n")

    # exibir_grafo(grafo)
