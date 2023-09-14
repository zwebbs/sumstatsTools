# File Name: stats.py
# Created By: ZW
# Created On: 2023-09-14
# Purpose:  defines types and transformations for basic statistics 
#   computed for GWAS summary stats. 


# library imports
# -----------------------------------------------------------------------------

from dataclasses import dataclass, field
from math import inf, copysign, erf, sqrt, log10
from typing import Tuple, Union

# type definitions
# -----------------------------------------------------------------------------

# type definitions for the basic statistical measurements have the following
# basic category theoretic data model:
#    __            __
#   |  |          |  |
#   |  v          |  v
# (Effect) ---> (ZScore) ---
#    __             __      |
#   |  |           |  |     |
#   |  v           |  v     | 
# (LogPValue) <- (PValue) <-
#      

# type definitions

Beta = Tuple[Union[float,None]]
StdErr = Tuple[Union[float,None]]
Effect = Tuple[Beta, StdErr]
ZScore = Tuple[Union[float,None]]
PValue = Tuple[Union[float,None]]
LogPValue = Tuple[Union[float,None]]

# mapping functor definitions

# Effect --> ZScore
def compute_zscore(eff: Effect) -> ZScore:
    if (eff[0][0] == None) or (eff[1][0] == None): return (None,)
    else:
        try:
            zscore = (eff[0][0] / eff[1][0])
        except ZeroDivisionError:
            zscore = copysign(inf, eff[0][0])
    return (zscore,)

# ZScore --> PValue
def compute_pvalue(zscore: ZScore) -> PValue:
    if (zscore[0] == None): return (None,)
    else:
        pval =  2.0 * (1 - 0.5 * (1.0 + erf(abs(zscore[0]) / sqrt(2.0))))
        return (pval,)

# PValue --> LogPValue
def compute_logpvalue(pval: PValue) -> LogPValue:
    if (pval[0] == None): return (None,)
    elif (pval[0] == 0):
        return (-inf,)
    else:
        return (-1.0 * log10(pval[0]),)


# object definitions
# -----------------------------------------------------------------------------

# define a SummaryStats object which is a data class that holds the 
# suite of commonly collected statistical measurements from a GWAS study
@dataclass
class SummaryStats:
    beta: Beta
    stderr: StdErr
    effect: Effect = field(init=False)
    zscore: ZScore
    pvalue: PValue
    logp: LogPValue

    def __post_init__(self) -> None:
        self.effect = (self.beta, self.stderr)


# function definitions
# -----------------------------------------------------------------------------

# define a function that takes a SummaryStats object and returns 
# another SummaryStats object with as many of the computable statistics 
# calculated as possible
def complete_summarystats(sumstats: SummaryStats) -> SummaryStats:
    
    # if the attributes in the passed SummaryStats object are empty, compute them from Effect values
    zscore = (compute_zscore(sumstats.effect) if sumstats.zscore == (None,) else sumstats.zscore)
    pvalue = (compute_pvalue(zscore) if sumstats.pvalue == (None,) else sumstats.pvalue)
    logp = (compute_logpvalue(pvalue) if sumstats.logp == (None,) else sumstats.logp)
    
    # return the new SummaryStats object
    return SummaryStats(
        beta=sumstats.beta,
        stderr=sumstats.stderr,
        zscore=zscore,
        pvalue=pvalue,
        logp=logp
    )
