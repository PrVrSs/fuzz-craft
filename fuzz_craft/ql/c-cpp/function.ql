import cpp

from Function function, Type argument_type, string return_type, string location, int argument_idx
where
    argument_type = function.getParameter(argument_idx).getType() and
    return_type = function.getType().toString() and
    location = min(function.getADeclarationLocation().getContainer().toString())
select function, argument_type, return_type, location, argument_idx
