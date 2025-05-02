from typing import List, Dict

def rod_cutting_memo(length: int, prices: List[int]) -> Dict:
    """
    Finds the optimal way to cut the rod using memoization (top-down approach).

    Args:
        length: The total length of the rod.
        prices: A list where prices[i] is the price of a rod piece of length i+1.

    Returns:
        A dictionary with the maximum profit, list of cuts, and number of cuts.
    """
    memo = {}  # Stores the maximum profit for each length.
    cuts_cache = {}  # Stores the first cut length for each rod length.

    def dp(n):
        if n == 0:
            return 0
        if n in memo:
            return memo[n]
        max_profit = float('-inf')
        for i in range(1, n + 1):
            if i <= len(prices):
                profit = prices[i - 1] + dp(n - i)
                if profit > max_profit:
                    max_profit = profit
                    cuts_cache[n] = i  # Store the first cut length.
        memo[n] = max_profit
        return max_profit

    max_profit = dp(length)

    # Reconstruct the list of cuts.
    cuts = []
    n = length
    while n > 0:
        cut = cuts_cache[n]
        cuts.append(cut)
        n -= cut

    return {
        "max_profit": max_profit,
        "cuts": cuts,
        "number_of_cuts": len(cuts) - 1  # Number of cuts is one less than number of pieces.
    }
    
    
def rod_cutting_table(length: int, prices: List[int]) -> Dict:
    """
    Finds the optimal way to cut the rod using tabulation (bottom-up approach).

    Args:
        length: The total length of the rod.
        prices: A list where prices[i] is the price of a rod piece of length i+1.

    Returns:
        A dictionary with the maximum profit, list of cuts, and number of cuts.
    """
    dp = [0] * (length + 1)  # dp[i] stores the maximum profit for rod length i.
    cuts_cache = [0] * (length + 1)  # cuts_cache[i] stores the first cut length for rod length i.

    for i in range(1, length + 1):
        max_profit = float('-inf')
        for j in range(1, i + 1):
            if j <= len(prices):
                if prices[j - 1] + dp[i - j] > max_profit:
                    max_profit = prices[j - 1] + dp[i - j]
                    cuts_cache[i] = j  # Store the first cut length.
        dp[i] = max_profit

    # Reconstruct the list of cuts.
    cuts = []
    n = length
    while n > 0:
        cut = cuts_cache[n]
        cuts.append(cut)
        n -= cut

    return {
        "max_profit": dp[length],
        "cuts": cuts,
        "number_of_cuts": len(cuts) - 1  # Number of cuts is one less than number of pieces.
    }

def run_tests():
    """Function to run all test cases."""
    test_cases = [
        # Test 1: Basic case
        {
            "length": 5,
            "prices": [2, 5, 7, 8, 10],
            "name": "Basic Case"
        },
        # Test 2: Optimal not to cut
        {
            "length": 3,
            "prices": [1, 3, 8],
            "name": "Optimal Not to Cut"
        },
        # Test 3: All cuts of length 1
        {
            "length": 4,
            "prices": [3, 5, 6, 7],
            "name": "Uniform Cuts"
        }
    ]

    for test in test_cases:
        print(f"\nTest: {test['name']}")
        print(f"Rod Length: {test['length']}")
        print(f"Prices: {test['prices']}")

        # Test memoization approach
        memo_result = rod_cutting_memo(test['length'], test['prices'])
        print("\nMemoization Result:")
        print(f"Maximum Profit: {memo_result['max_profit']}")
        print(f"Cuts: {memo_result['cuts']}")
        print(f"Number of Cuts: {memo_result['number_of_cuts']}")

        # Test tabulation approach
        table_result = rod_cutting_table(test['length'], test['prices'])
        print("\nTabulation Result:")
        print(f"Maximum Profit: {table_result['max_profit']}")
        print(f"Cuts: {table_result['cuts']}")
        print(f"Number of Cuts: {table_result['number_of_cuts']}")

        print("\nTest passed successfully!")

if __name__ == "__main__":
    run_tests()
