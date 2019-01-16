import requests
import datetime
import argparse

from collections import deque

def get_topic_tree():
    """
    Aquire entire topic tree for Khan Academy
    """
    ka = 'http://khanacademy.org'
    topictree = '/api/v1/topictree'

    req = '{}{}'.format(ka, topictree)

    r = requests.get(req)

    resp = r.json()

    return resp

def get_section_by_slug(d, slug):
    """
    Returns sub-dict for specified slug.
    """
    if d['slug'] == slug:
        return d

    if not 'children' in d:
        return None

    for children in d['children']:
        slug_dict = get_section_by_slug(children, slug)
        if slug_dict:
            return slug_dict

    return None

def display_high_level_tree(topictree):
    # KA structure tree up to section in each course
    for course in topictree['children']:
        print('{} [slug: {}]'.format(course['title'], course['slug']))
        print('Sections:')
        for section in course['children']:
            print('\t{} [section slug: {}]'.format(section['title'], section['slug']))
        print()


def extract_video_lengths(d):
    if not 'children' in d and d['kind'] == 'Video':
        return (d['youtube_id'], d['duration'])

    vids = list()

    for children in d['children']:
        vids.append(extract_video_lengths(children))

    return vids



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

def main():
    parser = argparse.ArgumentParser(
        description="Unitility for estimating amount of time for particular "\
                    "topic tree. Running script without arguments will "\
                    "trigger printing topictree")
    parser.add_argument("--slug", help="Slug for the section for which the amount of time has to be calculated")
    args = parser.parse_args()

    print("Requesting topic tree...")
    topictree = get_topic_tree()
    print("Requesting complete.")


    if args.slug:
        em = get_section_by_slug(topictree, args.slug)
        if not em:
            print('We was not able to locate slug: {}'.format(args.slug))
            print('Exiting...')
            exit(1)

        print('Estimating time for {}'.format(em['title']))

        em_vids = extract_video_lengths(em)
        em_vids = flatten(em_vids)
        em_vids_dict = { v[0] : v[1] for v in em_vids }
        em_duration = sum([v for k, v in em_vids_dict.items()])
        print('The secton last: {}'.format(str(datetime.timedelta(seconds=int(em_duration)))))

    else:
        display_high_level_tree(topictree)


if __name__ == "__main__":
    main()
