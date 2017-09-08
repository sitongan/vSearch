

__author__ = "Sitong An <sitong.an@desy.de>"


import ROOT
import array
import math

def main():


	f = open("baseline.result","r")
	baselines = f.readlines()
	f.close()
	baselines = [line.split(",") for line in baselines]

	(nvar, tauc_avg, tauc_error) = zip(*baselines)


	nvar = [int(i) for i in nvar]
	tauc_avg = [float(i) for i in tauc_avg]
	tauc_error = [float(i) for i in tauc_error]
	max_n_var=len(nvar)


	
	leg= ROOT.TLegend(0.5, 0.2, 0.8, 0.35)
	leg.SetBorderSize(0)
	leg.SetFillColor(0)
	leg.SetTextSize(0.025)
	leg.SetTextFont(42)

	x = array.array('f',range(1,max_n_var+1))
	y = array.array('f',tauc_avg)
	ye = array.array('f', tauc_error)
	xe = array.array('f', [0]*max_n_var)
	gr = ROOT.TGraphErrors(max_n_var, x, y,xe, ye)
	gr.SetMarkerColor(38)
	gr.SetLineColor(38)
	gr.SetMarkerStyle(20)
	gr.SetTitle("ROC Integral vs No. of Variables")
	gr.GetXaxis().SetTitle("No. of Training Variables")
	gr.GetYaxis().SetTitle("Relative Performance (AUROC)")
	leg.AddEntry(gr, "#splitline{Reference Baseline}{(Randomly selected variable sets as basis of comparison)}", "p")


	f = open("roc-tmva.result", "r")
	lines = f.readlines()
	f.close()
	blabel = [float((l.split(",")[0]).split("-")[-1]) for l in lines]
	bdata = [float((l.split(",")[-1])) for l in lines]
	x2 = array.array('f', blabel)
	y2 = array.array('f', bdata)
	d = dict()

	gr4 = plot_file("roc-tmva.result", 813, 813)
	gr9 = plot_file("itrRm.result",905,905)

	
	c1 = ROOT.TCanvas("c1", "Relative Performance (AUROC) vs No. of Training Variables", 950, 600)	
	gr.Draw("APL")

	gr4.Draw("PL")
	leg.AddEntry(gr4, "#splitline{TMVA out-of-the-box Ranking}{(Performance of top N vars as ranked by TMVA)}", "p")	
	leg.AddEntry(gr9, "#splitline{Iterative Removal - vSearch}{(Removing var with least impact on performance iteratively)}", "p")







	leg.Draw()
	
	print "press enter to continue\n"
	raw_input()
	
def plot_file(filen, markercolor, linecolor, xfixed=0, markerstyle=20):
	f = open(filen, "r")
	lines = f.readlines()
	f.close()
	label = [float((l.split(",")[0]).split("-")[-1]) for l in lines]
	data = [float((l.split(",")[-1])) for l in lines]
	#print label
	#print data

	if xfixed: x2 = array.array('f', [float(xfixed)]*len(data))
	else:	x2 = array.array('f', label)
	y2 = array.array('f', data)
	print x2

	gr3 = ROOT.TGraph(len(label), x2, y2)
	gr3.SetMarkerColor(markercolor)
	gr3.SetLineColor(linecolor)
	gr3.SetMarkerStyle(markerstyle)

	return gr3





if __name__ == '__main__':
	main()
