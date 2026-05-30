# Problem 1 - Frequency Counter

nums = [1,1,2,3,3,3]

freq = {}

for num in nums:
    if num in freq:
        freq[num] += 1
    else:
        freq[num] = 1

print(f"Frequency of numbers is {freq}")


#Problem 2 - First Repeated Number

nums = [5,2,1,5,3]

seen = {}

for num in nums:
    if num in seen:
        print(num)
        break
    else:
        seen[num] = True


#Problem 3 - Character Frequency

word = "backend"

freq = {}

for ch in word:
    if ch in freq:
        freq[ch] += 1
    else:
        freq[ch] = 1

print(f"Frequency of characters is {freq}")