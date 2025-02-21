from directories import parseString, Tree
import pytest


def test_parse_string():
    path = "fruits/apples/fuji"
    parts = parseString(path, '/')
    assert parts == ["fruits", "apples", "fuji"]

    path = "fruits"
    parts = parseString(path, '/')
    assert parts == ["fruits"]

    path = "fruits/apples"
    parts = parseString(path, '/')
    assert parts == ["fruits", "apples"]

    path = "fruits/apples/fuji/gala"
    parts = parseString(path, ':')
    assert parts == [path]

    path = ""
    parts = parseString(path, '/')
    assert parts == [path]

def test_tree_constructor():
    tree = Tree()
    assert len(tree.tree) == 0

def test_create_one_directory(capsys):
    tree = Tree()
    directory = "fruits"
    tree.create(directory)
    
    assert directory in tree.tree
    assert len(tree.tree) == 1
    
    captured = capsys.readouterr()
    assert captured.out == f"CREATE {directory}\n"
    assert captured.err == ""

def test_create_multiple_directories(capsys):
    directories = ["fruits", "vegetables", "grains"]

    tree = Tree()
    actual_ouput = ""
    for directory in directories:
        tree.create(directory)

        actual_ouput += f"CREATE {directory}\n"
        assert directory in tree.tree
        assert len(tree.tree[directory]) == 0


    assert len(tree.tree) == len(directories)

    captured = capsys.readouterr()
    assert captured.out == actual_ouput
    assert captured.err == ""

def test_create_nested_directories(capsys):
    parent = "fruits"
    child = "apples"
    directory = f"{parent}/{child}"

    tree = Tree()
    tree.create(directory)
    

    assert parent in tree.tree
    assert child not in tree.tree
    assert child in tree.tree[parent]

    assert len(tree.tree) == 1
    assert len(tree.tree[parent]) == 1
    assert len(tree.tree[parent][child]) == 0

    captured = capsys.readouterr()
    assert captured.out == f"CREATE {directory}\n"
    assert captured.err == ""

def test_create_nested_directories_iteratively(capsys):
    grandparent = "fruits"
    parent = "apples"
    child = "fuji"

    tree = Tree()
    path = ""
    actual_output = ""
    for directory in [grandparent, parent, child]:
        if len(path) > 0:
            path += "/"

        path += f"{directory}"
        tree.create(path)
        actual_output += f"CREATE {path}\n"


    assert grandparent in tree.tree
    assert parent not in tree.tree
    assert parent in tree.tree[grandparent]
    assert child not in tree.tree
    assert child not in tree.tree[grandparent]
    assert child in tree.tree[grandparent][parent]

    assert len(tree.tree) == 1
    assert len(tree.tree[grandparent]) == 1
    assert len(tree.tree[grandparent][parent]) == 1
    assert len(tree.tree[grandparent][parent][child]) == 0

    captured = capsys.readouterr()
    assert captured.out == actual_output
    assert captured.err == ""

def test_list_one_level(capsys):
    directories = ["fruits", "vegetables", "grains"]

    tree = Tree()
    actual_ouput = ""
    for directory in directories:
        tree.create(directory)

        actual_ouput += f"CREATE {directory}\n"
        assert directory in tree.tree
        assert len(tree.tree[directory]) == 0

    assert len(tree.tree) == len(directories)

    tree.list()

    actual_ouput += "LIST\n"
    for directory in sorted(directories):
        actual_ouput += f"{directory}\n"
   
    captured = capsys.readouterr()
    assert captured.out == actual_ouput
    assert captured.err == ""

def test_list_multiple_levels(capsys):
    grandparent = "fruits"
    parent = "apples"
    child = "fuji"

    tree = Tree()
    path = ""
    actual_output = ""
    for directory in [grandparent, parent, child]:
        if len(path) > 0:
            path += "/"

        path += f"{directory}"
        tree.create(path)
        actual_output += f"CREATE {path}\n"

    assert grandparent in tree.tree
    assert parent not in tree.tree
    assert parent in tree.tree[grandparent]
    assert child not in tree.tree
    assert child not in tree.tree[grandparent]
    assert child in tree.tree[grandparent][parent]
    assert len(tree.tree) == 1
    assert len(tree.tree[grandparent]) == 1
    assert len(tree.tree[grandparent][parent]) == 1
    assert len(tree.tree[grandparent][parent][child]) == 0

    tree.list()
    actual_output += "LIST\n"
    for count, directory in enumerate([grandparent, parent, child]):
        actual_output += f"{'  '*(count)}{directory}\n"

    captured = capsys.readouterr()
    assert captured.out == actual_output
    assert captured.err == ""

def test_list_varied_levels(capsys):
    level_one_directories = ["fruits", "vegetables", "grains"]
    grandparent = level_one_directories[0]
    parent = "apples"
    child = "fuji"

    tree = Tree()
    actual_output = ""
    for directory in level_one_directories:
        tree.create(directory)
        actual_output += f"CREATE {directory}\n"
        assert directory in tree.tree
        assert len(tree.tree[directory]) == 0
    
    path = grandparent
    for directory in [parent, child]:
        path += f"/{directory}"
        tree.create(path)
        actual_output += f"CREATE {path}\n"
    
    assert parent in tree.tree[grandparent]
    assert child in tree.tree[grandparent][parent]
    assert len(tree.tree) == len(level_one_directories)
    assert len(tree.tree[grandparent]) == 1
    assert len(tree.tree[grandparent][parent]) == 1
    assert len(tree.tree[grandparent][parent][child]) == 0

    tree.list()

    actual_output += "LIST\n"
    for directory in sorted(level_one_directories):
        actual_output += f"{directory}\n"

        if directory == grandparent:
            for count, subdirectory in enumerate([parent, child]):
                actual_output += f"{"  "*(count+1)}{subdirectory}\n"

    captured = capsys.readouterr()
    assert captured.out == actual_output
    assert captured.err == ""

