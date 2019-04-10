import xml.etree.cElementTree as ET

def traverse_xmltree(root):
    # preorder
    # child_traversals = [traverse_xmltree(child) for child in root]
    child_traversals = list()
    for child in root:
        if child.text:
            textline = '>>' + child.tag + '"' + child.text + '"'
            child_traversals.append( (textline, True) )
    for child in root:
        child_traversals.extend(traverse_xmltree(child))
    # pathed_child_traversals = [root.tag + "\\" + elem for elem in child_traversals]
    pathed_child_traversals = list()
    for elem in child_traversals:
        if not elem[1]:
            pathed_child_traversals.append( (root.tag + "\\" + elem[0], False) )
        else:
            pathed_child_traversals.append(elem)
    output = list()

    # the tuple format is: (node.tag, nodeIsText).
    # This helps us at the very end when we need to add >> or \\ in the front.
    # if root.text:
    #     output.append( (root.tag, True) )
    # else:
    #     output.append( (root.tag, False) )

    output.append( (root.tag, False) )
    output.extend(pathed_child_traversals)
    return output


if __name__ == "__main__":
    # using actual recursion
    filepath = "../cleanfile.xml"
    tree = ET.parse(filepath)
    root = tree.getroot()

    log = traverse_xmltree(root)

    # log2 = [elem[0] for elem in log]
    log2 = list()
    for elem in log:
        if not elem[1]:
            log2.append("\\\\" + elem[0])
        else:
            log2.append(elem[0])

    with open('Pathlog.txt', 'w') as pathlog:
        pathlog.write("\n".join(log2))
