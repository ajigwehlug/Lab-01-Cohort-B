"""
Logic Circuit Simulator
A tool to convert propositional logic expressions into visual circuit diagrams

Authors: [Your Team Names]
Date: 2025-11-15
"""

from logic_parser import LogicParser
from circuit_generator import CircuitGenerator
from circuit_visualizer import CircuitVisualizer, visualize_truth_table
import matplotlib.pyplot as plt

def print_banner():
    """Print welcome banner"""
    print("\n" + "="*60)
    print("        LOGIC CIRCUIT SIMULATOR")
    print("="*60)
    print("Convert propositional logic to visual circuits!")
    print("\nSupported operators:")
    print("  - AND: logical conjunction")
    print("  - OR: logical disjunction")
    print("  - NOT: logical negation")
    print("  - Use parentheses () for grouping")
    print("\nExample: (A AND B) OR (NOT C)")
    print("="*60 + "\n")

def get_user_input():
    """Get logic expression from user"""
    while True:
        try:
            expression = input("Enter your logic expression (or 'quit' to exit): ").strip()
            
            if expression.lower() == 'quit':
                return None
            
            if not expression:
                print("Error: Expression cannot be empty. Please try again.\n")
                continue
            
            # Basic validation
            if not any(op in expression for op in ['AND', 'OR', 'NOT']) and '(' not in expression:
                print("Warning: No operators found. Please use AND, OR, or NOT.\n")
                continue
            
            return expression
        except KeyboardInterrupt:
            return None

def test_circuit_interactively(circuit):
    """Allow user to test circuit with custom inputs"""
    print("\n" + "-"*60)
    print("INTERACTIVE TESTING MODE")
    print("-"*60)
    
    inputs = circuit['inputs']
    output_gate = circuit['output_gate']
    
    print(f"Input variables: {', '.join(inputs)}")
    print("\nEnter values for each variable (1 for True, 0 for False)")
    print("Press Enter without input to skip testing.\n")
    
    while True:
        try:
            variable_values = {}
            skip = False
            
            for var in inputs:
                while True:
                    value = input(f"  {var} = ").strip()
                    
                    if value == '':
                        skip = True
                        break
                    
                    if value in ['0', '1']:
                        variable_values[var] = (value == '1')
                        break
                    else:
                        print("    Invalid input. Use 0 or 1.")
            
            if skip:
                break
            
            # Evaluate circuit
            result = output_gate.evaluate(variable_values)
            
            print("\n  Results:")
            for var, val in variable_values.items():
                print(f"    {var} = {int(val)}")
            print(f"    Output = {int(result)}")
            print()            
            another = input("Test another combination? (y/n): ").strip().lower()
            if another != 'y':
                break
            print()                
        except KeyboardInterrupt:
            break
    
    print("-"*60 + "\n")

def handle_edge_cases(expression):
    """Demonstrate error handling for edge cases"""
    edge_cases = {
        'empty': '',
        'invalid_operator': 'A XOR B',
        'unbalanced_parens': '(A AND B',
        'missing_operand': 'AND B',
        'invalid_chars': 'A & B'
    }
    
    print("\n" + "="*60)
    print("EDGE CASE DEMONSTRATION")
    print("="*60)
    
    test_cases = [
        ('', 'Empty expression'),
        ('A XOR B', 'Invalid operator (XOR not supported)'),
        ('(A AND B', 'Unbalanced parentheses'),
        ('AND B', 'Missing operand'),
        ('A & B', 'Invalid characters')
    ]
    
    for test_expr, description in test_cases:
        print(f"\nTest: {description}")
        print(f"Expression: '{test_expr}'")
        try:
            if test_expr == '':
                print("✗ Result: Empty expression - validation failed")
            else:
                parser = LogicParser(test_expr)
                tree = parser.parse()
                print("✗ Unexpected: Expression parsed successfully")
        except Exception as e:
            print(f"✓ Result: Caught error - {str(e)}")
    
    print("\n" + "="*60 + "\n")

def main():
    """Main application loop"""
    print_banner()
    
    # Show edge case handling
    show_edges = input("Would you like to see edge case handling demo? (y/n): ").strip().lower()
    if show_edges == 'y':
        handle_edge_cases(None)
    
    while True:
        # Get user input
        expression = get_user_input()
        
        if expression is None:
            print("\nThank you for using Logic Circuit Simulator!")
            break
        
        try:
            print(f"\nProcessing: {expression}")
            print("-" * 60)
            
            # Step 1: Parse the expression
            print("Step 1: Parsing expression...")
            parser = LogicParser(expression)
            parse_tree = parser.parse()
            print("✓ Parsing successful!")
            
            # Step 2: Generate circuit
            print("\nStep 2: Generating circuit...")
            generator = CircuitGenerator(parse_tree)
            circuit = generator.generate()
            print(f"✓ Circuit generated with {len(circuit['gates'])} gates")
            print(f"  Input variables: {', '.join(circuit['inputs'])}")
            
            # Step 3: Generate truth table
            print("\nStep 3: Generating truth table...")
            truth_table = generator.generate_truth_table(circuit)
            visualize_truth_table(truth_table, circuit['inputs'])
            
            # Step 4: Visualize circuit
            print("Step 4: Creating circuit diagram...")
            visualizer = CircuitVisualizer(circuit)
            fig = visualizer.visualize()
            
            # Save the diagram
            filename = f"circuit_{expression.replace(' ', '_')[:30]}.png"
            visualizer.save(filename)
            
            # Step 5: Interactive testing
            test = input("\nWould you like to test the circuit interactively? (y/n): ").strip().lower()
            if test == 'y':
                test_circuit_interactively(circuit)
            
            # Display the diagram
            print("Displaying circuit diagram...")
            visualizer.show()
            
            print("\n✓ Process complete!")
            print("-" * 60)
            
            # Ask if user wants to continue
            another = input("\nWould you like to create another circuit? (y/n): ").strip().lower()
            if another != 'y':
                print("\nThank you for using Logic Circuit Simulator!")
                break
            print("\n")
            
        except Exception as e:
            print(f"\n✗ Error: {str(e)}")
            print("Please check your expression and try again.\n")

if __name__ == "__main__":
    main()