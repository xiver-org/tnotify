import inspect
import traceback

__all__ = ('ExceptionsParser',)

class ExceptionsParser:
    def __init__(self):  # noqa: ANN204
        pass

    def parse(self, exception: BaseException) -> dict:
        exception_info = {
            "type": type(exception).__name__,
            "message": str(exception),
            "full_traceback": "".join(traceback.format_exception(type(exception), exception, exception.__traceback__)),
            "traceback": [],
            "attributes": {}
        }
        
        tb = exception.__traceback__
        while tb is not None:
            frame = tb.tb_frame
            lineno = tb.tb_lineno
            code_context = traceback.extract_tb(tb)[-1]
            
            local_vars = {var: repr(val) for var, val in frame.f_locals.items()}
            
            exception_info["traceback"].append({
                "filename": frame.f_code.co_filename,
                "function_name": frame.f_code.co_name,
                "line_number": lineno,
                "line_code": code_context.line,
                "local_variables": local_vars
            })
            tb = tb.tb_next
        
        for attr_name, attr_value in vars(exception).items():
            exception_info["attributes"][attr_name] = attr_value
        
        if hasattr(exception, "args"):
            exception_info["args"] = exception.args
        
        exception_info["inspection"] = {
            "is_user_defined": inspect.isclass(type(exception)) and type(exception).__module__ != "builtins",
            "module": type(exception).__module__,
        }
        
        return exception_info
