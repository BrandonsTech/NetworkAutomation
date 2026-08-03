
import sys

if __name__ == "__main__":
    args = sys.argv
    print('Name: ' + args[1])
    print('Location: ' + args[2])
    print(args)

if __name__ == "__main__":
    with open('sys_module_made_this', 'w') as F:
        args = sys.argv
        F.write(f'Name: {args[1]}\n')
        F.write(f'Location: {args[2]}\n')
        F.write(f'{args}')