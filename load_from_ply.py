# so im thinking of a list of lists
# so we get each line, split it by spaces, and then add it to the list
# TODO make it work for ascii files

import numpy as np
import open3d as o3d
import struct



def conditional_cast(type, value):
    if type == 'uchar':
        return int(value)
    if type == 'int':
        return int(value)
    if type == 'float':
        return float(value)
    return value

def parse_header(fin):
    elements = []
    properties = []
    element_index = -1
    property_buffer = []
    for line in fin:
        words = [word for word in line.decode().split()]
        if words[0] == 'element':
            if property_buffer != []:
                properties.append(property_buffer)
            property_buffer = []
            elements.append(words[1])
            elements.append(words[2])
            element_index += 1
        if words[0] == 'property':
            property_buffer.append(words[1:])
        if words[0] == 'end_header':
            properties.append(property_buffer)
            break
    return elements, properties

def parse_ascii(fin):
    graphical_elements = []
    elements, properties = parse_header(fin)
    for x in range(1, len(elements), 2):
        for y in range(int(elements[x])):
            #properties[x-1] holds all the information for parsing the next lines of input
            line = fin.readline()
            words = [word for word in line.split()]
            if properties[int(x/2)][0][0] == 'list':
                graphical_elements.append([conditional_cast(properties[int(x/2)][0][1], word) for word in words[1:]])
            else:
                buffer = []
                counter = 0
                for word in words:
                    buffer.append((conditional_cast(properties[int(x/2)][counter][0], word)))
                    counter += 1
                graphical_elements.append(buffer)
    return graphical_elements

def stringify(properties):
    main_buffer = []
    for prop in properties:
        buffer = ""
        for x in prop:
            if x[0] == 'list':
                buffer += 'list ' + x[1] + ' ' + x[2] + ' '
            if x[0] == 'float':
                buffer += 'f'
            if x[0] == 'int':
                buffer += 'i'
            if x[0] == 'uchar':
                buffer += 'c'
            if x[0] == 'double':
                buffer += 'd'
        main_buffer.append(buffer)
    print(main_buffer)
    return main_buffer

def binary_parse(fin, file_name, endian):
    graphical_elements = []
    elements, properties = parse_header(fin)
    fin.close()
    fin = open(file_name, 'rb')
    for line in fin:
        if line == b'end_header\n':
            break
    stringified_properties = stringify(properties)
    for x in range(1, len(elements), 2):
        for y in range(int(elements[x])):
            #properties[x-1] holds all the information for parsing the next lines of input
            line = fin.read(struct.calcsize(endian + stringified_properties[int(x/2)]))
            words = struct.unpack(endian + stringified_properties[int(x/2)], line)
            graphical_elements.append(words)

    return graphical_elements

def load_from_ply(file_name):
    endian = '='
    fin = open(file_name, 'rb')
    format = fin.readline().decode('utf-8')
    if format != 'ply\n':
        print('Not a ply file')
        return
    type = fin.readline().decode('utf-8')
    if type == 'format binary_little_endian 1.0\n':
        endian = '<'
        graphical_elements =  binary_parse(fin, file_name, endian)
    elif type == 'format binary_big_endian 1.0\n':
        endian = '>'
        graphical_elements =  binary_parse(fin, file_name, endian)
    else:
        graphical_elements =  parse_ascii(fin)
    
    final = np.array(graphical_elements)
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(final)
    return pcd
    fin.close()

