import re, nltk
from nltk.util import ngrams, skipgrams
from nltk.tokenize import word_tokenize, sent_tokenize

from util.lcs import LCS
from util.wlcs import WLCS
from util.stemmer import stem
from util.ta import nChars

from math import sqrt, factorial

def nCr(n,r):
    f = factorial
    return f(n) / f(r) / f(n-r)

def tokenize(text, grams=1):
  wordStems = lambda s: map(stem, word_tokenize(s))
  sentTokens = lambda tok, s: tok + wordStems(s)

  if grams == 1:
    return list(reduce(sentTokens, sent_tokenize(text), [ ]))
  else:
    return list(ngrams(reduce(sentTokens, sent_tokenize(text), [ ]), grams))

def rougeN(candidateSummary, refrenceSummaries, grams):
  candidateGrams = set(tokenize(candidateSummary, grams))
  refGrams = lambda s: set(tokenize(s, grams))
  rogueScore = lambda s: float(len(candidateGrams & refGrams(s))) / len(refGrams(s))

  return max(map(rogueScore, refrenceSummaries))

def rougeL(candidateSummary, refrenceSummaries):
  B = 1

  lcs  = lambda s: nChars( LCS(tokenize(candidateSummary), tokenize(s)) )
  Rlcs = lambda s: float(lcs(s)) / nChars(candidateSummary)
  Plcs = lambda s: float(lcs(s)) / nChars(s)

  Flcs = lambda s: (1 + B ** 2) * Rlcs(s) * Plcs(s) / ( Rlcs(s) + B ** 2 * Plcs(s) ) if lcs(s) > 0 else 0

  return max(map(Flcs, refrenceSummaries))

def rougeW(candidateSummary, refrenceSummaries):
  B = 1

  wlcs = lambda s: WLCS(tokenize(candidateSummary), tokenize(s))
  Rlcs = lambda s: sqrt( float(wlcs(s)) / pow(nChars(candidateSummary),2) )
  Plcs = lambda s: sqrt( float(wlcs(s)) / pow(nChars(s),2) )

  Flcs = lambda s: (1 + B ** 2) * Rlcs(s) * Plcs(s) / ( Rlcs(s) + B ** 2 * Plcs(s) ) if wlcs(s) > 0 else 0

  return max(map(Flcs, refrenceSummaries))

def rougeS(candidateSummary, refrenceSummaries):
  B = 1

  candidateTokens = tokenize(candidateSummary)
  skip2  = lambda s: len(set(skipgrams(candidateTokens,2,2)) & set(skipgrams(tokenize(s), 2, 2)))

  Rskip2 = lambda s: float(skip2(s)) / nCr(len(candidateTokens), 2)
  Pskip2 = lambda s: float(skip2(s)) / nCr(len(tokenize(s)), 2)

  Fskip2 = lambda s: (1 + B ** 2) * Rskip2(s) * Pskip2(s) / ( Rskip2(s) + B ** 2 * Pskip2(s) ) if skip2(s) > 0 else 0

  return max(map(Fskip2, refrenceSummaries))
