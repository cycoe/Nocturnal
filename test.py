from modules.listUtils import filter_with_keys


key = ['1', '4']

table_ = [
    ['1', '3'],
    ['2', '3'],
    ['2', '4'],
    ['3'],
    ['1']
]

filtered = filter_with_keys(table_, key)
print(filtered)
