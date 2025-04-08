# CMPS 2200 Assignment 3
## Answers

**Name:**Viraj Choksi


Place all written answers from `assignment-03.md` here for easier grading.


1a)
To make change for N dollars using the fewest number of coins (with denominations that are all powers of 2), you should:
1. Start with the largest coin that is less than or equal to N.
2. Use one of that coin, subtract its value from N.
3. Repeat the process with the new remaining amount.
4. Keep doing this until the remaining amount becomes zero.

This works because powers of 2 allow you to build up any number using a unique combination of these coins, like how binary numbers work.
This means that at each step, you’re grabbing the biggest piece you can without going over the remaining amount.


1b)
Greedy Choice Property
At each step, choosing the largest coin ≤ N is always part of some optimal solution.
Proof:
Assume, for contradiction, that an optimal solution does not include the largest coin 2^i ≤ N. 
Then all the coins used must be smaller than 2^i, i.e. from (2^0, ..., 2^(i-1))
But the sum of any number of such coins can only produce multiples of 2^i − 1 at most: Max sum of m coins = m ⋅ 2^(i−1)
So you would need at least 2 or more such coins to match or exceed 2^i, contradicting the goal of using fewer coins. Hence, it’s always
better to take the largest available coin.

Optimal Substructure
The problem of making change for N − 2^i is a subproblem of making change for N, and solving it optimally leads to an optimal solution for N.
Proof: If we optimally solve the subproblem N − 2^i, and we already took 2^i, then together we get an optimal solution for N There’s no advantage to rearranging the coins because the denominations are powers of 2 and uniquely sum to any number in binary form. 
Thus, the greedy algorithm always gives the minimal number of coins.


1c)
Work:
The total work is proportional to the number of 1s in the binary representation of N, since each 1 represents a coin.
Converting N to binary takes O(log N) time, and counting the 1s also takes O(log N) time.
So overall work = O(log N).
Span:
If done sequentially (e.g., subtracting coins one by one), the span is O(log N).
But if we just want the number of coins (i.e., number of 1s in binary), we can do this in parallel with O(1) span.


2a)
Let’s say the coin denominations are: D = [1, 3, 4]. You want to make N = 6.
Greedy approach (take largest coin ≤ N at each step):
- Take 4 -> remaining = 2
- Take 1 -> remaining = 1
- Take 1 -> remaining = 0
Total coins = 3 (4 + 1 + 1)

But the optimal solution is:
3 + 3 = 6 -> uses 2 coins

So greedy gives 3 coins, but optimal is 2 coins. This shows that greedy does not always produce the minimum.


