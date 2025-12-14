"""Implementación del algoritmo BFS (Breadth-First Search)."""

from collections import deque


def generate_bfs_steps(graph, start_node):
    """
    Genera los pasos del algoritmo BFS para animación.
    
    Args:
        graph: Objeto Graph con los nodos y adyacencias
        start_node: ID del nodo inicial
        
    Returns:
        Lista de tuplas representando cada paso del algoritmo:
        - ('visit', node_id, queue_list): Nodo siendo visitado
        - ('enqueue', node_id, from_node_id, queue_list): Nodo agregado a la cola
        - ('done', node_id, queue_list): Nodo terminado de procesar
    """
    steps = []
    bfs_queue = deque([start_node])
    visited = {start_node}
    
    while bfs_queue:
        current = bfs_queue.popleft()
        steps.append(('visit', current, list(bfs_queue)))
        
        # Obtener vecinos ordenados
        neighbors = sorted(graph.get_neighbors(current))
        
        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                bfs_queue.append(neighbor)
                steps.append(('enqueue', neighbor, current, list(bfs_queue)))
        
        steps.append(('done', current, list(bfs_queue)))
    
    return steps
