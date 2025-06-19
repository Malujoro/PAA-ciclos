import os
import networkx as nx
import matplotlib.pyplot as plt
import random
import csv

# Função para gerar um grafo direcional
def gerar_grafo(quant_nos: int, prob_conexao: float = 0.3):
    grafo = nx.DiGraph()

    # Gera e adiciona os nós
    nos = [f"t{i + 1}" for i in range(quant_nos)]
    grafo.add_nodes_from(nos)

    # Adiciona arestas com peso aleatório
    for i in range(quant_nos):
        for j in range(quant_nos):
            if (i != j and random.random() < prob_conexao):
                grafo.add_edge(nos[i], nos[j])

    return grafo


# Função para salvar a imagem de um grafo
def salvar_grafo_imagem(grafo: nx.Graph, pasta: str = '', nome: str = 'grafo.png'):
    os.makedirs(pasta, exist_ok=True)
    caminho = os.path.join(pasta, nome)

    pos = nx.circular_layout(grafo)

    # Aumenta o tamanho da figura
    plt.figure(figsize=(10, 10))

    # Desenhando o grafo
    nx.draw(grafo, pos, with_labels=True, node_color='skyblue', node_size=800,
            edge_color='gray', arrows=True, arrowsize=30, connectionstyle='arc3,rad=0.1', width=2)

    # Salvando a imagem
    plt.title(
        f"Dígrafo com {grafo.number_of_nodes()} nós")
    plt.savefig(caminho, format='png', dpi=300)
    plt.close()


# Função para salvar as informações do grafo (nós e arestas) do grafo em um .csv
def salvar_grafo_csv(grafo: nx.Graph, pasta: str = '', nome: str = "grafo.csv"):
    os.makedirs(pasta, exist_ok=True)
    caminho = os.path.join(pasta, nome)

    with open(caminho, mode='w', newline='') as arquivo_csv:
        escritor = csv.writer(arquivo_csv)

        # Escrita do cabeçalho
        escritor.writerow(['no_origem', 'no_destino'])
        for u, v in grafo.edges():
            escritor.writerow([u, v])


if (__name__ == '__main__'):
    caminho = "grafos"
    quant_tabelas = 1000
    nome = f"grafo{quant_tabelas}"

    grafo = gerar_grafo(quant_tabelas, prob_conexao=0.005)
    salvar_grafo_imagem(grafo, pasta=caminho, nome=f"{nome}.png")
    salvar_grafo_csv(grafo, pasta=caminho, nome=f"{nome}.csv")