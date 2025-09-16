import math
from typing import List


def feature_vector_int(n: int) -> List[float]:
	# Core arithmetic features in [0,1] or {0,1}
	mod2 = 1.0 if (n & 1) else 0.0
	mod3 = 1.0 if (n % 3) in (1, 2) else 0.0
	mod5 = 1.0 if (n % 5) not in (0,) else 0.0
	mod6_15 = 1.0 if (n % 6) in (1, 5) else 0.0
	mod30_rr = 1.0 if (n % 30) in (1, 7, 11, 13, 17, 19, 23, 29) else 0.0
	frac8 = (n % 8) / 7.0
	frac12 = (n % 12) / 11.0
	frac30 = (n % 30) / 29.0
	last_digit_rr = 1.0 if (n % 10) in (1, 3, 7, 9) else 0.0
	return [
		mod2,
		mod3,
		mod5,
		mod6_15,
		mod30_rr,
		frac8,
		frac12,
		frac30,
		last_digit_rr,
	]


