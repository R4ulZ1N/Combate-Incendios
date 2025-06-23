# Combate-Incendios
Projeto destinado ao trabalho proposto na matéria de Estrutura de Dados.

Enunciado:
Suponha que um país esteja enfrentando uma série de emergências causadas por múltiplos focos de incêndio (f₁, f₂, ..., fₙ), espalhados por diferentes regiões. Para conter os danos, existem diversos postos de brigadistas (b₁, b₂, ..., bₖ) distribuídos pelo território. Cada posto possui uma capacidade específica de combate a incêndios, medida em área que pode ser controlada por hora (em km²), a qual pode variar conforme o porte e os recursos do posto.

Considere, neste trabalho, que os brigadistas atuam contra o fogo durante 12 horas diárias. Cada foco de incêndio possui uma área inicial e uma taxa de crescimento diária α, com 1 < α ≤ 2, que representa o aumento proporcional da área afetada em cada período.

O atendimento a um foco pode ser feito por múltiplos postos. De modo análogo, um mesmo posto pode atuar em mais de um foco simultaneamente, respeitando sua capacidade total de operação.

O cenário será representado por um grafo, cujos vértices correspondem aos focos de incêndio (com nomes iniciados por f) e aos postos de brigadistas (com nomes iniciados por b). Haverá uma aresta entre dois vértices sempre que houver viabilidade de deslocamento entre eles. Cada aresta possui um custo associado, correspondente ao tempo de deslocamento (em horas), o qual será subtraído do tempo útil disponível para atuação dos brigadistas no combate ao foco no respectivo dia.

A redução da área de cada foco depende dos postos alocados para o seu atendimento, do tempo efetivamente disponível após o deslocamento e da capacidade alocada por cada posto. O planejamento deve considerar uma alocação diária de recursos e permitir o acompanhamento da evolução da área dos focos ao longo do tempo.
O objetivo deste trabalho é, dado o mapa do país, as capacidades de cada posto de brigadistas e os dados de cada foco de incêndio, determinar uma estratégia viável de atuação que permita extinguir todos os focos. A solução deve indicar:
quais focos são atendidos por cada posto;
a quantidade de recursos alocados por posto e por foco, em cada dia de planejamento;
o dia em que cada foco é considerado extinto (quando sua área atinge zero);
o tempo total necessário para extinguir todos os focos.

Caso não seja possível conter todos os incêndios com os recursos disponíveis, a solução deve informar que não há capacidade suficiente para controlar todos os focos. A estratégia proposta não precisa ser ótima, mas soluções que resultem em menor tempo total de operação serão consideradas superiores.
