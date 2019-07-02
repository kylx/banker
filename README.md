# banker

All 2d resource arrays follows this format:

 ```
      A   B   C
 c1   1   2   3
 c2   4   5   6
 c3   7   8   9
```
where `resources={A,B,C}` and `customers={c1,c2,c3}`

## Files

`test.py` - run this to start

`max.txt` - maximum resources that can be requested

`state.py` - takes care of managing the state of resources

`banker.py` - contains the algorithm

`prettyprint.py` - handles outputting the state in a pretty format

`reqs.txt` - pip requirements. Install first on virtual environment
