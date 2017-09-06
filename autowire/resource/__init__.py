"""
autowire.resource
=================

Resource implementations.

"""
from autowire import impl
from autowire.base import BaseResource, Implementation

from .plain import Resource
from .function import FunctionResource


def create(implementation: Implementation=None, *, name=None, namespace=None):
    """
    Create a resource with implementation. ::

        @resource.create
        @contextlib.contextmanager
        def some_resource(context: Context):
            with open('output.log', 'w') as output:
                yield output

        with context.resolve(some_resource) as f:
            f.write('...')

    The default name and namespace will be resolved from decorated function.

    """
    def decorator(implementation):
        resource = FunctionResource(
            implementation, name=name, namespace=namespace
        )
        impl.implement(resource)(implementation)
        return resource
    if impl is not None:
        return decorator(implementation)
    return decorator


__all__ = [
    'Resource',
    'FunctionResource',
    'create',
]
