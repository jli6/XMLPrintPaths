# You can also use xml.etree.ElementTree, which is slower but worth a try if the below import doesn't work on
# your computer.
import xml.etree.cElementTree as ET


def traverse_xmltree(root):
    """
    Perform a preorder tree traversal to compute the paths of all the elements in the XML file.
    :param root: the root to start at
    :return: the paths of every element at or below the root, as a list of tuples
    """

    # Stores the results of the recursive calls, for later processing.
    # Each element of this list is a tuple of the form (path, is_text).
    # path is a string representing the path from input root to some element.
    # is_text is a boolean representing whether it's actually a path or just an element's tag and text.
    # The boolean is necessary for keeping track of things. If we didn't have the special case for
    # printing an element's tag and text, we wouldn't need the boolean.
    child_traversals = list()

    # If the element is a "text" element, print the tag and text.
    # This is distinct from a path, and we don't want to recurse here.
    for child in root:
        if child.text:
            textline = '>>' + child.tag + '"' + child.text + '"'
            child_traversals.append((textline, True))
    # For all elements (including the text elements we just saw before), compute their paths.
    for child in root:
        child_traversals.extend(traverse_xmltree(child))

    # The recursive calls earlier have computed paths that are all missing the input root.
    # We need to add the input root to all of these paths (but not the tag and text lines).
    pathed_child_traversals = list()
    for elem in child_traversals:
        if not elem[1]:
            pathed_child_traversals.append( (root.tag + "\\" + elem[0], False) )
        else:
            pathed_child_traversals.append(elem)

    # In a preorder traversal, the root comes first, followed by the results of the children.
    output = list()
    output.append((root.tag, False))
    output.extend(pathed_child_traversals)  # use extend() to ensure we don't have nested lists
    return output


if __name__ == "__main__":
    # Replace filepath with the path to your XML file. Because ElementTree doesn't work well with namespaces,
    # your XML file should not have XML namespaces in it.
    filepath = "workspace.xml"
    tree = ET.parse(filepath)
    root = tree.getroot()

    # Perform the tree traversal of the XML file.
    log = traverse_xmltree(root)

    # We need to process the results of the traversal. Doing this is a matter of extracting the path information from
    # the (path, is_text) tuples. These are not actual variable names but do describe the tuples.
    # We check the boolean is_text (again, not an actual variable name) and process the tuple slightly
    # differently than in the general case involving full paths.
    log2 = list()
    for elem in log:
        if not elem[1]:
            log2.append("\\\\" + elem[0])
        else:
            log2.append(elem[0])

    # Write the paths to a text file
    with open('pathlog.txt', 'w') as pathlog:
        pathlog.write("\n".join(log2))
