# Problem 1, Reverse the array

nums = [1,2,3,4,5]

#expected = [5,4,3,2,1]

left = 0
right = len(nums) - 1

while left < right:
    nums[left], nums[right] = nums[right], nums[left]

    left += 1
    right -= 1

print(nums)


# Problem 2, Check Palindrome

word = "madam"

left = 0
right = len(word) - 1

is_palindrome = True

while left < right:
    if word[left] != word[right]:
        is_palindrome = False
        break
    
    left += 1
    right -= 1

print(is_palindrome)


# Problem 3, Move zeroes to end

nums = [1,0,2,0,4]

#expected = [1,2,4,0,0]

left = 0

for right in range(len(nums)):
    if nums[right] != 0:
        nums[left], nums[right] = nums[right], nums[left]
        left += 1

print(nums)