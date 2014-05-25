#!/usr/bin/python
import random
from serpent import parser, rewriter, compiler, lllparser

def bijection_test_lllparser(lll):
    text = lllparser.serialize_lll(lll)
    i = 0
    n = random.randrange(4)  # No comments yet.
    while i >= 0 and n > 0:
        i = text.find('\n', i)
        n -= 1
    if i > 0:
        text = text[:i] + '\n' + text[i:]
    print(text)

    parsed_lll = lllparser.parse_lll(text)
    if parsed_lll.listfy() != lll.listfy():
        print("BUG: Parsing output again gave different result!")
        print(lll)
        print(parsed_lll)
        print("")

t = open('tests.txt').readlines()
i = 0
while True:
    o = []
    while i < len(t) and (not len(t[i]) or t[i][0] != '='):
        o.append(t[i])
        i += 1
    i += 1
    print '================='
    text = '\n'.join(o).replace('\n\n', '\n')
    print text
    ast = parser.parse(text)
    print "AST:", ast
    print ""
    lll = rewriter.compile_to_lll(ast)
    print "LLL:", lll
    print ""
    bijection_test_lllparser(lll)

    varz = rewriter.analyze(ast)
    print "Analysis: ", varz
    print ""
    aevm = compiler.compile_lll(lll)
    print "AEVM:", ' '.join([str(x) for x in aevm])
    print ""
    code = compiler.assemble(aevm)
    print "Output:", code.encode('hex')
    if i >= len(t):
        break
