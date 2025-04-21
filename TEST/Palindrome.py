def is_palindrome(s):
    clean = ""

    for char in s:
        if char.isalnum():
            clean += char.lower()
    
    reversed = ""
    for char in clean:
        reversed = char + reversed

    if clean == reversed:
        return "Yes"
    elif clean != reversed:
        return "No"

    
    

print(is_palindrome("A man, a plan, a canal, Panama!"))
print(is_palindrome("No 'x' in Nixon"))
print(is_palindrome("Was it a car or a cat I saw?"))
print(is_palindrome("Madam, in Eden, I'm Adam"))
print(is_palindrome("racecar"))
print(is_palindrome("12321"))
print(is_palindrome("Able was I ere I saw Elba"))
print(is_palindrome("Hello, World!"))
print(is_palindrome("Step on no pets"))
print(is_palindrome("Not a palindrome"))

