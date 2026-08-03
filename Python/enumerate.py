groceries = ['apples', 'bananas', 'milk', 'bread', "tomato"]

for index, each in enumerate(groceries):
    if each == 'bread':
        print(f'{index} {each}')
        break
    if each == 'milk':
        print(f'{index} {each}')
        continue
    else:
        print("nothing")
if __name__ == '__main__':
    print("True")