import matplotlib.pyplot as plt
import networkx as nx
import os
from cor import Cor
from main import limpar_grafo, nos_ordenados, ler_grafo_csv
from grafo import gerar_nos

class Desenho:
    def __init__(self, folder = "imagens"):
        self._etapa = 0
        self._folder = folder
        os.makedirs(folder, exist_ok=True)

    def desenhar_grafo(self, grafo):
        self._etapa += 1
        pos = nx.circular_layout(grafo)

        # Mapeando as cores do Enum para cores visuais
        cor_nos = []
        for no in grafo.nodes:
            cor = grafo.nodes[no].get('cor')

            if cor == Cor.BRANCO:
                cor_nos.append('white')
            elif cor == Cor.CINZA:
                cor_nos.append('gray')
            elif cor == Cor.PRETO:
                cor_nos.append('#404040')
            else:
                cor_nos.append('red')
            

        plt.figure(figsize=(8, 8))
        nx.draw(grafo, pos, with_labels=True, node_color=cor_nos,
                node_size=600, edge_color='gray', font_color='black')
        plt.title(f"Etapa {self._etapa} da DFS")
        plt.savefig(f"{self._folder}/dfs_etapa_{self._etapa:03d}.png")
        plt.close() 

def linha(char: str = "=", tam: int = 70):
    print(char * tam)


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

    desenho.desenhar_grafo(grafo)
    sucessores = list(grafo.successors(atual))

    for no in sucessores:
        if (grafo.nodes[no]['cor'] == Cor.CINZA):
            grafo.nodes[no]['cor'] = None
            return True

        if (grafo.nodes[no]['cor'] == Cor.PRETO):
            continue

        # Se for branco continua a busca
        if (verificarCicloAuxiliar(grafo, no)):
            return True

    noAtual['cor'] = Cor.PRETO
    desenho.desenhar_grafo(grafo)
    return False

if __name__ == '__main__':
    tamanhos = [5, 10]

    for tamanho in tamanhos:
        nome_grafo = f"grafo{tamanho}.csv"
        caminho_csv = f'grafos/{nome_grafo}'
        lista_nos = gerar_nos(tamanho)
        grafo = ler_grafo_csv(caminho_csv, lista_nos)

        folder = nome_grafo.split(".")[0]
        desenho = Desenho(folder=f"imagens/{folder}")
        # exibir_grafo(grafo)

        desenho.desenhar_grafo(grafo)

        if (verificarCiclo(grafo)):
            desenho.desenhar_grafo(grafo)
            print("Existe ciclo\n")
        else:
            print("Não existe ciclo\n")
        # exibir_grafo(grafo)
