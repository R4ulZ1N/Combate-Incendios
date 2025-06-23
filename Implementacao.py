from heapq import heapify, heappop, heappush

# Classe que representa um grafo com arestas ponderadas
class Graph:
    def __init__(self, graph: dict = {}):
        self.graph = graph
    
    # Adiciona uma aresta com peso entre dois nós.
    def adicionar_no(self, no1, no2, peso):
        if no1 not in self.graph:
            self.graph[no1] = {}
        self.graph[no1][no2] = peso
        if no2 not in self.graph:
            self.graph[no2] = {}
        self.graph[no2][no1] = peso

    # Algoritmo de Dijkstra para calcular a menor distância entre o nó raiz e os demais,
    # Escolhi o Dijkstra aqui porque o problema envolve o menor tempo de deslocamento em um grafo.
    def distancia_minima(self, raiz: str):
        distancias = {no: float("inf") for no in self.graph}
        distancias[raiz] = 0
        fila_de_prioridade = [(0, raiz)]
        heapify(fila_de_prioridade)
        visitados = set()

        while fila_de_prioridade:
            distancia_atual, no_atual = heappop(fila_de_prioridade)
            if no_atual in visitados:
                continue
            visitados.add(no_atual)

            for vizinho, peso in self.graph.get(no_atual, {}).items():
                distancia_prevista = distancia_atual + peso
                if distancia_prevista < distancias[vizinho]:
                    distancias[vizinho] = distancia_prevista
                    heappush(fila_de_prioridade, (distancia_prevista, vizinho))
        return distancias

# Representa uma brigada com uma determinada capacidade de combate por hora
class Brigada:
    def __init__(self, id_brigada: str, capacidade: float):
        self.id = id_brigada
        self.capacidade_por_hora = capacidade
        self.capacidade_diaria_total = capacidade * 12 # Capacidade total em km² por dia

# Representa um foco de incêndio com área e taxa de crescimento diárias
class Foco:
    def __init__(self, id_foco: str, area_inicial: float, fator_crescimento: float):
        self.id = id_foco
        self.area = area_inicial
        self.crescimento = fator_crescimento

# Classe para o Combate aos focos.
class Combate:
    def __init__(self, grafo: Graph, brigadas: list, focos: list):
        self.grafo = grafo
        self.brigadas = brigadas
        self.focos = focos

    # Simula um dia inteiro de combate
    def simular_dia(self):
        # Capacidade disponível de cada brigada para o dia atual
        capacidade_disponivel_brigadas = {b.id: b.capacidade_diaria_total for b in self.brigadas}
        
        # Crescimento dos focos no início do dia
        for foco in self.focos:
            if foco.area > 0:
                foco.area *= foco.crescimento
        
        print("--- Alocações do dia ---")

        # Ordena os focos: maior área e maior taxa de crescimento primeiro.
        focos_ordenados = sorted([f for f in self.focos if f.area > 0],key=lambda f: (f.area * f.crescimento),reverse=True)

        for foco in focos_ordenados:
            print(f"Foco {foco.id} - Área antes do combate: {foco.area:.2f} km²")
            
            # Lista para guardar as alocações para este foco neste dia
            alocacoes_para_foco = []
            
            # Tentar alocar brigadas para este foco até ele ser extinto ou não haver mais brigadas
            while foco.area > 0:
                melhor_alocacao_foco_brigada = None
                max_area_combatida_possivel = 0
                
                for brigada in self.brigadas:
                    if capacidade_disponivel_brigadas[brigada.id] <= 0:
                        continue # Esta brigada já esgotou sua capacidade diária

                    # Calcula a menor distância da brigada para o foco
                    distancias = self.grafo.distancia_minima(brigada.id)
                    distancia = distancias.get(foco.id, float('inf'))

                    if distancia == float('inf') or distancia >= 12: # Tempo de deslocamento inviável
                        continue

                    tempo_util = 12 - distancia
                    # Quanto a brigada PODE combater dado seu tempo útil e capacidade diária restante
                    area_de_combate = min(
                        tempo_util * brigada.capacidade_por_hora,
                        capacidade_disponivel_brigadas[brigada.id] # Não exceder a capacidade diária restante
                    )
                    
                    if area_de_combate > max_area_combatida_possivel:
                        max_area_combatida_possivel = area_de_combate
                        melhor_alocacao_foco_brigada = {
                            "brigada": brigada,
                            "distancia": distancia,
                            "tempo_combate": tempo_util,
                            "area_combatida": area_de_combate
                        }
                
                if melhor_alocacao_foco_brigada:
                    # Alocar a brigada escolhida para o foco
                    brigada_escolhida = melhor_alocacao_foco_brigada["brigada"]
                    area_a_combater = min(foco.area, melhor_alocacao_foco_brigada["area_combatida"])
                    
                    foco.area -= area_a_combater
                    capacidade_disponivel_brigadas[brigada_escolhida.id] -= area_a_combater # Deduz da capacidade diária
                    
                    if foco.area < 0: foco.area = 0 # Não deixar a área negativa

                    print(f"  {brigada_escolhida.id}: deslocamento={melhor_alocacao_foco_brigada['distancia']:.2f}h, tempo útil={melhor_alocacao_foco_brigada['tempo_combate']:.2f}h, combate para Foco {foco.id}={area_a_combater:.2f} km²")
                    alocacoes_para_foco.append({
                        "brigada_id": brigada_escolhida.id,
                        "foco_id": foco.id,
                        "area_combatida": area_a_combater
                    })
                    
                    # Se o foco foi extinto, pare de alocar brigadas para ele e vá para o próximo foco
                    if foco.area <= 0:
                        print(f"Foco {foco.id} extinto!")
                        break
                else:
                    # Nenhuma brigada viável ou com capacidade restante para este foco no momento
                    break 

            if foco.area > 0:
                print(f"Foco {foco.id} - Área restante após combate: {foco.area:.2f} km²")
        
        # Retorna o que foi alocado no dia (opcional, para registro)
        return alocacoes_para_foco 

    # Executa a simulação até que todos os focos sejam extintos ou um limite de dias seja atingido
    def simular_ate_extincao(self):
        dia = 0
        MAX_DIAS = 100 # Limite de dias para a extinção dos focos.

        while any(f.area > 0 for f in self.focos):
            if dia >= MAX_DIAS:
                print("--- Limite de dias atingido. ---")
                break

            dia += 1
            print(f"--- DIA {dia} ---")
            self.simular_dia() # A função simular_dia já imprime os detalhes

            # Resumo do estado dos focos no final do dia
            print("--- Resumo do Dia ---")
            for foco in self.focos:
                print(f"Foco {foco.id}: Área = {foco.area:.2f} km² (Crescimento diário: {foco.crescimento})")

        if all(f.area <= 0 for f in self.focos):
            print(f"--- Simulação Concluída ---")
            print(f"Todos os focos extintos em {dia} dias.")
        else:
            print(f"--- Simulação Concluída ---")
            print(f"Alguns focos não puderam ser extintos após {dia} dias.")

