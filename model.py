import re
import logging
from typing import List, Set
from abc import ABC, abstractmethod


class AbstractModel(ABC):
    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    def __repr__(self):
        raise NotImplementedError


class Query(AbstractModel):
    def __init__(self, expression: str):
        self.code: str = None
        self.expr_tokens: List[str] = []
        self._tokenise_query(expression)

    def _tokenise_query(self, expression: str):
        # Split off the course code label
        self.code, requirement = expression.split(': ')
        self.expr_tokens = re.findall(r'(\b[A-Z]{4}\d{4}\b|and|or|not|at least|greater than|less than|\d+UOC|\(|\))', requirement)
        logging.info(f"Tokens extracted for {self.code}: {self.expr_tokens}")
    
    def __repr__(self):
        return f"Query(code={self.code}, tokens={self.expr_tokens})"


class Student(AbstractModel):
    def __init__(self, courses: Set[str], UOC: int):
        self.completed_courses = courses
        self.UOC = UOC  # for simplicity, assume that all courses are worth 6 UOC

    def __repr__(self):
        return f"Student(completed_courses={self.completed_courses}, UOC={self.UOC})"


class Course(AbstractModel):
    def __init__(self, query: Query):
        self.code: str = query.code
        self.query = query
    
    def evaluate_requisites(self, student: Student) -> bool:
        eval_expression: List[str] = []
        for token in self.query.expr_tokens:
            eval_expression = self._expression_builder(token, eval_expression, student)
        
        to_eval: str = " ".join(eval_expression)
        logging.debug(f"Expression to evaluate: {to_eval}")
        result = eval(to_eval, {"__builtins__": None}, {})  # global = {"__builtins__": None} means no access to built-in functions, enhancing security, and local = {} means no access to local variables
        logging.info(f"Evaluation result: {result}")
        return result

    @staticmethod
    def _expression_builder(
        token: str, 
        eval_expression: List[str], 
        student: Student
    ) -> List[str]:
        if re.match(r'[A-Z]{4}\d{4}', token):
            is_completed = 'True' if token in student.completed_courses else 'False'
            eval_expression.append(is_completed)
        elif token.endswith('UOC'):
            # Remove 'UOC' and convert to integer
            uoc_needed = int(token[:-3])
            eval_expression.append(str(uoc_needed))
        elif token in ['at least', 'greater than', 'less than']:
            eval_expression.append(str(student.UOC))
            if token == 'at least':
                eval_expression.append('>=')
            elif token == 'greater than':
                eval_expression.append('>')
            elif token == 'less than':
                eval_expression.append('<')
        else:  # assume that the rest of the tokens are `(`, `)`, and operators
            eval_expression.append(token)
        return eval_expression

    def __repr__(self):
        return f"Course(code={self.code}, tokens={self.query})"
