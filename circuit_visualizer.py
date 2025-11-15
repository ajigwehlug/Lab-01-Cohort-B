import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch
import numpy as np

class CircuitVisualizer:
    """Visualizes logic circuits using matplotlib"""
    
    def __init__(self, circuit):
        self.circuit = circuit
        self.gate_positions = {}
        self.fig, self.ax = plt.subplots(figsize=(14, 8))
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(0, 8)
        self.ax.axis('off')
        
    def visualize(self):
        """Main method to visualize the circuit"""
        output_gate = self.circuit['output_gate']
        inputs = self.circuit['inputs']
        
        # Position gates using a layered approach
        self._position_gates(output_gate, 8, 4, inputs)
        
        # Draw all gates and connections
        self._draw_circuit(output_gate, inputs)
        
        plt.title("Logic Circuit Diagram", fontsize=16, fontweight='bold')
        plt.tight_layout()
        return self.fig
    
    def _position_gates(self, gate, x, y, inputs, level=0):
        """Recursively position gates in the circuit"""
        if gate.gate_id in self.gate_positions:
            return self.gate_positions[gate.gate_id]
        
        if gate.gate_type == 'INPUT':
            # Position input gates on the left
            input_index = inputs.index(gate.inputs[0])
            pos = (1, 6 - input_index * 1.5)
            self.gate_positions[gate.gate_id] = pos
            return pos
        
        # Position child gates first
        if gate.gate_type == 'NOT':
            child_pos = self._position_gates(gate.inputs[0], x - 2, y, inputs, level + 1)
            pos = (child_pos[0] + 2, child_pos[1])
        else:  # AND or OR
            left_pos = self._position_gates(gate.inputs[0], x - 2, y + 1, inputs, level + 1)
            right_pos = self._position_gates(gate.inputs[1], x - 2, y - 1, inputs, level + 1)
            avg_y = (left_pos[1] + right_pos[1]) / 2
            pos = (max(left_pos[0], right_pos[0]) + 2, avg_y)
        
        self.gate_positions[gate.gate_id] = pos
        return pos
    
    def _draw_circuit(self, gate, inputs):
        """Draw the complete circuit"""
        drawn_gates = set()
        self._draw_gate_recursive(gate, inputs, drawn_gates)
    
    def _draw_gate_recursive(self, gate, inputs, drawn_gates):
        """Recursively draw gates and their connections"""
        if gate.gate_id in drawn_gates:
            return
        
        # Draw child gates first
        if gate.gate_type != 'INPUT':
            for input_gate in gate.inputs:
                self._draw_gate_recursive(input_gate, inputs, drawn_gates)
        
        # Draw this gate
        pos = self.gate_positions[gate.gate_id]
        
        if gate.gate_type == 'INPUT':
            self._draw_input(pos, gate.inputs[0])
        elif gate.gate_type == 'NOT':
            self._draw_not_gate(pos)
            self._draw_connection(self.gate_positions[gate.inputs[0].gate_id], pos)
        elif gate.gate_type == 'AND':
            self._draw_and_gate(pos)
            self._draw_connection(self.gate_positions[gate.inputs[0].gate_id], pos, 'left')
            self._draw_connection(self.gate_positions[gate.inputs[1].gate_id], pos, 'right')
        elif gate.gate_type == 'OR':
            self._draw_or_gate(pos)
            self._draw_connection(self.gate_positions[gate.inputs[0].gate_id], pos, 'left')
            self._draw_connection(self.gate_positions[gate.inputs[1].gate_id], pos, 'right')
        
        drawn_gates.add(gate.gate_id)
    
    def _draw_input(self, pos, label):
        """Draw an input node"""
        circle = Circle(pos, 0.15, facecolor='lightblue', edgecolor='black', linewidth=2)
        self.ax.add_patch(circle)
        self.ax.text(pos[0] - 0.5, pos[1], label, fontsize=12, fontweight='bold', 
                    ha='right', va='center')
    
    def _draw_and_gate(self, pos):
        """Draw an AND gate"""
        # Gate body (rectangle + semicircle)
        rect = FancyBboxPatch((pos[0] - 0.3, pos[1] - 0.25), 0.4, 0.5,
                              boxstyle="round,pad=0.05", facecolor='lightyellow',
                              edgecolor='black', linewidth=2)
        self.ax.add_patch(rect)
        self.ax.text(pos[0], pos[1], 'AND', fontsize=9, ha='center', va='center', fontweight='bold')
    
    def _draw_or_gate(self, pos):
        """Draw an OR gate"""
        rect = FancyBboxPatch((pos[0] - 0.3, pos[1] - 0.25), 0.4, 0.5,
                              boxstyle="round,pad=0.05", facecolor='lightgreen',
                              edgecolor='black', linewidth=2)
        self.ax.add_patch(rect)
        self.ax.text(pos[0], pos[1], 'OR', fontsize=9, ha='center', va='center', fontweight='bold')
    
    def _draw_not_gate(self, pos):
        """Draw a NOT gate"""
        # Triangle with circle
        triangle = patches.Polygon([(pos[0] - 0.3, pos[1] - 0.2),
                                   (pos[0] - 0.3, pos[1] + 0.2),
                                   (pos[0] + 0.1, pos[1])],
                                  facecolor='lightcoral', edgecolor='black', linewidth=2)
        self.ax.add_patch(triangle)
        circle = Circle((pos[0] + 0.15, pos[1]), 0.05, facecolor='white', 
                       edgecolor='black', linewidth=2)
        self.ax.add_patch(circle)
        self.ax.text(pos[0] - 0.1, pos[1], 'NOT', fontsize=8, ha='center', va='center', fontweight='bold')
    
    def _draw_connection(self, from_pos, to_pos, side='center'):
        """Draw a connection line between gates"""
        if side == 'left':
            to_x, to_y = to_pos[0] - 0.3, to_pos[1] + 0.15
        elif side == 'right':
            to_x, to_y = to_pos[0] - 0.3, to_pos[1] - 0.15
        else:
            to_x, to_y = to_pos[0] - 0.3, to_pos[1]
        
        from_x, from_y = from_pos[0] + 0.15, from_pos[1]
        
        arrow = FancyArrowPatch((from_x, from_y), (to_x, to_y),
                               arrowstyle='-', linewidth=1.5, color='black')
        self.ax.add_patch(arrow)
    
    def save(self, filename='circuit_diagram.png'):
        """Save the circuit diagram to a file"""
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"Circuit diagram saved as {filename}")
    
    def show(self):
        """Display the circuit diagram"""
        plt.show()


def visualize_truth_table(truth_table, inputs):
    """Visualize truth table as a formatted table"""
    print("\n" + "="*50)
    print("TRUTH TABLE")
    print("="*50)
    
    # Print header
    header = " | ".join(inputs) + " | Output"
    print(header)
    print("-" * len(header))
    
    # Print rows
    for row in truth_table:
        values = [str(int(row[var])) for var in inputs]
        output = str(int(row['Output']))
        print(" | ".join(values) + " |   " + output)
    
    print("="*50 + "\n")