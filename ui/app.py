"""Aplicación principal del visualizador BFS."""

import tkinter as tk
from tkinter import messagebox

from config.colors import COLORS, UI_COLORS
from models.graph import Graph
from algorithms.bfs import generate_bfs_steps
from ui.control_panel import ControlPanel
from ui.graph_canvas import GraphCanvas


class BFSVisualizerApp:
    """Aplicación principal para visualización de BFS."""
    
    def __init__(self, root):
        """
        Inicializa la aplicación.
        
        Args:
            root: Ventana principal de tkinter
        """
        self.root = root
        self.root.title("Visualizador de BFS - Algoritmo de Búsqueda en Anchura")
        self.root.geometry("1200x850")
        self.root.minsize(900, 700)
        self.root.configure(bg=UI_COLORS['bg_main'])
        
        # Modelo del grafo
        self.graph = Graph()
        
        # Estados de la aplicación
        self.mode = 'idle'  # 'idle', 'add_node', 'add_edge', 'delete', 'select_start', 'running'
        self.edge_first_node = None
        self.bfs_running = False
        self.bfs_paused = False
        self.animation_speed = 500  # ms
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Configura la interfaz de usuario."""
        # PanedWindow para paneles redimensionables
        self.paned = tk.PanedWindow(
            self.root,
            orient=tk.HORIZONTAL,
            bg=UI_COLORS['bg_separator'],
            sashwidth=8,
            sashrelief=tk.RAISED
        )
        self.paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Callbacks para el panel de control
        callbacks = {
            'set_mode': self._set_mode,
            'clear_all': self._clear_all,
            'start_bfs': self._start_bfs_mode,
            'reset_colors': self._reset_colors,
            'toggle_pause': self._toggle_pause,
            'update_speed': self._update_speed_from_entry
        }
        
        # Panel de control
        self.control_panel = ControlPanel(self.paned, callbacks)
        
        # Canvas del grafo
        self.graph_canvas = GraphCanvas(self.paned)
        self.graph_canvas.bind_click(self._on_canvas_click)
        
        # Agregar paneles al PanedWindow
        self.paned.add(self.control_panel.frame, minsize=250, width=450)
        self.paned.add(self.graph_canvas.frame, minsize=300)
    
    def _set_mode(self, mode):
        """Establece el modo actual de la aplicación."""
        if self.bfs_running:
            return
        
        # Resetear estados de edición
        self.edge_first_node = None
        
        # Resetear botones
        self.control_panel.reset_buttons()
        
        if self.mode == mode:
            # Si ya estaba en ese modo, desactivar
            self.mode = 'idle'
            self.control_panel.update_status(
                "Estado: Selecciona una acción", 
                UI_COLORS['text_muted']
            )
            self.control_panel.update_instruction(
                "Usa los botones de arriba\npara crear tu grafo"
            )
        else:
            self.mode = mode
            self.control_panel.set_button_active(mode)
            
            if mode == 'add_node':
                self.control_panel.update_status(
                    "Modo: AGREGAR NODO", 
                    UI_COLORS['btn_success']
                )
                self.control_panel.update_instruction(
                    "Click en el canvas para\ncolocar un nuevo nodo"
                )
            elif mode == 'add_edge':
                self.control_panel.update_status(
                    "Modo: AGREGAR ARISTA", 
                    UI_COLORS['btn_info']
                )
                self.control_panel.update_instruction(
                    "Click en el primer nodo,\nluego click en el segundo"
                )
            elif mode == 'delete':
                self.control_panel.update_status(
                    "Modo: ELIMINAR", 
                    UI_COLORS['btn_danger']
                )
                self.control_panel.update_instruction(
                    "Click en un nodo o cerca\nde una arista para eliminar"
                )
    
    def _update_speed_from_entry(self, event=None):
        """Actualiza la velocidad desde el campo de texto."""
        try:
            value = int(self.control_panel.get_speed_value())
            if value < 50:
                value = 50
            elif value > 5000:
                value = 5000
            self.animation_speed = value
            self.control_panel.set_speed_value(value)
        except ValueError:
            self.control_panel.set_speed_value(self.animation_speed)
    
    def _toggle_pause(self):
        """Alterna entre pausar y reanudar el BFS."""
        if not self.bfs_running:
            return
        
        self.bfs_paused = not self.bfs_paused
        if self.bfs_paused:
            self.control_panel.set_pause_button(True, "Reanudar", is_paused=True)
            self.control_panel.update_status(
                "Estado: BFS PAUSADO", 
                UI_COLORS['btn_warning']
            )
        else:
            self.control_panel.set_pause_button(True, "Pausar", is_paused=False)
            self.control_panel.update_status(
                "Estado: EJECUTANDO BFS...", 
                UI_COLORS['btn_danger']
            )
    
    def _on_canvas_click(self, event):
        """Maneja todos los clicks en el canvas según el modo actual."""
        x, y = event.x, event.y
        node = self.graph_canvas.get_node_at(x, y, self.graph.nodes)
        
        if self.mode == 'idle':
            pass
        
        elif self.mode == 'add_node':
            self._create_node(x, y)
        
        elif self.mode == 'add_edge':
            self._handle_add_edge_click(node)
        
        elif self.mode == 'delete':
            self._handle_delete_click(x, y, node)
        
        elif self.mode == 'select_start':
            if node is not None:
                self._run_bfs(node)
    
    def _create_node(self, x, y):
        """Crea un nuevo nodo en la posición dada."""
        if self.graph_canvas.get_node_at(x, y, self.graph.nodes) is not None:
            return
        
        label = self.graph.next_label
        circle_id, text_id = self.graph_canvas.create_node(x, y, label)
        self.graph.add_node(x, y, circle_id, text_id)
    
    def _handle_add_edge_click(self, node):
        """Maneja el click para agregar aristas."""
        if node is None:
            return
        
        if self.edge_first_node is None:
            # Primer nodo seleccionado
            self.edge_first_node = node
            label = self.graph.get_node(node)['label']
            self.control_panel.update_instruction(
                f"Nodo {label} seleccionado.\nClick en el segundo nodo"
            )
            # Resaltar nodo seleccionado
            circle_id = self.graph.get_node(node)['circle_id']
            self.graph_canvas.set_node_outline(circle_id, UI_COLORS['btn_active'], 4)
        else:
            # Segundo nodo seleccionado
            first_node = self.graph.get_node(self.edge_first_node)
            second_node = self.graph.get_node(node)
            
            x1, y1 = first_node['x'], first_node['y']
            x2, y2 = second_node['x'], second_node['y']
            
            line_id = self.graph_canvas.create_edge(x1, y1, x2, y2)
            
            if self.graph.add_edge(self.edge_first_node, node, line_id):
                label1 = first_node['label']
                label2 = second_node['label']
                self.control_panel.update_instruction(
                    f"Arista {label1}-{label2} creada.\nClick para más aristas"
                )
            else:
                # La arista ya existía, eliminar la línea creada
                self.graph_canvas.delete_item(line_id)
            
            # Restaurar outline del primer nodo
            self.graph_canvas.set_node_outline(
                first_node['circle_id'], 
                '#333333', 
                2
            )
            self.edge_first_node = None
    
    def _handle_delete_click(self, x, y, node):
        """Maneja el click para eliminar elementos."""
        if node is not None:
            node_data = self.graph.get_node(node)
            label = node_data['label']
            
            # Eliminar del canvas
            self.graph_canvas.delete_item(node_data['circle_id'])
            self.graph_canvas.delete_item(node_data['text_id'])
            
            # Eliminar del grafo
            removed_line_ids = self.graph.remove_node(node)
            for line_id in removed_line_ids:
                self.graph_canvas.delete_item(line_id)
            
            self.control_panel.update_instruction(f"Nodo {label} eliminado.")
        else:
            edge_idx = self.graph_canvas.get_edge_at(
                x, y, 
                self.graph.edges, 
                self.graph.nodes
            )
            if edge_idx is not None:
                n1_data = self.graph.get_node(self.graph.edges[edge_idx][0])
                n2_data = self.graph.get_node(self.graph.edges[edge_idx][1])
                label1 = n1_data['label']
                label2 = n2_data['label']
                
                n1, n2, line_id = self.graph.remove_edge(edge_idx)
                self.graph_canvas.delete_item(line_id)
                
                self.control_panel.update_instruction(
                    f"Arista {label1}-{label2} eliminada."
                )
    
    def _start_bfs_mode(self):
        """Inicia el modo de selección de nodo inicial."""
        if not self.graph.has_nodes():
            messagebox.showwarning(
                "Sin nodos", 
                "Primero crea algunos nodos en el grafo."
            )
            return
        
        if self.bfs_running:
            return
        
        self._set_mode('idle')
        self.mode = 'select_start'
        self.control_panel.update_status(
            "Estado: SELECCIONA NODO INICIAL", 
            UI_COLORS['status_warning']
        )
        self.control_panel.update_instruction(
            "Click en el nodo donde\nquieres iniciar el BFS"
        )
        self.control_panel.set_start_button_state(False)
    
    def _set_node_color(self, node_id, color):
        """Cambia el color de un nodo."""
        node = self.graph.get_node(node_id)
        if node:
            self.graph_canvas.set_node_color(
                node['circle_id'], 
                node['text_id'], 
                color
            )
    
    def _set_edge_color(self, node1, node2, color):
        """Cambia el color de una arista."""
        for n1, n2, line_id in self.graph.edges:
            if (n1 == node1 and n2 == node2) or (n1 == node2 and n2 == node1):
                self.graph_canvas.set_edge_color(line_id, color)
                break
    
    def _update_queue_display(self, queue):
        """Actualiza la visualización de la cola."""
        if queue:
            labels = [self.graph.get_node(n)['label'] for n in queue]
            self.control_panel.update_queue_display(labels)
        else:
            self.control_panel.update_queue_display([])
    
    def _run_bfs(self, start_node):
        """Ejecuta el algoritmo BFS con visualización."""
        self.bfs_running = True
        self.bfs_paused = False
        self.mode = 'running'
        
        self.control_panel.update_status(
            "Estado: EJECUTANDO BFS...", 
            UI_COLORS['status_danger']
        )
        self.control_panel.update_instruction(
            "Observa la animación\ndel recorrido BFS"
        )
        self.control_panel.set_pause_button(True, "Pausar")
        
        # Reiniciar colores
        for node_id in self.graph.nodes:
            self._set_node_color(node_id, COLORS['unvisited'])
        for _, _, line_id in self.graph.edges:
            self.graph_canvas.set_edge_color(line_id, COLORS['edge'])
        
        # Colorear nodo inicial
        self._set_node_color(start_node, COLORS['queued'])
        self._update_queue_display([start_node])
        
        # Generar pasos del BFS
        steps = generate_bfs_steps(self.graph, start_node)
        
        # Animar los pasos
        self._animate_steps(steps, 0)
    
    def _animate_steps(self, steps, index):
        """Anima un paso del BFS."""
        if index >= len(steps):
            self.bfs_running = False
            self.bfs_paused = False
            self.mode = 'idle'
            self.control_panel.update_status(
                "Estado: BFS COMPLETADO", 
                UI_COLORS['status_success']
            )
            self.control_panel.update_instruction(
                "Recorrido finalizado.\nUsa los botones para continuar"
            )
            self.control_panel.set_start_button_state(True)
            self.control_panel.set_pause_button(False, "Pausar")
            self.control_panel.update_queue_display([])
            return
        
        if self.bfs_paused:
            self.root.after(100, lambda: self._animate_steps(steps, index))
            return
        
        step = steps[index]
        
        if step[0] == 'visit':
            _, node, queue = step
            self._set_node_color(node, COLORS['current'])
            self._update_queue_display(queue)
        
        elif step[0] == 'enqueue':
            _, node, from_node, queue = step
            self._set_node_color(node, COLORS['queued'])
            self._set_edge_color(from_node, node, COLORS['edge_traversed'])
            self._update_queue_display(queue)
        
        elif step[0] == 'done':
            _, node, queue = step
            self._set_node_color(node, COLORS['visited'])
            self._update_queue_display(queue)
        
        self.root.after(
            self.animation_speed, 
            lambda: self._animate_steps(steps, index + 1)
        )
    
    def _reset_colors(self):
        """Reinicia los colores de todos los nodos y aristas."""
        if self.bfs_running:
            return
        
        for node_id in self.graph.nodes:
            self._set_node_color(node_id, COLORS['unvisited'])
        
        for _, _, line_id in self.graph.edges:
            self.graph_canvas.set_edge_color(line_id, COLORS['edge'])
        
        self.control_panel.update_queue_display([])
        self.mode = 'idle'
        self.control_panel.update_status(
            "Estado: Colores reiniciados", 
            UI_COLORS['status_success']
        )
        self.control_panel.update_instruction(
            "Usa los botones de arriba\npara crear tu grafo"
        )
        self.control_panel.set_start_button_state(True)
    
    def _clear_all(self):
        """Limpia todo el grafo."""
        if self.bfs_running:
            return
        
        self.graph_canvas.delete_all()
        self.graph.clear()
        self.edge_first_node = None
        
        self.control_panel.update_queue_display([])
        self._set_mode('idle')
        self.control_panel.update_status(
            "Estado: Grafo limpiado", 
            UI_COLORS['status_success']
        )
        self.control_panel.update_instruction(
            "Usa los botones de arriba\npara crear tu grafo"
        )
        self.control_panel.set_start_button_state(True)
