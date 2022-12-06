import cpp

from Function function, Type argument_type, int argument_idx
where
    argument_type = function.getParameter(argument_idx).getType()
select function, argument_type, argument_idx
