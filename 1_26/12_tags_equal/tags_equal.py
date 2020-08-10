import shlex


def tags_equal(tag_lst1, tag_lst2):

    to_return = True
    
    final_dicts = []
    
    for tag_lst in [tag_lst1, tag_lst2]:

        tag_lst = tag_lst.replace("<", "")
        tag_lst = tag_lst.replace(">", "")
        tag_lst = shlex.split(tag_lst)
        for i, tag in enumerate(tag_lst):
            tag = tag.replace("\"", "")
            tag = tag.replace("\'", "")
            tag_lst[i] = tag
        keys = []
        vals = []

        for i, tag in enumerate(tag_lst):
            if "=" in tag:
                key, val = tag.split("=")
            else:
                key = tag
                val = "default"

            if key.lower() in keys:
                pass
            else:
                keys.append(key.lower().strip())
                vals.append(val.lower().strip())

        final_dicts.append(dict(zip(keys, vals)))

    for key in final_dicts[0]:
        if key in final_dicts[1] and final_dicts[0][key] == final_dicts[1][key]:
            pass
        else:
            to_return = False
            break

    return to_return
