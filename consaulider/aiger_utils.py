from functools import reduce

# Let us first define
# nice helpers for building circuits
all_ = lambda l: reduce(lambda u, v: u & v, l)
any_ = lambda l: reduce(lambda u, v: u | v, l)
