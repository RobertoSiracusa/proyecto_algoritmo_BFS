#!/usr/bin/env python3
"""
BFS Graph Visualizer
Una aplicación interactiva para crear grafos y visualizar el algoritmo BFS.
"""

import tkinter as tk
from ui.app import BFSVisualizerApp


def main():
    """Punto de entrada principal de la aplicación."""
    root = tk.Tk()
    app = BFSVisualizerApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
