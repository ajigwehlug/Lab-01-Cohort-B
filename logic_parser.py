import re

class LogicParser:
    def __init__(self, expression):
        self.expression = expression
        self.pos = 0
        self.current_token = None

    def parse(self):
        self.next_token()  # Initialize the first token
        return self.expr()

    def expr(self):
        left = self.term()
        while self.current_token is not None and self.current_token['type'] == 'OR':
            operator = self.current_token
            self.next_token()  # Move to next token
            right = self.term()
            left = {'type': 'OR', 'left': left, 'right': right}
        return left

    def term(self):
        left = self.factor()
        while self.current_token is not None and self.current_token['type'] == 'AND':
            operator = self.current_token
            self.next_token()  # Move to next token
            right = self.factor()
            left = {'type': 'AND', 'left': left, 'right': right}
        return left

    def factor(self):
        if self.current_token is not None and self.current_token['type'] == 'NOT':
            self.next_token()  # Move to next token
            return {'type': 'NOT', 'right': self.factor()}
        elif self.current_token is not None and self.current_token['type'] == 'LPAREN':
            self.next_token()  # Move to next token
            node = self.expr()
            if self.current_token is None or self.current_token['type'] != 'RPAREN':
                raise Exception("Missing closing parenthesis")
            self.next_token()  # Move past ')'
            return node
        elif self.current_token is not None and self.current_token['type'] == 'IDENTIFIER':
            node = {'type': 'IDENTIFIER', 'value': self.current_token['value']}
            self.next_token()  # Move to next token
            return node
        else:
            raise Exception("Invalid factor")

    def next_token(self):
        while self.pos < len(self.expression) and self.expression[self.pos] == ' ':
            self.pos += 1
        if self.pos >= len(self.expression):
            self.current_token = None
            return
        m = re.match(r'\(|\)', self.expression[self.pos:])
        if m:
            self.current_token = {'type': 'LPAREN' if m.group() == '(' else 'RPAREN'}
            self.pos += len(m.group())
            return
        m = re.match(r'AND|OR|NOT', self.expression[self.pos:])
        if m:
            self.current_token = {'type': m.group()}
            self.pos += len(m.group())
            return
        m = re.match(r'[a-zA-Z_][a-zA-Z0-9_]*', self.expression[self.pos:])
        if m:
            self.current_token = {'type': 'IDENTIFIER', 'value': m.group()}
            self.pos += len(m.group())
            return
        raise Exception("Invalid character")