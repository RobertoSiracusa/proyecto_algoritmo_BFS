"""Estructura de datos del grafo."""


class Graph:
    """Representa un grafo no dirigido con nodos y aristas."""
    
    def __init__(self):
        """Inicializa un grafo vacío."""
        self.nodes = {}  # {node_id: {'x': int, 'y': int, 'label': str, 'circle_id': int, 'text_id': int}}
        self.edges = []  # [(node_id1, node_id2, line_id)]
        self.adjacency = {}  # {node_id: [neighbor_ids]}
        self._next_node_id = 0
        self._next_label = ord('A')
    
    @property
    def next_node_id(self):
        """Retorna el siguiente ID de nodo disponible."""
        return self._next_node_id
    
    @property
    def next_label(self):
        """Retorna la siguiente etiqueta disponible."""
        return chr(self._next_label)
    
    def add_node(self, x, y, circle_id, text_id):
        """
        Agrega un nuevo nodo al grafo.
        
        Args:
            x: Posición X del nodo
            y: Posición Y del nodo
            circle_id: ID del círculo en el canvas
            text_id: ID del texto en el canvas
            
        Returns:
            El ID del nodo creado
        """
        node_id = self._next_node_id
        label = chr(self._next_label)
        
        self.nodes[node_id] = {
            'x': x,
            'y': y,
            'label': label,
            'circle_id': circle_id,
            'text_id': text_id
        }
        self.adjacency[node_id] = []
        
        self._next_node_id += 1
        self._next_label += 1
        if self._next_label > ord('Z'):
            self._next_label = ord('A')
        
        return node_id
    
    def add_edge(self, node1, node2, line_id):
        """
        Agrega una arista entre dos nodos.
        
        Args:
            node1: ID del primer nodo
            node2: ID del segundo nodo
            line_id: ID de la línea en el canvas
            
        Returns:
            True si la arista fue creada, False si ya existía o es inválida
        """
        if node1 == node2:
            return False
        
        # Verificar si ya existe
        for n1, n2, _ in self.edges:
            if (n1 == node1 and n2 == node2) or (n1 == node2 and n2 == node1):
                return False
        
        self.edges.append((node1, node2, line_id))
        self.adjacency[node1].append(node2)
        self.adjacency[node2].append(node1)
        return True
    
    def remove_node(self, node_id):
        """
        Elimina un nodo y todas sus aristas.
        
        Args:
            node_id: ID del nodo a eliminar
            
        Returns:
            Lista de line_ids de las aristas eliminadas, o None si el nodo no existe
        """
        if node_id not in self.nodes:
            return None
        
        removed_line_ids = []
        edges_to_remove = []
        
        for i, (n1, n2, line_id) in enumerate(self.edges):
            if n1 == node_id or n2 == node_id:
                removed_line_ids.append(line_id)
                edges_to_remove.append(i)
                # Actualizar adyacencia
                if n1 != node_id and n1 in self.adjacency:
                    if node_id in self.adjacency[n1]:
                        self.adjacency[n1].remove(node_id)
                if n2 != node_id and n2 in self.adjacency:
                    if node_id in self.adjacency[n2]:
                        self.adjacency[n2].remove(node_id)
        
        for i in reversed(edges_to_remove):
            self.edges.pop(i)
        
        del self.nodes[node_id]
        del self.adjacency[node_id]
        
        return removed_line_ids
    
    def remove_edge(self, edge_index):
        """
        Elimina una arista por su índice.
        
        Args:
            edge_index: Índice de la arista a eliminar
            
        Returns:
            Tupla (node1, node2, line_id) de la arista eliminada
        """
        n1, n2, line_id = self.edges[edge_index]
        
        if n2 in self.adjacency[n1]:
            self.adjacency[n1].remove(n2)
        if n1 in self.adjacency[n2]:
            self.adjacency[n2].remove(n1)
        
        self.edges.pop(edge_index)
        return (n1, n2, line_id)
    
    def get_neighbors(self, node_id):
        """
        Obtiene los vecinos de un nodo.
        
        Args:
            node_id: ID del nodo
            
        Returns:
            Lista de IDs de nodos vecinos
        """
        return self.adjacency.get(node_id, [])
    
    def get_node(self, node_id):
        """
        Obtiene los datos de un nodo.
        
        Args:
            node_id: ID del nodo
            
        Returns:
            Diccionario con los datos del nodo o None
        """
        return self.nodes.get(node_id)
    
    def has_nodes(self):
        """Retorna True si el grafo tiene al menos un nodo."""
        return len(self.nodes) > 0
    
    def clear(self):
        """Limpia todo el grafo."""
        # Guardar los IDs de canvas para eliminar
        circle_ids = [n['circle_id'] for n in self.nodes.values()]
        text_ids = [n['text_id'] for n in self.nodes.values()]
        line_ids = [e[2] for e in self.edges]
        
        self.nodes.clear()
        self.edges.clear()
        self.adjacency.clear()
        self._next_node_id = 0
        self._next_label = ord('A')
        
        return circle_ids, text_ids, line_ids
