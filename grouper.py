import os, shutil, string, sys

def stringify(input_list, delimiter):
    """
    stringify(input_list, delimiter) --> String
    Function that accepts a list and a string as arguments and joins the list
    using the string as the delimiter.
    """
    output_string = ""
    for item in input_list:
        output_string += item + delimiter
    return output_string[:(-1 * len(delimiter))]

def group(path, delimiter):
    """
    group(path, delimiter) --> List
    Function that accepts the folder path as argument,
    navigates to this folder using a cmd command and groups the files
    there by name.
    Also accepts delimiter as an argument: all files with
    the same string before the delimiter will be grouped into the same
    folder (e.g. myfile-1.txt, myfile-2.txt, myfile-3.txt will all be grouped
    into a myfile folder if the delimiter is '-').
    The first character in the name of each file should be a letter.
    """
    try:
        os.chdir(path)
        os.system("dir > pygrouper.pyg")
        file_name = ""
        folder_name = ""
        folders_list = []
        state = True
        with open(path + "pygrouper.pyg", 'r') as f:
            for line in f.readlines():
                if (len(line) == 1 or "DIR" in line or line.startswith(" Vol")
                    or line.startswith(" Dir")):
                    continue
                line = line.split(' ')
                try:
                    line.remove('AM')
                except:
                    pass
                try:
                    line.remove('PM')
                except:
                    pass
                line = stringify(line, ' ')
                for char in line:
                    if char == delimiter and len(file_name) > 0 and (
                            not file_name.strip() in folders_list and state):
                        state = False
                        folder_name = 'grouper-' + file_name
                        folder_name = folder_name.strip()
                        folders_list.append(folder_name)
                        os.system('md "' + folder_name + '"')
                    if char == '\n':
                        if not (os.system('copy "' + file_name
                                + '" "' + folder_name + '"') == 0):
                            print("Could not copy", file_name)
                        file_name = ""
                        folder_name = ""
                        state = True
                        break
                    if char in string.ascii_letters or len(file_name) > 0:
                        file_name += char
        return list(set(folders_list))
    except:
        print("Error.", sys.exc_info()[1])
        return None

def remove_old(path, folders_list):
    """
    remove_old(path, folders_list) --> None
    Function that removes all the files in path for which folders have been
    created.
    """
    for f in folders_list:
        try:
            g = f.replace("grouper-", '')
            os.rename(path + f, path + g)
            f = g
            for item in os.listdir():
                try:
                    if f in item and len(item) > len(f):
                        os.remove(item)
                except:
                    continue
        except:
            continue

def undo(path, folders_list):
    """
    undo(path, folders_list) --> None
    Function that removes all folders in folder_list from path.
    """
    if type(folders_list) == type(list()):
        for f in folders_list:
            try:
                shutil.rmtree(path + f)
            except:
                pass

def main():
    folder = input("Folder Path >> ")
    path = folder + '/' if not folder.endswith('/') else folder
    delimiter = input("Delimiter >> ") if input(
                "Change delimiter from '-'? (1 for Yes) >> ") == '1' else '-'
    folders_list = group(path, delimiter)
    if not type(folders_list) == type(list()):
        return
    choice = input("Please check the folder(s) created. \
Enter 1 if satisfied or 2 to undo >> ")
    if choice == '1':
        remove_old(path, folders_list)
    else:
        undo(path, folders_list)
    os.remove("pygrouper.pyg")
    print("All done. Exiting...")

main()
