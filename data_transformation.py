import main as c_ui
from fractions import Fraction
import cmath
from c_calc import Calc_block as c_calc
import data_transformation as d_t


def data_formatting(data):
    data_type, left_value, oper, right_value = data

    if data_type == '1':

        left_value = complex(left_value)

        right_value = complex(right_value)

    elif data_type == '2':

        a = left_value
        # left_value = int(left_value)
        left_value = Fraction(int(a[0: a.index('/')]), int(a[a.index('/')+1:len(a)]))

        g = right_value
        # right_value = int(right_value)
        right_value = Fraction(int(g[0: g.index('/')]), int(g[g.index('/')+1:len(g)]))

    return (left_value, oper, right_value)
