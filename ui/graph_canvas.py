"""Canvas para dibujar y manipular el grafo."""

import tkinter as tk
import math

from config.colors import COLORS, UI_COLORS, NODE_RADIUS


class GraphCanvas:
    """Encapsula el canvas de tkinter para dibujar grafos."""
    
    def __init__(self, parent):
        """
        Inicializa el canvas del grafo.
        
        Args:
            parent: Widget padre de tkinter
        """
        self.frame = tk.Frame(parent, bg=UI_COLORS['bg_separator'], bd=2, relief='solid')
        
        self.canvas = tk.Canvas(
            self.frame,
            bg=UI_COLORS['bg_canvas'],
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
    
    def bind_click(self, callback):
        """Vincula un callback al evento de click."""
        self.canvas.bind('<Button-1>', callback)
    
    def create_node(self, x, y, label):
        """
        Crea un nodo visual en el canvas.
        
        Args:
            x: Posición X
            y: Posición Y
            label: Etiqueta del nodo
            
        Returns:
            Tupla (circle_id, text_id)
        """
        circle_id = self.canvas.create_oval(
            x - NODE_RADIUS, y - NODE_RADIUS,
            x + NODE_RADIUS, y + NODE_RADIUS,
            fill=COLORS['unvisited'],
            outline='#333333',
            width=2
        )
        
        text_id = self.canvas.create_text(
            x, y, text=label,
            font=('Helvetica', 14, 'bold'),
            fill='#333333'
        )
        
        return circle_id, text_id
    
    def create_edge(self, x1, y1, x2, y2):
        """
        Crea una arista visual en el canvas.
        
        Args:
            x1, y1: Coordenadas del primer nodo
            x2, y2: Coordenadas del segundo nodo
            
        Returns:
            ID de la línea creada
        """
        line_id = self.canvas.create_line(
            x1, y1, x2, y2,
            fill=COLORS['edge'],
            width=3
        )
        self.canvas.tag_lower(line_id)
        return line_id
    
    def delete_item(self, item_id):
        """Elimina un elemento del canvas."""
        self.canvas.delete(item_id)
    
    def delete_all(self):
        """Elimina todos los elementos del canvas."""
        self.canvas.delete('all')
    
    def set_node_color(self, circle_id, text_id, color):
        """
        Cambia el color de un nodo.
        
        Args:
            circle_id: ID del círculo
            text_id: ID del texto
            color: Nuevo color de relleno
        """
        self.canvas.itemconfig(circle_id, fill=color)
        text_color = '#ffffff' if color in [COLORS['current'], COLORS['visited']] else '#333333'
        self.canvas.itemconfig(text_id, fill=text_color)
    
    def set_edge_color(self, line_id, color):
        """Cambia el color de una arista."""
        self.canvas.itemconfig(line_id, fill=color)
    
    def set_node_outline(self, circle_id, outline_color, width):
        """Cambia el contorno de un nodo."""
        self.canvas.itemconfig(circle_id, outline=outline_color, width=width)
    
    def get_node_at(self, x, y, nodes):
        """
        Encuentra el nodo en una posición dada.
        
        Args:
            x, y: Coordenadas del click
            nodes: Diccionario de nodos del grafo
            
        Returns:
            ID del nodo o None
        """
        for node_id, data in nodes.items():
            dx = x - data['x']
            dy = y - data['y']
            if math.sqrt(dx*dx + dy*dy) <= NODE_RADIUS:
                return node_id
        return None
    
    def get_edge_at(self, x, y, edges, nodes):
        """
        Encuentra la arista cercana a una posición.
        
        Args:
            x, y: Coordenadas del click
            edges: Lista de aristas
            nodes: Diccionario de nodos
            
        Returns:
            Índice de la arista o None
        """
        tolerance = 10
        for i, (n1, n2, _) in enumerate(edges):
            x1, y1 = nodes[n1]['x'], nodes[n1]['y']
            x2, y2 = nodes[n2]['x'], nodes[n2]['y']
            
            line_len = math.sqrt((x2-x1)**2 + (y2-y1)**2)
            if line_len == 0:
                continue
            
            t = max(0, min(1, ((x-x1)*(x2-x1) + (y-y1)*(y2-y1)) / (line_len**2)))
            proj_x = x1 + t * (x2-x1)
            proj_y = y1 + t * (y2-y1)
            
            dist = math.sqrt((x-proj_x)**2 + (y-proj_y)**2)
            if dist <= tolerance:
                return i
        return None
