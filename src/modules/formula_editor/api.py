"""
Formula Editor API
公式编辑器API接口

This module provides the API interface for formula editing functionality.
此模块提供公式编辑功能的API接口。
"""

from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field
from enum import Enum

class FormulaType(Enum):
    """Formula type enumeration."""
    ARITHMETIC = "算术"
    LOGICAL = "逻辑"
    COMPARISON = "比较"
    FUNCTION = "函数"
    CUSTOM = "自定义"

@dataclass
class Variable:
    """Variable data class."""
    name: str
    type: str
    description: str = ""
    default_value: Any = None

@dataclass
class Function:
    """Function data class."""
    name: str
    description: str
    parameters: List[Variable]
    return_type: str
    example: str = ""

@dataclass
class Formula:
    """Formula data class."""
    content: str
    type: FormulaType
    variables: List[Variable] = field(default_factory=list)
    description: str = ""
    is_valid: bool = False
    error_message: str = ""

class FormulaEditorAPI:
    """Formula editor API interface class."""
    
    def __init__(self):
        self.current_formula: Optional[Formula] = None
        self.formula_changed_callbacks = []
        self._load_builtin_functions()
    
    def create_formula(self, content: str, formula_type: FormulaType) -> Formula:
        """Create a new formula."""
        formula = Formula(content=content, type=formula_type)
        self.current_formula = formula
        self._notify_formula_changed()
        return formula
    
    def validate_formula(self, formula: Formula) -> bool:
        """Validate formula syntax and semantics."""
        try:
            # TODO: 实现公式验证逻辑
            formula.is_valid = True
            formula.error_message = ""
            return True
        except Exception as e:
            formula.is_valid = False
            formula.error_message = str(e)
            return False
    
    def get_variables(self, formula: Formula) -> List[Variable]:
        """Get variables used in the formula."""
        # TODO: 实现变量提取逻辑
        return formula.variables
    
    def get_functions(self) -> List[Function]:
        """Get available functions."""
        return list(self.functions.values())
    
    def get_function(self, name: str) -> Optional[Function]:
        """Get function by name."""
        return self.functions.get(name)
    
    def register_formula_changed_callback(self, callback):
        """Register a callback for formula changes."""
        self.formula_changed_callbacks.append(callback)
    
    def _notify_formula_changed(self):
        """Notify all registered callbacks about formula changes."""
        for callback in self.formula_changed_callbacks:
            callback()
    
    def _load_builtin_functions(self):
        """Load built-in functions."""
        self.functions = {
            # 数学函数
            "sum": Function(
                name="sum",
                description="计算一组数值的总和",
                parameters=[
                    Variable("values", "List[float]", "要计算的数值列表")
                ],
                return_type="float",
                example="sum([1, 2, 3]) -> 6"
            ),
            "avg": Function(
                name="avg",
                description="计算一组数值的平均值",
                parameters=[
                    Variable("values", "List[float]", "要计算的数值列表")
                ],
                return_type="float",
                example="avg([1, 2, 3]) -> 2"
            ),
            "min": Function(
                name="min",
                description="获取一组数值中的最小值",
                parameters=[
                    Variable("values", "List[float]", "要比较的数值列表")
                ],
                return_type="float",
                example="min([1, 2, 3]) -> 1"
            ),
            "max": Function(
                name="max",
                description="获取一组数值中的最大值",
                parameters=[
                    Variable("values", "List[float]", "要比较的数值列表")
                ],
                return_type="float",
                example="max([1, 2, 3]) -> 3"
            ),
            
            # 逻辑函数
            "if": Function(
                name="if",
                description="根据条件返回不同的值",
                parameters=[
                    Variable("condition", "bool", "条件表达式"),
                    Variable("true_value", "Any", "条件为真时的值"),
                    Variable("false_value", "Any", "条件为假时的值")
                ],
                return_type="Any",
                example="if(x > 0, 'positive', 'negative')"
            ),
            "and": Function(
                name="and",
                description="逻辑与运算",
                parameters=[
                    Variable("conditions", "List[bool]", "条件列表")
                ],
                return_type="bool",
                example="and([true, false]) -> false"
            ),
            "or": Function(
                name="or",
                description="逻辑或运算",
                parameters=[
                    Variable("conditions", "List[bool]", "条件列表")
                ],
                return_type="bool",
                example="or([true, false]) -> true"
            ),
            
            # 字符串函数
            "concat": Function(
                name="concat",
                description="连接字符串",
                parameters=[
                    Variable("strings", "List[str]", "要连接的字符串列表"),
                    Variable("separator", "str", "分隔符", "")
                ],
                return_type="str",
                example="concat(['a', 'b'], '-') -> 'a-b'"
            ),
            "length": Function(
                name="length",
                description="获取字符串长度",
                parameters=[
                    Variable("text", "str", "要计算长度的字符串")
                ],
                return_type="int",
                example="length('abc') -> 3"
            )
        } 