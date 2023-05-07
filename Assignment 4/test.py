import random
import matplotlib.pyplot as plt

lower_bound = 0
upper_bound = 10
expected_value = 3

random_values = [random.triangular(lower_bound, upper_bound, expected_value) for _ in range(100000)]

plt.hist(random_values, bins=300, density=True)
plt.xlabel('Value')
plt.ylabel('Probability Density')
plt.title('Triangular Distribution')
plt.show()
