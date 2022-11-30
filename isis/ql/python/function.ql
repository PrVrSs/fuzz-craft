import python

from FunctionExpr function_expr, string func_name, Arguments argument, Expr annotation, int argument_idx
where
    func_name = function_expr.getName() and
    argument = function_expr.getArgs() and
    annotation = argument.getAnnotation(argument_idx)
select func_name, annotation, argument_idx
