import os


#------------------------------------------------------------------------------
class FileObject(object):
    def __init__(self, name, size=0, parent=None, is_dir=False):
        self.name = name
        self.size = size
        self.parent = parent
        self.children = []
        self.is_dir = is_dir
        if self.is_dir:
            self.size = 0
            print("Adding directory object {}".format(self.name))
        else:
            print("Adding file object {}".format(self.name))
    
    def add_child(self, child):
        self.children.append(child)
    
    def get_size(self):
        size = 0
        if self.is_dir:
            for child in self.children:
                size += child.get_size()
        else:
            size = self.size

        return size

#------------------------------------------------------------------------------
def print_fs_recursive(filesys: FileObject, depth: int):
    if depth >= 16:
        return
    print_filesystem(filesys, depth)
    if len(filesys.children) > 0:
        for child in filesys.children:
            print_fs_recursive(child, depth + 1)
#------------------------------------------------------------------------------
def print_filesystem(filesys: FileObject, depth: int):

    print(" "*depth, end='')
    print(" - {}".format(filesys.name), end='')
    if filesys.is_dir:
        print(" (dir)")
    else:
        print(" (file, size={})".format(filesys.size))
#------------------------------------------------------------------------------
def sum_small_dirs(filesys, thresh):
    this_size = filesys.get_size()
    this_sum = 0
    if filesys.is_dir and this_size <= thresh:
        this_sum += this_size

    if filesys.is_dir and len(filesys.children) > 0:
        for child in filesys.children:
            this_sum += sum_small_dirs(child, thresh)
    return this_sum
#------------------------------------------------------------------------------
def find_dirs_to_delete(filesys, size, candidates):
    this_size = filesys.get_size()
    if filesys.is_dir and this_size >= size:
        candidates.append(this_size)

    if filesys.is_dir and len(filesys.children) > 0:
        for child in filesys.children:
            find_dirs_to_delete(child, size, candidates)
#------------------------------------------------------------------------------
if __name__ == "__main__":
    file_list = os.listdir()
    for i in range(0, len(file_list)):
        print("{}\t{}".format(i, file_list[i]))

    try:
        fname = file_list[int(input("Line Number: "))]
    except IndexError or ValueError:
        fname = "datastream.txt"

    f = open(fname, 'r')


    # FIRST CONSTRUCT FILESYSTEM
    filesys_root = FileObject('/', is_dir=True)
    filesys = filesys_root
    cmd = ''
    for line in f:
        parts = line.strip().split(' ')

        if parts[0] == '$':
            cmd = parts[1]
            if cmd == 'cd':
                print("change directory cmd -> {}".format(parts[2]))
                cd_dest = parts[2]
                if cd_dest == '..':
                    if type(filesys.parent) != type(None):
                        filesys = filesys.parent
                elif cd_dest == '/':
                    while type(filesys.parent) != type(None):
                        filesys = filesys.parent
                else:
                    for child in filesys.children:
                        if child.is_dir and child.name == cd_dest:
                            filesys = child
                            break
            elif cmd == 'ls':
                print("list contents of {}".format(filesys.name))
        elif cmd == 'ls':
            
            if parts[0] == 'dir':
                filesys.add_child(FileObject(parts[1], parent=filesys, is_dir=True))
            else:
                filesys.add_child(FileObject(parts[1], parent=filesys, size=int(parts[0])))

    # first, go to our root directory
    # filesys = filesys_root

    # now print our file system
    print("==========")
    print("FILESYSTEM")
    print("==========")
    print_fs_recursive(filesys_root, 0)
    print("==========")

    n_small_dirs = sum_small_dirs(filesys_root, 100000)
    print("\nSum of sizes of all dirs at most 100000 in size is : {}".format(n_small_dirs))

    total_space  = 70000000
    needed_space = 30000000

    full_space = filesys_root.get_size()
    space_to_free = needed_space - (total_space - full_space)

    print("Directory / is {} units in size.".format(full_space))
    print("We need to free up {} units.".format(space_to_free))
    
    candidates = []

    find_dirs_to_delete(filesys_root, space_to_free, candidates)
    print("CANDIDATES FOR DELETION:")
    print(candidates)
    print("\nThe minimum sized file then is of size {}.".format(min(candidates)))