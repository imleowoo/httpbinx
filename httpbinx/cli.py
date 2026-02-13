"""httpbinx CLI."""

import argparse
import platform
import sys

import fastapi

import httpbinx


def info(_args):
    """Show httpbinx and environment information."""
    print(f"httpbinx: {httpbinx.__version__}")
    print(f"fastapi: {fastapi.__version__}")
    print(f"python: {sys.version}")
    print(f"platform: {platform.platform()}")
    print(f"python executable: {sys.executable}")


def version(_args):
    """Show httpbinx version."""
    print(httpbinx.__version__)


def server(_args):
    """Start the httpbinx server."""
    import uvicorn
    uvicorn.run(
        'httpbinx.main:app',
        host=_args.host,
        port=_args.port
    )


def execute():
    """Execute the CLI."""
    parser = argparse.ArgumentParser(
        prog='httpbinx',
        description='httpbinx is a fastapi server for testing.'
    )
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    subparsers = parser.add_subparsers(dest='command')
    # version
    parser_version = subparsers.add_parser('version', help='show version')
    parser_version.set_defaults(func=version)
    # info
    parser_info = subparsers.add_parser('info', help='show info')
    parser_info.set_defaults(func=info)
    # server
    parser_server = subparsers.add_parser('server', help='start server')
    parser_server.set_defaults(func=server)
    parser_server.add_argument(
        '--host',
        type=str,
        help='host',
        default='0.0.0.0'
    )
    parser_server.add_argument(
        '--port',
        type=int,
        help='port',
        default=80
    )

    parse_args = parser.parse_args()
    if hasattr(parse_args, 'func'):
        parse_args.func(parse_args)
    else:
        parser.print_help()


if __name__ == '__main__':
    execute()
