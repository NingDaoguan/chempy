# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function)
import re


# See https://github.com/python-quantities/python-quantities/pull/112
def format_units_html(udict, font='%s', mult=r'&sdot;', paren=False):
    '''
    Replace the units string provided with an equivalent html string.

    Exponentiation (m**2) will be replaced with superscripts (m<sup>2</sup>})

    No formating is done, change `font` argument to e.g.:
    '<span style="color: #0000a0">%s</span>' to have text be colored blue.

    Multiplication (*) are replaced with the symbol specified by the mult
    argument. By default this is the latex &sdot; symbol.  Other useful options
    may be '' or '*'.

    If paren=True, encapsulate the string in '(' and ')'

    '''
    from quantities.markup import format_units
    res = format_units(udict)
    if res.startswith('(') and res.endswith(')'):
        # Compound Unit
        compound = True
    else:
        # Not a compound unit
        compound = False
    # Replace exponentiation (**exp) with ^{exp}
    res = re.sub(r'\*{2,2}(?P<exp>\d+)', r'<sup>\g<exp></sup>', res)
    # Remove multiplication signs
    res = re.sub(r'\*', mult, res)
    if paren and not compound:
        res = '(%s)' % res
    res = font % res
    return res


def _patch_quantities(pq):
    pq.dimensionality.Dimensionality.html = property(lambda self: format_units_html(self))
