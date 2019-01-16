import requests
from pprint import pprint

ka = 'http://khanacademy.org'

topictree = '/api/v1/topictree'

req = '{}{}'.format(ka, topictree)
print('Requesting', req)

r = requests.get(req)

resp = r.json()

def get_section_by_slug(d, slug):
    if d['node_slug'] == slug:
        return d

    if not 'children' in d:
        return None

    for children in d['children']:
        slug_dict = get_section_by_slug(children, slug)
        if slug_dict:
            return slug_dict

    return None


# KA structure tree up to section in each course
for course in resp['children']:
    print('{} [slug: {}]'.format(course['title'], course['slug']))
    print('Sections:')
    for section in course['children']:
        print('\t{} [section slug: {}]'.format(section['title'], section['slug']))
    print()


def extract_video_lengths(d):
#     import ipdb; ipdb.set_trace()
    if not 'children' in d and d['kind'] == 'Video':
        return (d['youtube_id'], d['duration'])

    vids = list()

    for children in d['children']:
        vids.append(extract_video_lengths(children))

    return vids


from collections import deque

def flatten(nested_list):
    res_list = list()
    d = deque()
    for x in nested_list:
        d.append(x)

    while len(d) > 0:
        curr_item = d.popleft()
        if type(curr_item) is list:
            for x in curr_item:
                d.append(x)
        else:
            res_list.append(curr_item)

    return res_list


import datetime

em = get_section_by_slug(resp, 'early-math')
em_vids = extract_video_lengths(em)
em_vids = flatten(em_vids)
em_vids_dict = { v[0] : v[1] for v in em_vids }
em_duration = sum([v for k, v in em_vids_dict.items()])
print(str(datetime.timedelta(seconds=int(em_duration))))

