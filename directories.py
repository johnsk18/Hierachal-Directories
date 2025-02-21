import sys

"""
Parses `name` into a list of strings based on `separator`
"""
def parseString(name, separator):
    part = ""
    parts = []
    for character in name:
        if character == separator:
            parts.append(part)
            part = ""
        else:
            part += character

    parts.append(part)
    return parts

"""
Hierarchical tree structure that can create, list, move, and delete directories given to it.
"""
class Tree:
    def __init__(self):
        self.tree = {}

    """
    Creates a directory at the given `path`
    """
    def create(self, path):
        print("CREATE", path)
        directories = parseString(path, '/')

        current = self.tree

        for directory in directories:
            if directory not in current:
                current[directory] = {}
            current = current[directory]

    """
    Lists all directories in the tree
    """
    def list(self):
        print("LIST")

        stack = [("", self.tree, -1)]
        
        while len(stack) > 0:
            curr_key, curr_value, depth = stack.pop()

            if depth > -1:
                print(("  " * depth) + curr_key)

            for key, value in sorted(curr_value.items(), reverse=True):
                stack.append((key, value, depth + 1))
    
    """
    Moves a directory from `source` to `destination`
    """
    def move(self, source, destination):
        print("MOVE", source, destination)
        
        source_item = self.delete(source, return_item=True)
        source_key, source_value = source_item.popitem()

        destination_item = self.tree
        destination_parts = parseString(destination, '/')
        for part in destination_parts:
            if part not in destination_item:
                destination_item[part] = {}
            destination_item = destination_item[part]

        destination_item[source_key] = source_value

    """
    Deletes a directory at the given `path`
    """
    def delete(self, path, return_item=False):
        if not return_item:
            print("DELETE", path)

        source_parts = parseString(path, '/')
        source_key = source_parts[-1]
        source_item = self.tree
        for part in source_parts[:-1]:
            if part not in source_item:
                raise LookupError(f"Cannot delete {path} - {part} does not exist")
            source_item = source_item[part]

        if source_key not in source_item:
            raise LookupError(f"Cannot delete {path} - {source_key} does not exist")

        source_copy = dict(source_item[source_key])
        del source_item[source_key]

        if return_item:
            return {source_key : source_copy}
        

if __name__ == "__main__":
    tree = Tree()

    # If a file path is given, read and execute the commands
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        with open(file_path, "r") as file:
            for line in file:
                input_list = parseString(line.strip(), ' ')
                operation, args = input_list[0], input_list[1:]
                try:
                    if operation == "CREATE":
                        tree.create(*args)
                    elif operation == "LIST":
                        tree.list()
                    elif operation == "MOVE":
                        tree.move(*args)
                    elif operation == "DELETE":
                        tree.delete(*args)
                    else:
                        raise ValueError(f"Cannot perform command - {operation} does not exist")
                except Exception as e:
                    print(e)
                    
    # Otherwise, read and execute commands from the user
    else:
        print("Enter commands found in README.md. Type 'QUIT' to exit.")
        input_text = input("Enter command >>> ")
        while input_text != "QUIT":
            input_list = parseString(input_text, ' ')
            operation, args = input_list[0], input_list[1:]
            try:
                if operation == "CREATE":
                    tree.create(*args)
                elif operation == "LIST":
                    tree.list()
                elif operation == "MOVE":
                    tree.move(*args)
                elif operation == "DELETE":
                    tree.delete(*args)
                elif operation == "":
                    print("Enter commands found in README.md. Type 'QUIT' to exit.")
                else:
                    raise ValueError(f"Cannot perform command - {operation} does not exist")
            except Exception as e:
                print(e)

            input_text = input("Enter command >>> ")