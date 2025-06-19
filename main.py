import networkx as nx
import csv
from enum import Enum
import time
import tracemalloc

class Cor(Enum):
    BRANCO = 0
    CINZA = 1
    PRETO = 2

def ler_grafo_csv(caminho_csv: str, lista_nos=None):
    grafo = nx.DiGraph()

    with open(caminho_csv, mode='r', newline='') as arquivo_csv:
        leitor = csv.reader(arquivo_csv)
        next(leitor)

        for linha in leitor:
            origem, destino = linha
            grafo.add_edge(origem, destino)

    if (lista_nos):
        for no in lista_nos:
            if no not in grafo.nodes:
                grafo.add_node(no)

    limpar_grafo(grafo)
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


def linha(char: str = "=", tam: int = 70):
    print(char * tam)


if __name__ == '__main__':
    # nome_grafo = "grafo10.csv"
    # caminho_csv = f'grafos/{nome_grafo}'
    # grafo = ler_grafo_csv(caminho_csv)

    # exibir_grafo(grafo)

    # if (verificarCiclo(grafo)):
    #     print("Existe ciclo\n")
    # else:
    #     print("Não existe ciclo\n")

    # exibir_grafo(grafo)

    with open("tempos_ciclo.csv", mode="w", newline="") as arquivoCSV:
        writer = csv.writer(arquivoCSV)
        writer.writerow(["tamanho", "iteracao", "tempo", "memoria_pico_kb",])

        iteracoes = 30
        lista_tamanhos = [10, 100, 1_000, 1_000_000]

        for tamanho in lista_tamanhos:
            linha()

            nome_grafo = f"grafo{tamanho}.csv"
            caminho_csv = f'grafos/{nome_grafo}'
            lista_nos = [f"t{i + 1}" for i in range(tamanho)]
            grafo = ler_grafo_csv(caminho_csv, lista_nos)

            print(
                f"GRAFO COM {tamanho} TABELAS")

            for it in range(iteracoes):
                tracemalloc.start()
                tracemalloc.reset_peak()
                inicio = time.perf_counter()

                ciclo = verificarCiclo(grafo)

                fim = time.perf_counter()
                memoria_atual_b, memoria_pico_b = tracemalloc.get_traced_memory()
                tracemalloc.stop()

                tempo = fim - inicio

                csv_tempo = f"{tempo:.6f}"
                csv_memoria_pico = f"{memoria_pico_b / 1024:.2f}"

                print(
                    f"[{it + 1}ª Iteração] {csv_tempo} segundos, com pico de {csv_memoria_pico} bytes")

                writer.writerow(
                    [tamanho, it + 1, csv_tempo, csv_memoria_pico])

            if (ciclo):
                print("Existe ciclo\n")
            else:
                print("Não existe ciclo\n")

            linha(char="-", tam=60)
