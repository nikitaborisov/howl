#!/usr/bin/python

from datetime import datetime, time, timedelta
from math import ceil, floor
from collections import namedtuple, defaultdict

paces = [timedelta(minutes=6)+timedelta(minutes=1)*i for i in range((20-6))]
loop = 3.29 # miles

start = datetime(2016,8,13,7,30)
end = start + timedelta(hours=8)


def loops(t,p):
    return int(floor((end-t).seconds / p.seconds / loop))

Cutoff = namedtuple('Cutoff',['pace','paceindex','loops'])
cutoffs = defaultdict(list)

for i,p in enumerate(paces):
    for n in range(1,int(ceil(timedelta(hours=8).seconds/p.seconds/loop))):
        t = end-p*loop*n
        t.replace(microsecond=0)
        assert(t >= start)
        cutoffs[t].append(Cutoff(p,i,n))

obs = set({})
for i,p in enumerate(paces):
    for n in range(1,4):
        t = end-p*n
        if t not in cutoffs:
            obs.add(t)


with open("howl.html","w") as outfile:
    print("""
<html lang="en">
<head>
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css" integrity="sha384-rHyoN1iRsVXV4nD0JutlnGaslCJuC7uwjduW9SVrLvRYooPp2bWYgmgJQIXwl/Sp" crossorigin="anonymous">
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>
<title>Howl Times</title>
</head>
<body>
<div class="container-fluid">
<table class="table table-striped table-bordered">
<thead>
<tr>
<th>Time</th>
""", file=outfile)
    for p in paces:
        print("<th>{}</th>".format(str(p)[2:]),file=outfile)
    print("""
    </tr>
    </thead>
    <tbody>
    """,file=outfile)

    for t in [start]+sorted(list(cutoffs.keys())+list(obs)):
        print("<tr><th>{}</th>".format(t.strftime("%H:%M")),file=outfile)
        for i,p in enumerate(paces):
            l = loops(t,p)
            if l:
                if t > start and loops(t+timedelta(minutes=-1),p) > l:
                    print("<td><strong>{}L@{}</strong></td>".format(l,p.seconds//60),file=outfile)
                else:
                    print("<td>{}</td>".format(l),file=outfile)
            else:
                ob = (end-t).seconds / p.seconds
                if ob >= 1:
                    print("<td>{} OB{}</td>".format(int(floor(ob)),"s"*(ob >= 2)),file=outfile)
                else:
                    print("<td></td>",file=outfile)
        print("</tr>",file=outfile)

    print("""
    </table>
    </div>
    </body>
    </html>
    """,file=outfile)
