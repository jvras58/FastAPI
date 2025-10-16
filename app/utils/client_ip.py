"""Client IP utility functions."""
from fastapi import Request


def get_client_ip(request: Request) -> str:
    """Get client IP from request, checking multiple sources."""
    if request.client and request.client.host:
        return request.client.host

    # Check headers in order of preference
    forwarded_for = request.headers.get('x-forwarded-for')
    if forwarded_for:
        # X-Forwarded-For can contain multiple IPs, get the first one
        return forwarded_for.split(',')[0].strip()

    real_ip = request.headers.get('x-real-ip')
    if real_ip:
        return real_ip

    remote_addr = request.headers.get('remote-addr')
    if remote_addr:
        return remote_addr

    return '127.0.0.1'  # Fallback to localhost
