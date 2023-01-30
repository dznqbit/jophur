import sys
print("UTIL TEST!", sys.path)
from lib.jophur.util import lerp, rotate_index

def test_lerp():
  assert lerp(0.0, 5, 9) == 5
  assert lerp(1.0, 5, 9) == 9
  assert lerp(0.6, 0, 10) == 6
