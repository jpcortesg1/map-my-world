"""Custom log formatters for Map My World API."""
from typing import Any, Dict, Optional
from datetime import datetime


def format_request_log(method: str, path: str, client_ip: str, user_agent: Optional[str] = None) -> str:
    """Format request log message."""
    log_parts = [f"Request: {method} {path} from {client_ip}"]
    if user_agent:
        log_parts.append(f"User-Agent: {user_agent}")
    return " | ".join(log_parts)


def format_response_log(status_code: int, response_time_ms: float) -> str:
    """Format response log message."""
    return f"Response: {status_code} in {response_time_ms:.2f}ms"


def format_error_log(error: Exception, context: Optional[Dict[str, Any]] = None) -> str:
    """Format error log message."""
    error_msg = f"Error: {type(error).__name__}: {str(error)}"
    if context:
        context_str = " | ".join([f"{k}={v}" for k, v in context.items()])
        error_msg += f" | Context: {context_str}"
    return error_msg


def format_performance_log(operation: str, duration_ms: float, details: Optional[Dict[str, Any]] = None) -> str:
    """Format performance log message."""
    perf_msg = f"Performance: {operation} took {duration_ms:.2f}ms"
    if details:
        details_str = " | ".join([f"{k}={v}" for k, v in details.items()])
        perf_msg += f" | Details: {details_str}"
    return perf_msg 