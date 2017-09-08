from vSearchHelper import *
import heapq
import random
import shutil
from collections import defaultdict

def choose_next_vlistlist_itrRm(result, resultlistdir, vlistdir):
	curr_strategy="Iterative Removal"
	#implement strategy to pick next vlist_curr
	#result will be a list of tuple (vlistname, performance)
	#return a tuple (list of vlistname, list of output prompts)
	highest_roci = max(result, key = lambda x: x[1])
	res = []
	res.append(highest_roci[0])
	printlines = []
	printlines.append("Selected best vlist :" + str(res))

	vlisttitle = res[0].split("-")[0]
	gen = res[0].split("-")[1]
	f = open(resultlistdir + vlisttitle + ".result", "a")	#append plot file for no.var vs benchmark plot
	f.write(vlisttitle + '-' + str(gen) + "," + str(highest_roci[0]) + "," + str(highest_roci[1]) + "\n")
	f.close()
	shutil.copyfile(vlistdir + highest_roci[0], resultlistdir + "best-gen-" + str(gen))

	return (res, printlines)

def genvlist_itrRm(vlist_lines, checkedvlist, vlist_all):
	curr_strategy="Iterative Removal"
	#define stratgy to generate next-gen vlists from a single parent vlist vlist_lines
	#vlist_lines will contain only lines describing vars, excluding header and ampersand line
	#return a tuple (list of varlists, string describing current strategy name)
	out=[]
	for i in range(0,len(vlist_lines)):
		thisfile = []
		for line in range(0,len(vlist_lines)):
			if line != i:
				thisfile.append(vlist_lines[line])
		out.append(thisfile)
	return (out, curr_strategy)



def choose_next_vlistlist_itrAd(result, resultlistdir, vlistdir):
	curr_strategy="Iterative Addition"
	highest_roci = max(result, key = lambda x: x[1])
	res = []
	res.append(highest_roci[0])
	printlines = []
	printlines.append("Selected best vlist :" + str(res))

	vlisttitle = res[0].split("-")[0]
	gen = res[0].split("-")[1]
	f = open(resultlistdir + vlisttitle + ".result", "a")	#append plot file for no.var vs benchmark plot
	f.write(vlisttitle + '-' + str(gen) + "," + str(highest_roci[0]) + "," + str(highest_roci[1]) + "\n")
	f.close()
	shutil.copyfile(vlistdir + highest_roci[0], resultlistdir + "best-gen-" + str(gen))

	return (res, printlines)

def genvlist_itrAd(vlist_lines, checkedvlist, vlist_all):
	curr_strategy="Iterative Addition"
	out=[]
	for line in vlist_all:
		if line in vlist_lines: continue	#already added this line, skip
		thisfile = vlist_lines[:]	#copy			
		thisfile.append(line)
		out.append(thisfile)
	return (out, curr_strategy)


def choose_next_vlistlist_beamSearch(result, resultlistdir, vlistdir):
	curr_strategy="Beam Search"
	width=10	#define beam width
	res = heapq.nlargest(width, result, key = lambda x: x[1])
	selectvlist = [i for (i,j) in res]
	bestvlist = max(res, key = lambda x: x[1])
	printlines = []
	printlines.append("Selected vlist :" + str(selectvlist))
	printlines.append("Best for this generation :" + str(bestvlist))

	vlisttitle = bestvlist[0].split("-")[0]
	gen = bestvlist[0].split("-")[1]
	f = open(resultlistdir + vlisttitle + ".result", "a")	#append plot file for no.var vs benchmark plot
	f.write(vlisttitle + '-' + str(gen) + "," + str(bestvlist[0]) + "," + str(bestvlist[1]) + "\n")
	f.close()
	shutil.copyfile(vlistdir + bestvlist[0], resultlistdir + "best-gen-" + str(gen))

	return (selectvlist, printlines)



def genvlist_beamSearch(vlist_lines, checkedvlist, vlist_all):
	curr_strategy="Beam Search"
	out=[]
	for i in range(0,len(vlist_lines)):
		thisfile = []
		for line in range(0,len(vlist_lines)):
			if line != i:
				thisfile.append(vlist_lines[line])
		if list2vec(thisfile, vlist_all) in checkedvlist:	continue	#won't check checked combination
		out.append(thisfile)
	return (out, curr_strategy)




def choose_next_vlistlist_rdmWalk(result, resultlistdir, vlistdir):
	width = 1	#define how many vlists are selected to be next gen parent vlist
	printlines = []
	d = defaultdict(list)
	bestineachnvar = []

	for (vlist, perf) in result:	
		d[vlist.split("-")[3]].append((vlist, perf))
	f = open(resultlistdir + "roc.result", "r")
	flines = f.readlines()
	f.close()
	flines = [(line.split(",")[0], line.split(",")[1],float(line.split(",")[-1])) for line in flines]
	for nvar, vlisttuplelist in d.iteritems():
		genbestperf = [(sr,perf) for (vl, sr, perf) in flines if vl == ("nvar-" + str(nvar))][0]
		bestvlist = max(vlisttuplelist, key = lambda x: x[1])
		bestineachnvar.append((bestvlist[0], bestvlist[1]-genbestperf[1]))
		if bestvlist[1] > genbestperf[1]:
			printlines.append("Performance for nvar = " + str(nvar) + " is improved from " + str(genbestperf) + " to " + str(bestvlist))
			shutil.copyfile(vlistdir + bestvlist[0], resultlistdir + "best-gen-" + str(nvar))			
			flines[int(nvar)-1] = ("nvar-" + str(nvar),bestvlist[0],bestvlist[1])
		else:
			printlines.append("No performance improvement for nvar = " + str(nvar))
		vlisttuplelist = [(vlist, perf-genbestperf[1]) for (vlist,perf) in vlisttuplelist]
		d[nvar] = vlisttuplelist
	flines = [vl + "," + sr + "," + str(perf) for (vl, sr, perf) in flines]
	f = open(resultlistdir + "roc.result", "w")
	for l in flines:	f.write(l + "\n")
	f.close()	
	
	#flat_list = [item for sublist in d.values() for item in sublist]
	res = heapq.nlargest(width, bestineachnvar, key = lambda x: x[1])
	selectvlist = [i for (i,j) in res]
	printlines.append("Selected vlist :" + str(selectvlist))

	return (selectvlist, printlines)
		
			

def genvlist_rdmWalk(vlist_lines, checkedvlist, vlist_all):
	width = 100	#how many random children is generated from one parent
	nvarlimit = (4, 12)
	curr_strategy="Random Walk"
	out=[]
	vec = list2vec(vlist_lines, vlist_all)
	childid = 0
	j = 0
	random.seed()
	while (childid<width):
		if j >width: break
		admissibleTweakFlag = False
		while(admissibleTweakFlag == False):
			nflips = 1 + rdm([70,50,40,30,10,10,10,10])	#define PDF for no. of flips
			chosen = random.sample(range(len(vlist_all)), nflips)
			flippedvec = [i ^ (inx in chosen) for inx, i in enumerate(vec)]
			if flippedvec.count(1) >= nvarlimit[0] and flippedvec.count(1) <= nvarlimit[1]:
				admissibleTweakFlag = True
		if tuple(flippedvec) in checkedvlist:	
			j += 1
			continue	#won't check checked combination
		out.append(vec2list(flippedvec, vlist_all))
		childid += 1
	return (out, curr_strategy)


def check_benchmark_roc(rf):
	roc = rf.Get("Method_BDT/BDT/MVA_BDT_rejBvsS")
	roci = roc.Integral()
	if roci < 0.5: # impossible, file error
		return -1
	else:
		return roci

