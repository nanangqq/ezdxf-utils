def filterForms(ents, block_name):
    return [ent for ent in ents if 'block' in dir(ent) and ent.block().name==block_name]

def getFormBB(formInsert):
    
    vertices = []
    for vent in formInsert.virtual_entities():
        if type(vent)==ezdxf.entities.line.Line:
            attrs = vent.dxf.all_existing_dxf_attribs()
            vertices += [attrs['start'], attrs['end']]
        elif type(vent)==ezdxf.entities.lwpolyline.LWPolyline:
            vertices += [v for v in vent.vertices()]
    
    minX, minY = vertices[0][:2]
    maxX, maxY = vertices[0][:2]
    for v in vertices[1:]:
        if v[0]<minX:
            minX = v[0]
        if v[0]>maxX:
            maxX = v[0]
        if v[1]<minY:
            minY = v[1]
        if v[1]>maxY:
            maxY = v[1]
    
    return minX, minY, maxX, maxY


def getSize(bb):
    return {
        'width': int(bb[2]-bb[0]),
        'height': int(bb[3]-bb[1])
    }

def getIntersectingForms(insert, space_map):
    loc = getInsertTextPoint(insert)
    return [bb_id for bb_id in space_map.intersection((loc[0], loc[1], loc[0], loc[1]))]


def getFormDictAndIndex(forms):
    form_dict = {}
    space_map = index.Index()
    for i in range(len(forms)):
        formInsert = forms[i]
        form_dict[i] = formInsert
        space_map.insert(i, getFormBB(formInsert))
    return form_dict, space_map