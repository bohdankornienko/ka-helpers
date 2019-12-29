import json

from itertools import cycle

header = """
<!DOCTYPE html>
<html>
<head>
<style>
table {
    border-collapse: collapse;
    width: 100%;
    margin: 10pt;
}

table, th, td {
    border: 1px solid black;
    padding: 5px;
}

div.date {
    margin-top: 20pt;
    font-weight: bold;
}

div.person {
    background-color: sandybrown;
    margin: 11pt;
    padding: 6pt;
    font-size: larger;
}

</style>
</head>
<body>
"""

bottom = """
</body>
</html>
"""

table_start = ["""<table style="background-color: gainsboro">""",
               """<table style="background-color: silver">"""]
table_start = cycle(table_start)

table_end = """</table>"""


with open('summary.json', 'r') as fp:
    summary = json.load(fp)

html = list()
html.append(header)

row_double_cell = """
  <tr>
    <td colspan="2">{}</td>
  </tr>    
"""

row_two_cells = """
  <tr>
    <td>{}</td>
    <td>{}</td>
  </tr>
"""

person_element = """<div class="person">{}</div>"""

date_element = """<h1>{}</h1><hr>"""

for day, day_summary in summary.items():
    item = date_element.format(day)
    html.append(item)

    for person, persons_summary in day_summary.items():
        item = person_element.format(person)
        html.append(item)

        for translation in persons_summary['translations']:
            html.append(next(table_start))
            item = row_double_cell.format('<b>' + translation['source'] + '</b>')
            html.append(item)

            for suggestion in translation['suggestions']:
                item = row_two_cells.format(
                    suggestion['author'],
                    suggestion['text']
                )
                html.append(item)
            html.append(table_end)

html.append(bottom)

with open("summary.html", 'w') as fp:
    fp.write('\n'.join(html))

print(html)
