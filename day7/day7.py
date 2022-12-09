import os


#------------------------------------------------------------------------------
class FileObject(object):
    def __init__(self, name, size=0, parent=None, children=[], is_dir=False):
        self.name = name
        self.size = size
        self.parent = parent
        self.children = children
        self.is_dir = is_dir
        if self.is_dir:
            self.size = 0
            print("Adding directory object {}".format(self.name))
        else:
            print("Adding file object {}".format(self.name))
    
    def get_parent(self):
        return self.parent

    def set_parent(self, parent):
        self.parent = parent
    
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
    if depth > 16:
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
    filesys = FileObject('/', is_dir=True)
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
                    pass
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
    while type(filesys.parent) != type(None):
        filesys = filesys.parent

    # now print our file system
    print("==========")
    print("FILESYSTEM")
    print("==========")
    print_fs_recursive(filesys, 0)
