"""
Created on July 04, 2013
@author: C.J. Hutto

Citation Information

If you use any of the VADER sentiment analysis tools
(VADER sentiment lexicon or Python code for rule-based sentiment
analysis engine) in your work or research, please cite the paper.
For example:

  Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for
  Sentiment Analysis of Social Media Text. Eighth International Conference on
  Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014.

Updated for python3 by CG
"""

import os, math, re, sys, fnmatch, string

def sentiment(text):
    """
    Returns a float for sentiment strength based on the input text.
    Positive values are positive valence, negative value are negative valence.
    """
    return 0
