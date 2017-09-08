import random

def file2list(fname):
	#open a varlist, return list of variables only, excluding header and ampersand line
	f = open(fname, "r")
	vlist = f.readlines()
	f.close()
	endline = next((i for i, x in enumerate(vlist) if x == "&\n"),len(vlist))
	vlist = vlist[1:endline]
	return vlist

def list2vec(vlist, vlist_all):
	try:
		vec = [0] * len(vlist_all)
		for v in vlist:
			vec[vlist_all.index(v)]=1
		return tuple(vec)
	except ValueError:
		print "vSearch : Critical error converting varlist to vector representation"
		print "vSearch : Please make sure all variables in all variable lists are included in the mother list"
		exit(1)

def vec2list(vec, vlist_all):
	return [i for (inx,i) in enumerate(vlist_all) if vec[inx] == 1]

def rdm(weights):
    cdf = []
    total = 0

    for w in weights:
        total += w
        cdf.append(total)

    rnd = random.random() * total
    for i, total in enumerate(cdf):
        if rnd < total:
            return i

