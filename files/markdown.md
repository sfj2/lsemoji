hexer
=====

A simple utility to toggle between hex and rgb colour values.

Example usage:

    % hexer.py '#0ff'
    rgb(0,255,255)
    % hexer.py 'rgb(255,192,3)'
    #FFC103
    % hexer.py 'rgba(134,23,192,0.3)'
    #8617C0
    % echo '#89cf0a' | hexer.py
    rgb(137,207,10)
