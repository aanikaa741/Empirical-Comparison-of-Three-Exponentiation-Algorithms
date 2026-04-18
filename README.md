# Empirical-Comparison-of-Three-Exponentiation-Algorithms

This project compares three algorithms for integer exponentiation. Naive iterative exponentiation is an algorithm that has O(n) time complexity. Fast exponentiation by squaring can achieve O(log n) time complexity by applying the divide-and-conquer technique. Similarly, O(log n) time complexity is achieved in modular exponentiation due to the use of modular arithmetic. 

Four distinct experiments are designed and conducted, spanning exponent values from 500 to 1,000,000. Seven graphs are generated to evaluate empirical performance against theoretical predictions. The results confirm both O(n) and O(log n) complexities, quantify speedup factors exceeding 100× at n = 20,000, and demonstrate that Python's arbitrary-precision integer arithmetic introduces a measurable secondary cost that diverges from the idealized unit-cost multiplication model assumed in theoretical analysis. The results confirm both O(n) and O(log n) complexities, and quantify speedup factors exceeding 100× at n = 20,000, and demonstrate that Python's arbitrary-precision integer arithmetic introduces a measurable secondary cost that diverges from the idealized unit-cost multiplication model assumed in theoretical analysis.

Algorithm 1 - Naive Iterative Exponentiation
Algorithm Description
The basic algorithm computes aⁿ starting from result=1 and multiplying result by the base a, a total of n times, inside a for loop. In other words, the algorithm is the simplest computational implementation of the mathematical expression.

Algorithm 2 - Fast Exponentiation by Squaring
Algorithm Description
The fast exponentiation algorithm uses a divide-and-conquer strategy and achieves O(log n) time complexity by reducing the number of multiplications from n to O(log n). The algorithm works as follows: it splits the exponent n into binary form (i.e., the number's binary representation) from its LSB to MSB and computes powers of base: a¹, a², a⁴, a⁸, and so on, multiplying only required powers of a according to positions of bits "1".

Algorithm 3 - Modular Exponentiation
Algorithm Description
Modular exponentiation computes (aⁿ) mod m using the same divide-and-conquer squaring strategy as Algorithm 2, with one critical addition: every multiplication is immediately followed by a modular reduction. By applying mod m after each operation, all intermediate values are bounded by m², ensuring that no number ever exceeds a fixed size regardless of how large n or a becomes.

Experiment 1 — Runtime vs Exponent Value

Experiment 2 — Large Exponent Scalability

Experiment 3 — Theoretical Complexity Validation

Experiment 4 - Effect of Base Value
