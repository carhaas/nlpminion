#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import subprocess
import math
from collections import Counter  # multiset represented by dictionary


def translate(decoder_bin, ini, weights, nl_file, kbest=0):
    '''Given a file of input sentence, a cdec configuration, some weights and the location of the decoder bin,
    sends a call to cdec and returns cdec'c translation as a string. Optionally returns a unique k-best list whose
    size can be set via kbest

    :param decoder_bin: the location of the cdec script
    :param ini: the cdec configuration file
    :param weights: a weights file
    :param nl: the file containing sentences to be translated
    :param kbest: the size of the kbest list
    :return: the translation string as returned by cdec
    '''
    args = [decoder_bin,
            '-c', ini,
            '-w', weights,
            '-i', nl_file]
    if kbest != 0:
        args += ['-k', '%s' % kbest, '-r']
    proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (out, err) = proc.communicate()
    proc.stdout.close()
    proc.stderr.close()
    try:
        proc.kill()
    except OSError:
        pass
    return out


def translate_sentence(decoder_bin, ini, weights, nl, kbest=0):
    '''Given a string, a cdec configuration, some weights and the location of the decoder bin,
    sends a call to cdec and returns cdec'c translation as a string. Optionally returns a unique k-best list whose
    size can be set via kbest

    :param decoder_bin: the location of the cdec script
    :param ini: the cdec configuration file
    :param weights: a weights file
    :param nl: the natural language string to be translated
    :param kbest: the size of the kbest list
    :return: the translation string as returned by cdec
    '''
    args = [decoder_bin,
            '-c', ini,
            '-w', weights]
    if kbest != 0:
        args += ['-k', '%s' % kbest, '-r']
    echo = subprocess.Popen(('echo', '%s' % nl), stdout=subprocess.PIPE)
    proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=echo.stdout)
    (out, err) = proc.communicate()
    echo.stdout.close()
    proc.stdout.close()
    proc.stderr.close()
    try:
        proc.kill()
    except OSError:
        pass
    try:
        echo.kill()
    except OSError:
        pass
    return out


def bleu(script_path, references, input):
    '''
    Given a file to be scores and its true references, calls cdec's corpus-wide BLEU script
    and returns the value as a string

    :param script_path: the path where cdec's bleu script lies
    :param references: a file containing translation options for
    :param input: a file containg the sentence to be scored
    :return: a corpus-wide BLEU score
    '''
    args = [script_path,
            '-r', references,
            '-i', input]
    proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (out, err) = proc.communicate()
    proc.stdout.close()
    proc.stderr.close()
    try:
        proc.kill()
    except OSError:
        pass
    return out


def per_sentence_bleu(nl, references, n=4, smooth=0.0):
    '''
    Implementation of per-sentence BLEU as defined by (Nakov et al., 2012).

    A string to be scored and its reference(s) (more than 1 possible per sentence) are passed to the function.
    It returns the per-sentence BLEU score.
    Optionally changed the n-gram size via n and a smoothing parameter via smooth.

    :param nl: a natural language string to be investigated
    :param references: the nl's true translation option(s)
    :param n: order of n-gram
    :param smooth: smoothing value
    :return: per-sentence BLEU score
    '''
    if nl.strip() == "":
        return 0.0  # no translation
    log_bleu = 0.0
    # get longest ref
    longest_ref = max(len(ref.split()) for ref in references)
    for i in range(1, n + 1):  # 1 to n-gram
        try:
            log_bleu += ngram(nl, references, i)
        except ValueError:
            return 0.0
    log_bleu = log_bleu / min(n, longest_ref)  # divide by n or length of ref if its lower than n
    # word penalty calculations
    input_len = len(nl.strip().split(" "))
    # adding the ref len outside the abs again allows us to pick the smaller ref when there is a draw
    diff = [math.fabs(input_len - len(ref.split())) + len(ref.split()) for enum, ref in enumerate(references)]
    best_match_length = len(references[diff.index(min(diff))].strip().split(" "))
    brevity_penalty = min(0.0, 1.0 - ((best_match_length + smooth) / input_len))
    log_bleu += brevity_penalty
    return math.exp(log_bleu)


def ngram(nl, references, n):
    '''
    Given a sentence to be scored and its reference, counts how many (clipped) n-gram in the sentence
    are also in the reference.

    :param nl: a natural language string to be investigated
    :param references: the nl's true translation option(s)
    :param n: order of n-gram
    :return: the n-gram based precision of this n-gram order
    '''
    input_ngrams = Counter(zip(*[nl.split(" ")[i:] for i in range(n)]))
    references_ngrams = []
    for ref in references:
        references_ngrams = Counter(zip(*[ref.split(" ")[i:] for i in range(n)]))
    count_input_ngrams = 0
    count_clipped = 0
    if n >= 2:
        add = 1.0
    else:
        add = 0.0
    for ngram in input_ngrams:
        count_clipped += min(input_ngrams[ngram], references_ngrams[ngram])
        count_input_ngrams += input_ngrams[ngram]
    # means that the sentence does not even contain a unigram of the reference,
    # would cause log(0) below so we raise here so we can catch and return 0.0 BLEU in caller function
    if (count_clipped+add) == 0:
        raise ValueError("math domain error")
    return math.log(count_clipped + add) - math.log(count_input_ngrams + add)