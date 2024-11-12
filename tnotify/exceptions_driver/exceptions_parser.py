import traceback
import inspect


__all__ = ('ExceptionsParser',)

class ExceptionsParser:
    def __init__(self):
        pass
    
    def parse(self, exception):
        exception_info = {
            "type": type(exception).__name__,
            "message": str(exception),
            "full_traceback": "".join(traceback.format_exception(type(exception), exception, exception.__traceback__)),
            "traceback": [],
            "attributes": {}
        }
        
        # Extract traceback details along with local variables
        tb = exception.__traceback__
        while tb is not None:
            frame = tb.tb_frame
            lineno = tb.tb_lineno
            code_context = traceback.extract_tb(tb)[-1]
            
            # Get local variables in the frame at the moment of exception
            local_vars = {var: repr(val) for var, val in frame.f_locals.items()}
            
            exception_info["traceback"].append({
                "filename": frame.f_code.co_filename,
                "function_name": frame.f_code.co_name,
                "line_number": lineno,
                "line_code": code_context.line,
                "local_variables": local_vars
            })
            tb = tb.tb_next
        
        # Extract custom attributes
        for attr_name, attr_value in vars(exception).items():
            exception_info["attributes"][attr_name] = attr_value
        
        # Extract arguments passed to the exception (if any)
        if hasattr(exception, "args"):
            exception_info["args"] = exception.args
        
        # Add inspection data if available
        exception_info["inspection"] = {
            "is_user_defined": inspect.isclass(type(exception)) and type(exception).__module__ != "builtins",
            "module": type(exception).__module__,
        }
        
        return exception_info
