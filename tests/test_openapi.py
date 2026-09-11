"""OpenAPI schema tests."""


def test_multi_method_routes_have_unique_operation_ids(client):
    """Every documented operation for a multi-method endpoint has a unique ID."""
    schema = client.get('/openapi.json').json()
    paths = ['/anything', '/delay/{delay}', '/redirect-to']
    operation_ids = [
        operation['operationId']
        for path in paths
        for operation in schema['paths'][path].values()
        if isinstance(operation, dict) and 'operationId' in operation
    ]

    assert len(operation_ids) == len(set(operation_ids))


def test_multi_method_routes_do_not_document_trace(client):
    """TRACE is not part of httpbinx's public API."""
    schema = client.get('/openapi.json').json()
    paths = ['/anything', '/delay/{delay}', '/redirect-to']

    assert all('trace' not in schema['paths'][path] for path in paths)