# --- FUNÇÃO DE LEITURA DE ENTRADA ---
def read_input():

    # Linha 1: número de focos e de brigadas
    n_focos, n_brigadas = map(int, input().split())

    # Linha 2: capacidade de combate de cada brigada
    capacidades_brigadas = list(map(float, input().split()))

    # Linha 3: área inicial de cada foco
    areas_focos = list(map(float, input().split()))

    # Linha 4: fator crescimento de cada foco
    fatores_crescimento = list(map(float, input().split()))

    # Criação das instâncias de Brigada e Foco
    brigadas = [Brigada(f"B{i+1}", capacidades_brigadas[i]) for i in range(n_brigadas)]
    focos = [Foco(f"F{i+1}", areas_focos[i], fatores_crescimento[i]) for i in range(n_focos)]

    # Para ler a matriz, vamos assumir que as entradas são strings "nó1 nó2 peso"
    graph_data = {}
    print("\nPor favor, insira as arestas do grafo no formato 'Nó1 Nó2 Peso' (Ex: 'B1 F1 1').")
    print("Pressione Enter em uma linha vazia para finalizar a entrada do grafo.")
    
    while True:
        try:
            line = input().strip()
            if not line:
                break
            parts = line.split()
            if len(parts) == 3:
                node1, node2, weight_str = parts
                weight = float(weight_str) # Pode ser float se o tempo for decimal
                
                if node1 not in graph_data:
                    graph_data[node1] = {}
                if node2 not in graph_data:
                    graph_data[node2] = {}
                
                graph_data[node1][node2] = weight
                graph_data[node2][node1] = weight # Assumindo grafo não-direcionado para distâncias
            else:
                print("Formato de aresta inválido. Use 'Nó1 Nó2 Peso'.")
        except ValueError:
            print("Peso inválido. Certifique-se de que é um número.")
        except Exception as e:
            print(f"Erro ao ler a aresta: {e}")
            
    G = Graph(graph_data)
    
    # Adicionar nós que podem estar nas brigadas/focos mas não têm arestas no grafo ainda
    # Isso garante que todos os nós relevantes estejam no grafo para o Dijkstra
    for b in brigadas:
        if b.id not in G.graph:
            G.graph[b.id] = {}
    for f in focos:
        if f.id not in G.graph:
            G.graph[f.id] = {}


    return G, brigadas, focos

# --- EXECUÇÃO ---
if __name__ == "__main__":
    G, brigadas, focos = read_input()

    # Inicia a simulação de combate
    c = Combate(G, brigadas, focos)
    c.simular_ate_extincao()

# Exemplo:
    # 2 3
    # 10 8 5
    # 100 87
    # 1.5 1.25
    # B1 F1 1
    # B1 F2 2
    # B2 F1 3
    # B2 B3 2
    # B3 F2 4
    # F1 F2 3
