START = 145852
END = 616942

def is_valid_p1(pw):
    pw = list(str(pw))
    # make sure there's at least one duplicate
    if len(set(pw)) == len(pw):
        return False
    for i in range(1,6):
        if pw[i] < pw[i-1]:
            return False

    return True

def is_valid_p2(pw):
    pw = list(str(pw))
    for i in range(1,6):
        if pw[i] < pw[i-1]:
            return False

    for digit in set(pw):
        if pw.count(digit) == 2:
            return True

    return False

def main():
    # find real start
    counter_p1 = 0
    counter_p2 = 0
    for pw in range(START, END):
        counter_p1 += 1 if is_valid_p1(pw) else 0
        counter_p2 += 1 if is_valid_p2(pw) else 0

    print(f'Part 1: {counter_p1}')
    print(f'Part 2: {counter_p2}')

if __name__ == '__main__':
    main()
