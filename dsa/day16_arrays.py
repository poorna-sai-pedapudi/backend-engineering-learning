# Problem 1: Find maximum number in array
nums = [4,7,2,9,1]
max_num = nums[0]

for num in nums:
    if num > max_num:
        max_num = num

print(f"maximum number in array is {max_num}")

# Problem 2: Find sum of array
nums = [1,2,3,4]

total = 0
for num in nums:
    total += num

print(f"the sum of array is {total}")

# Problem 3: Count even numbers

nums = [1,2,4,7,8]

count = 0
for num in nums:
    if num % 2 == 0:
        count += 1

print(f"The count of even numbers is {count}")