def test_move_simple(capsys):
    directories = ["fruits", "apples"]
    tree = Tree()
    
    actual_output = ""
    for directory in directories:
        tree.create(directory)
        actual_output += f"CREATE {directory}\n"
        assert directory in tree.tree
        assert len(tree.tree[directory]) == 0

    assert len(tree.tree) == len(directories)

    tree.move(directories[1], directories[0])
    actual_output += f"MOVE {directories[1]} {directories[0]}\n"

    assert directories[1] not in tree.tree
    assert directories[1] in tree.tree[directories[0]]

    captured = capsys.readouterr()
    assert captured.out == actual_output
    assert captured.err == ""

def test_move_nested(capsys):
    level_one_directories = ["fruits", "vegetables", "grains"]
    grandparent = level_one_directories[0]
    parent = "apples"
    child = "fuji"

    tree = Tree()
    actual_output = ""
    for directory in level_one_directories:
        tree.create(directory)
        actual_output += f"CREATE {directory}\n"
        assert directory in tree.tree
        assert len(tree.tree[directory]) == 0
    
    path = grandparent
    for directory in [parent, child]:
        path += f"/{directory}"
        tree.create(path)
        actual_output += f"CREATE {path}\n"
    
    assert parent in tree.tree[grandparent]
    assert child in tree.tree[grandparent][parent]
    assert len(tree.tree) == len(level_one_directories)
    assert len(tree.tree[grandparent]) == 1
    assert len(tree.tree[grandparent][parent]) == 1
    assert len(tree.tree[grandparent][parent][child]) == 0

    tree.move(f"{grandparent}/{parent}", level_one_directories[1])
    actual_output += f"MOVE {grandparent}/{parent} {level_one_directories[1]}\n"

    assert parent not in tree.tree[grandparent]
    assert parent in tree.tree[level_one_directories[1]]
    assert child in tree.tree[level_one_directories[1]][parent]

    captured = capsys.readouterr()
    assert captured.out == actual_output
    assert captured.err == ""

def test_delete_simple(capsys):
    directory = "fruits"
    tree = Tree()
    actual_output = ""
    tree.create(directory)
    actual_output += f"CREATE {directory}\n"
    
    assert directory in tree.tree
    assert len(tree.tree) == 1

    tree.delete(directory)
    actual_output += f"DELETE {directory}\n"

    assert directory not in tree.tree
    assert len(tree.tree) == 0

    captured = capsys.readouterr()
    assert captured.out == actual_output
    assert captured.err == ""

def test_delete_within_nested(capsys):
    grandparent = "fruits"
    parent = "apples"
    child = "fuji"

    tree = Tree()
    actual_output = ""
    path = ""
    for directory in [grandparent, parent, child]:
        if len(path) > 0:
            path += "/"

        path += f"{directory}"
        tree.create(path)
        actual_output += f"CREATE {path}\n"

    assert grandparent in tree.tree
    assert parent not in tree.tree
    assert parent in tree.tree[grandparent]
    assert child not in tree.tree
    assert child not in tree.tree[grandparent]
    assert child in tree.tree[grandparent][parent]
    assert len(tree.tree) == 1
    assert len(tree.tree[grandparent]) == 1
    assert len(tree.tree[grandparent][parent]) == 1
    assert len(tree.tree[grandparent][parent][child]) == 0

    tree.delete(f"{grandparent}/{parent}/{child}")
    actual_output += f"DELETE {grandparent}/{parent}/{child}\n"

    assert grandparent in tree.tree
    assert parent not in tree.tree
    assert parent in tree.tree[grandparent]
    assert child not in tree.tree
    assert child not in tree.tree[grandparent]
    assert child not in tree.tree[grandparent][parent]
    assert len(tree.tree) == 1
    assert len(tree.tree[grandparent]) == 1
    assert len(tree.tree[grandparent][parent]) == 0

    captured = capsys.readouterr()
    assert captured.out == actual_output
    assert captured.err == ""

def test_delete_nested(capsys):
    grandparent = "fruits"
    parent = "apples"
    child = "fuji"

    tree = Tree()
    actual_output = ""
    path = ""
    for directory in [grandparent, parent, child]:
        if len(path) > 0:
            path += "/"

        path += f"{directory}"
        tree.create(path)
        actual_output += f"CREATE {path}\n"

    assert grandparent in tree.tree
    assert parent not in tree.tree
    assert parent in tree.tree[grandparent]
    assert child not in tree.tree
    assert child not in tree.tree[grandparent]
    assert child in tree.tree[grandparent][parent]
    assert len(tree.tree) == 1
    assert len(tree.tree[grandparent]) == 1
    assert len(tree.tree[grandparent][parent]) == 1
    assert len(tree.tree[grandparent][parent][child]) == 0

    tree.delete(grandparent)
    actual_output += f"DELETE {grandparent}\n"

    assert len(tree.tree) == 0
    assert grandparent not in tree.tree
    assert parent not in tree.tree
    assert child not in tree.tree

    captured = capsys.readouterr()
    assert captured.out == actual_output
    assert captured.err == ""

def test_delete_nonexistent(capsys):
    tree = Tree()
    directory = "fruits"
    tree.create(directory)
    actual_output = f"CREATE {directory}\n"

    nonexistent_directory = "apples"
    with pytest.raises(LookupError):
        tree.delete(f"{directory}/{nonexistent_directory}")
    
    actual_output += f"DELETE {directory}/{nonexistent_directory}\n"
  
    captured = capsys.readouterr()
    assert captured.out == actual_output
    assert captured.err == ""
