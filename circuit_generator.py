class Gate:
    """Represents a logic gate in the circuit"""
    def __init__(self, gate_type, inputs=None):
        self.gate_type = gate_type  # 'AND', 'OR', 'NOT', 'INPUT'
        self.inputs = inputs if inputs else []
        self.output = None
        self.gate_id = None
        
    def evaluate(self, variable_values):
        """Evaluate the gate output based on input values"""
        if self.gate_type == 'INPUT':
            # For input gates, return the variable value
            return variable_values.get(self.inputs[0], False)
        elif self.gate_type == 'NOT':
            return not self.inputs[0].evaluate(variable_values)
        elif self.gate_type == 'AND':
            left = self.inputs[0].evaluate(variable_values)
            right = self.inputs[1].evaluate(variable_values)
            return left and right
        elif self.gate_type == 'OR':
            left = self.inputs[0].evaluate(variable_values)
            right = self.inputs[1].evaluate(variable_values)
            return left or right
        return False
    
    def __repr__(self):
        return f"Gate({self.gate_type}, id={self.gate_id})"


class CircuitGenerator:
    """Converts parsed logic expressions into circuit representation"""
    def __init__(self, parse_tree):
        self.parse_tree = parse_tree
        self.gates = []
        self.input_variables = set()
        self.gate_counter = 0
        
    def generate(self):
        """Generate the circuit from the parse tree"""
        output_gate = self._build_circuit(self.parse_tree)
        return {
            'gates': self.gates,
            'output_gate': output_gate,
            'inputs': sorted(list(self.input_variables))
        }
    
    def _build_circuit(self, node):
        """Recursively build circuit from parse tree"""
        if node['type'] == 'IDENTIFIER':
            # Create an input gate
            var_name = node['value']
            self.input_variables.add(var_name)
            gate = Gate('INPUT', [var_name])
            gate.gate_id = self.gate_counter
            self.gate_counter += 1
            self.gates.append(gate)
            return gate
            
        elif node['type'] == 'NOT':
            # Create a NOT gate
            input_gate = self._build_circuit(node['right'])
            gate = Gate('NOT', [input_gate])
            gate.gate_id = self.gate_counter
            self.gate_counter += 1
            self.gates.append(gate)
            return gate
            
        elif node['type'] in ['AND', 'OR']:
            # Create AND or OR gate
            left_gate = self._build_circuit(node['left'])
            right_gate = self._build_circuit(node['right'])
            gate = Gate(node['type'], [left_gate, right_gate])
            gate.gate_id = self.gate_counter
            self.gate_counter += 1
            self.gates.append(gate)
            return gate
        
        return None
    
    def generate_truth_table(self, circuit):
        """Generate truth table for the circuit"""
        inputs = circuit['inputs']
        output_gate = circuit['output_gate']
        
        # Generate all possible input combinations
        num_inputs = len(inputs)
        truth_table = []
        
        for i in range(2 ** num_inputs):
            # Create binary representation
            binary = format(i, f'0{num_inputs}b')
            variable_values = {}
            for j, var in enumerate(inputs):
                variable_values[var] = binary[j] == '1'
            
            # Evaluate circuit
            output = output_gate.evaluate(variable_values)
            
            # Add to truth table
            row = {var: variable_values[var] for var in inputs}
            row['Output'] = output
            truth_table.append(row)
        
        return truth_table
