"""
Zero-overhead citation tracking for PICASO functions.

Functions are tagged with DOIs at *definition* time via the `@cite`
decorator below. The decorator only attaches metadata to the function
object and records it in a module-level registry -- it never wraps the
function, so calling a cited function costs exactly what calling the
undecorated function would cost (no added runtime overhead).

To find out which citations apply to a given run, callers do not need to
execute anything: `driver.references(driver_file)` statically reads the
driver TOML config (the same config `driver.run` consumes) to determine
which pt_/chem_/cloud_ parameterization functions would be selected, then
looks up any DOIs registered against those function names.

To cite a new function anywhere in the codebase, decorate it:

    from .citations import cite

    @cite('10.1051/0004-6361/200913396')
    def pt_guillot(self, ...):
        ...

A function may carry more than one DOI (e.g. the framework it implements
plus the paper defining its exact equations):

    @cite('10.1093/mnras/stx1246', '10.1093/mnras/stad670')
    def cloud_brewster_mie(self, ...):
        ...
"""

CITATIONS = {}


def cite(*dois):
    """
    Decorator that tags a function with one or more DOI references.

    Attaches metadata only (as a `.dois` attribute) and registers the
    function's name in the module-level CITATIONS registry -- it does
    not wrap or call the function, so there is no runtime cost to citing
    a function.

    Parameters
    ----------
    *dois : str
        One or more DOI strings, e.g. '10.1051/0004-6361/200913396'
    """
    def decorator(func):
        func.dois = dois
        CITATIONS[func.__name__] = dois
        return func
    return decorator


def get_citations(func_name):
    """
    Look up the DOIs registered for a function name (empty tuple if none).
    """
    return CITATIONS.get(func_name, ())


def all_citations():
    """
    Return the full citation registry as {function_name: (doi, ...)}.
    """
    return dict(CITATIONS)
