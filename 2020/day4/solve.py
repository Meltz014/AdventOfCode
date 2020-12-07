import re

def part1(db):
    required = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}
    valid_passports = []
    for passport in db:
        # valid if contains all fields but cid
        keys = set(passport.keys())
        if required.issubset(keys):
            valid_passports.append(passport)
    print(f'Part1: {len(valid_passports)}')
    return valid_passports

def part2(db):
    """
    byr (Birth Year) - four digits; at least 1920 and at most 2002.
    iyr (Issue Year) - four digits; at least 2010 and at most 2020.
    eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
    hgt (Height) - a number followed by either cm or in:
        If cm, the number must be at least 150 and at most 193.
        If in, the number must be at least 59 and at most 76.
    hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
    ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
    pid (Passport ID) - a nine-digit number, including leading zeroes.
    cid (Country ID) - ignored, missing or not.
    """
    valid_passports = []
    for passport in db:
        try:
            byr = int(passport['byr'])
            if byr not in range(1920, 2003):
                continue
            iyr = int(passport['iyr'])
            if iyr not in range(2010, 2021):
                continue
            eyr = int(passport['eyr'])
            if eyr not in range(2020, 2031):
                continue
            hgt = int(passport['hgt'][:-2])
        except ValueError:
            # invalid int
            continue
        unit = passport['hgt'][-2:].lower()
        if unit == 'in':
            if hgt not in range(59, 77):
                continue
        elif unit == 'cm':
            if hgt not in range(150, 194):
                continue
        else:
            # invalid units
            continue

        mobj = re.match(r'#[0-9a-f]', passport['hcl'].lower())
        if not mobj:
            continue

        if passport['ecl'].lower() not in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']:
            continue

        if not (len(passport['pid']) == 9 and passport['pid'].isnumeric()):
            continue

        valid_passports.append(passport)
    print(f'Part 2: {len(valid_passports)}')


def main():
    with open('day4\input.txt') as fid:
        lines = fid.readlines()

    # build db of passports
    # byr (Birth Year)
    # iyr (Issue Year)
    # eyr (Expiration Year)
    # hgt (Height)
    # hcl (Hair Color)
    # ecl (Eye Color)
    # pid (Passport ID)
    # cid (Country ID)
    db = []
    passport = {} # current passport
    for line in lines:
        line = line.strip()
        if not line:
            # blank line.  Add cur to db and reset
            db.append(passport)
            passport = {}
            continue
        fields = line.split(' ')
        for f in fields:
            (k, v) = f.split(':')
            passport[k] = v
    db.append(passport)
    passport = {}

    valid_db = part1(db)
    part2(valid_db)

if __name__ == '__main__':
    main()