import hepdata_lib
from hepdata_lib import Submission
submission = Submission()
from hepdata_lib import Table
import ROOT







def makeHeshy(filename,FigName):
    table = Table("Fig"+FigName)
    table.keywords["observables"] = [filename]
    table.keywords["reactions"] = ["P P -->  ZZ --> 4l"]
    from hepdata_lib import Variable, Uncertainty
    f=ROOT.TFile(filename+".root")
    
    c=ROOT.TCanvas()
    c=f.Get("c1")
    #obj = c.GetPrimitive(filename)
    data=c.GetPrimitive("TMultiGraph")
      
    namearr=[]
    fnew=ROOT.TFile("hig-19-009/tmp.root","recreate")
    k=0
    for i in obj.GetHists():
        if i.InheritsFrom("TH1") :
            fnew.cd()
            i.Write()
            namearr.append(i.GetName())
            if k==0:
               hdata=ROOT.TH1F("data","",i.GetNbinsX(),i.GetXaxis().GetXmin(),i.GetXaxis().GetXmax())
               for m in range(1,data.GetN()):
                 hdata.Fill(data.GetPointX(m),data.GetPointY(m))
               fnew.cd()
               hdata.Write()  
               namearr.append("data")
            k=k+1
    fnew.Close()
    from hepdata_lib import RootFileReader
    reader = RootFileReader("hig-19-009/tmp.root")
    k=0
    for j in namearr:
        zx = reader.read_hist_1d(j) 
        if k==0 : 
            v1 = Variable(filename, is_independent=True, is_binned=False, units="")
            v1.values = zx["x"]
            table.add_variable(v1)
        jname = j.replace('ffH','Total') 
        jname = jname.replace('VVH','VBF+VH') 
        jname = jname.replace(filename+"_",'') 
        v2 = Variable(jname, is_independent=False, is_binned=False, units="")
        v2.values = zx["y"]
        table.add_variable(v2)
        k=k+1
#    data=reader.read_("data")
#    v2 = Variable("Data", is_independent=False, is_binned=False, units="")
#    v2.values = data["y"]
#    table.add_variable(v2)
    table.add_image("hig-19-009/Figure_"+FigName+".pdf")
    return table


def makeTable(filename,FigName,obsName,pref):

	table = Table("Fig"+FigName)
	table.keywords["observables"] = [obsName]
	table.keywords["reactions"] = ["P P -->  ZZ --> 4l"]
	
	from hepdata_lib import RootFileReader
	
	reader = RootFileReader("hig-19-009/"+filename)
	zx = reader.read_hist_1d("hzx")
	qqzz = reader.read_hist_1d("hqqzz")
	Higgs = reader.read_hist_1d("hHiggs")
	Higgs0p = reader.read_hist_1d("hHiggs0p")
	Higgs0m = reader.read_hist_1d("hHiggs0m")
	data = reader.read_hist_1d("hdata")
	
	from hepdata_lib import Variable, Uncertainty
	
	v1 = Variable(obsName, is_independent=True, is_binned=False, units="")
	v1.values = zx["x"]
	
	v2 = Variable("ZX", is_independent=False, is_binned=False, units="")
	v2.values = zx["y"]
	
	v3 = Variable("ZZ/Z"r"\gamma", is_independent=False, is_binned=False, units="")
	v3.values = qqzz["y"]

	v7 = Variable("H other", is_independent=False, is_binned=False, units="")
	v7.values = Higgs["y"]
	v4 = Variable(pref+" SM", is_independent=False, is_binned=False, units="")
	v4.values = Higgs0p["y"]
	v5 = Variable(pref+" 0-", is_independent=False, is_binned=False, units="")
	v5.values = Higgs0m["y"]
	v6 = Variable("Data", is_independent=False, is_binned=False, units="")
	v6.values = data["y"]
	
	table.add_variable(v1)
	table.add_variable(v2)
	table.add_variable(v3)
	table.add_variable(v7)
	table.add_variable(v4)
	table.add_variable(v5)
	table.add_variable(v6)
	table.add_image("hig-19-009/Figure_"+FigName+".pdf")
	return table
	
def makelike(filename,FigName,v1name,v2name):
	table = Table("Fig"+FigName)
	table.keywords["observables"] = [v1name, v2name, r'$-2 \Delta ln L$']
	table.keywords["reactions"] = ["P P -->  ZZ --> 4l"]
	
	from hepdata_lib import RootFileReader
	
	reader = RootFileReader(filename)
	lik = reader.read_hist_2d("Graph2D")
	lik.keys()
	
	from hepdata_lib import Variable, Uncertainty
	
	v1 = Variable(v1name, is_independent=True, is_binned=False, units="")
	v1.values = lik["x"]
	
	v2 = Variable(v2name, is_independent=True, is_binned=False, units="")
	v2.values = lik["y"]
	
	v3 = Variable(r"$-2\Delta ln L$", is_independent=False, is_binned=False, units="")
	v3.values = lik["z"]
	
	table.add_variable(v1)
	table.add_variable(v2)
	table.add_variable(v3)
	table.add_image("paper/HIG-19-009/Figure_"+FigName+".pdf")
	return table

def makegraph(filename,FigName,obsName,v1,v2,v3,v4):
        table = Table("Fig"+FigName)
        table.keywords["observables"] = [obsName]
        table.keywords["reactions"] = ["P P -->  ZZ --> 4l"]
    

        import numpy as np

        data = np.loadtxt(filename)

        from hepdata_lib import Variable, Uncertainty
        d = Variable(obsName, is_independent=True, is_binned=False, units="")
        d.values = data[0]
        print (data[0])
        obs = Variable(v1, is_independent=False, is_binned=False, units="")
        obs.values = data[1]
        obs.add_qualifier("-2 Delta Log Likelihood", "Observed")

        exp = Variable(v2, is_independent=False, is_binned=False, units="")
        exp.values = data[2]
        exp.add_qualifier("-2 Delta Log Likelihood", "Expected")

        #       from hepdata_lib.c_file_reader import CFileReader
        #       c_file = "hig-19-009/scan_kappa.C"
        #       reader = CFileReader(c_file) 
        #       graphs = reader.get_graphs()
        #
        #
        if v2 != "":
                gg_obs = Variable(v1, is_independent=False, is_binned=False, units="")
                gg_obs.values = data[1] 
                gg_obs.add_qualifier("-2 Delta Log Likelihood", "Observed, fix others")

                gg_exp = Variable(v2, is_independent=False, is_binned=False, units="")
                gg_exp.values = data[2] 
                gg_exp.add_qualifier("-2 Delta Log Likelihood", "Expected, fix others")

                fl_obs = Variable(v3, is_independent=False, is_binned=False, units="")
                fl_obs.values = data[3] 
                fl_obs.add_qualifier("-2 Delta Log Likelihood", "Observed, float others")

                fl_exp = Variable(v4, is_independent=False, is_binned=False, units="")
                fl_exp.values = data[4] 
                fl_exp.add_qualifier("-2 Delta Log Likelihood", "Expected, float others")
 
        table.add_variable(d)
        if v2 != "":
            table.add_variable(gg_obs)
            table.add_variable(gg_exp)
            table.add_variable(fl_obs)
            table.add_variable(fl_exp)
        else :         
            table.add_variable(obs)
            table.add_variable(exp)

        table.add_image("paper/HIG-19-009/Figure_"+FigName+".pdf")
        return table

if __name__ == "__main__":
    submission.add_link("Webpage with all figures and tables", "https://cms-results.web.cern.ch/cms-results/public-results/publications/HIG-19-009/")
    submission.add_link("arXiv", "http://arxiv.org/abs/arXiv:2104.12152")
    submission.add_record_id(1860903, "inspire")
    #$\delta c_z$, $c_{zz}$, $c_{z \Box}$, and $\tilde c_{zz}$ with the $c_{gg}$ and $\tilde c_{gg}$  
    disname=["test"]
    rootname=["output_ctzczb.root","output_ctzcz.root","output_ctzdz.root","output_czczb.root","output_dzczb.root","output_dzcz.root"]
    #for i,l in enumerate(rootname):
    table_test =makelike("./SMEFT/2Dci_scans/"+rootname[0],"022-e",r"$c_{z \Box}$",r"$\tilde c_{zz}$")
    submission.add_table(table_test)
    table_test =makelike("./SMEFT/2Dci_scans/"+rootname[1],"022-d",r"$c_{zz}$",r"$\tilde c_{zz}$")
    submission.add_table(table_test)
    table_test =makelike("./SMEFT/2Dci_scans/"+rootname[2],"022-a",r"$\delta c_z$",r"$\tilde c_{zz}$")
    submission.add_table(table_test)
    table_test =makelike("./SMEFT/2Dci_scans/"+rootname[3],"022-f",r"$c_{z \Box}$",r"$c_{zz}$")
    submission.add_table(table_test)
    table_test =makelike("./SMEFT/2Dci_scans/"+rootname[4],"022-c",r"$\delta c_z$",r"$c_{z \Box}$")
    submission.add_table(table_test)
    table_test =makelike("./SMEFT/2Dci_scans/"+rootname[5],"022-b",r"$\delta c_z$",r"$c_{zz}$")
    submission.add_table(table_test)

    table_test = makegraph("./SMEFT/input_ci_scans/output_dz.txt","021-a",r"$\delta c_z$","Observed","","","")
    submission.add_table(table_test)
    table_test = makegraph("./SMEFT/input_ci_scans/output_czz.txt","021-b",r"$c_{zz}$","Observed","","","")
    submission.add_table(table_test)
    table_test = makegraph("./SMEFT/input_ci_scans/output_czb.txt","021-c",r"$c_{z \Box}$","Observed","","","")
    submission.add_table(table_test)
    table_test = makegraph("./SMEFT/input_ci_scans/output_ctz.txt","021-d",r"$\tilde c_{zz}$","Observed","","","")
    submission.add_table(table_test)
    

    table_test = makegraph("./SMEFT/fai1d/output_fa3.txt","020-a",r"$f_{a3}$","Observed, fix others","Expected, fix other","Observed, float others","Expected, float others")
    submission.add_table(table_test)
    table_test = makegraph("./SMEFT/fai1d/output_fa2.txt","020-b",r"$f_{a2}$","Observed, fix others","Expected, fix other","Observed, float others","Expected, float others")
    submission.add_table(table_test)
    table_test = makegraph("./SMEFT/fai1d/output_fL1.txt","020-c",r"$f_{\Lambda1}$","Observed, fix others","Expected, fix other","Observed, float others","Expected, float others")
    submission.add_table(table_test)


    
    table_test = makegraph("./NonSMEFT/fai1d/output_fa3.txt","018-a",r"$f_{a3}$","Observed, fix others","Expected, fix other","Observed, float others","Expected, float others")
    submission.add_table(table_test)
    table_test = makegraph("./NonSMEFT/fai1d/output_fa2.txt","018-b",r"$f_{a2}$","Observed, fix others","Expected, fix other","Observed, float others","Expected, float others")
    submission.add_table(table_test)
    table_test = makegraph("./NonSMEFT/fai1d/output_fL1.txt","018-c",r"$f_{\Lambda1}$","Observed, fix others","Expected, fix other","Observed, float others","Expected, float others")
    submission.add_table(table_test)
    table_test = makegraph("./NonSMEFT/fai1d/output_fL1Zg.txt","018-d",r"$f_{\Lambda1}^{Z\gamma}$","Observed, fix others","Expected, fix other","Observed, float others","Expected, float others")
    submission.add_table(table_test)





    #\newcommand{\fB}{\ensuremath{f_{a2}}\xspace}
    #\newcommand{\fC}{\ensuremath{f_{a3}}\xspace}
    #\newcommand{\fL}{\ensuremath{f_{\Lambda1}}\xspace}
    #\newcommand{\fLZg}{\ensuremath{f_{\Lambda1}^{\PZ\gamma}}\xspace}
    rootname=["output_fa2fL1.root","output_fa2fL1Zg.root","output_fa3fa2.root","output_fa3fL1.root","output_fa3fL1Zg.root","output_fL1fL1Zg.root"]
    table_test =makelike("./NonSMEFT/2Dfai/"+rootname[0],"019-d",r"$f_{a2}$",r"$f_{\Lambda1}$")
    submission.add_table(table_test)
    table_test =makelike("./NonSMEFT/2Dfai/"+rootname[1],"019-e",r"$f_{a2}$",r"$f_{\Lambda1}^{Z\gamma}$")
    submission.add_table(table_test)
    table_test =makelike("./NonSMEFT/2Dfai/"+rootname[2],"019-a",r"$f_{a2}$",r"$f_{a3}$")
    submission.add_table(table_test)
    table_test =makelike("./NonSMEFT/2Dfai/"+rootname[3],"019-b",r"$f_{a3}$",r"$f_{\Lambda1}$")
    submission.add_table(table_test)
    table_test =makelike("./NonSMEFT/2Dfai/"+rootname[4],"019-c",r"$f_{a3}$",r"$f_{\Lambda1}^{Z\gamma}$")
    submission.add_table(table_test)
    table_test =makelike("./NonSMEFT/2Dfai/"+rootname[4],"019-f",r"$f_{\Lambda1}$",r"$f_{\Lambda1}^{Z\gamma}$")
    submission.add_table(table_test)


    #1D ci scans : 



    submission.create_files("Figures_018_019_020_021_022")



'''
disname=[
        '007-b','007-c',
        '011-a','011-b','011-c','011-d','011-e','011-f','011-g','011-h','011-i',
        '012-a','012-b','012-c','012-d','012-e','012-f','012-g','012-h','012-i',
        '013-a','013-b','013-c','013-d','013-e','013-f','013-g','013-h','013-i'
        ]
rootname=[
        'D_2jet_VBF','D_2jet_VH',
        'D_bkg','D_0minus_decay','D_0hplus_decay','D_L1_decay','D_L1Zg_decay','D_CP_decay','D_int_decay','D_bkg_boosted','ZZPt_boosted',
'D_bkg_VBFdecay','D_0minus_VBFdecay','D_0hplus_VBFdecay','D_L1_VBFdecay','D_L1Zg_VBFdecay','D_CP_VBF', 'D_int_VBF','D_bkg_VBF1j','ZZPt_VBF1j',
'D_bkg_HadVHdecay','D_0minus_HadVHdecay','D_0hplus_HadVHdecay' ,'D_L1_HadVHdecay','D_L1Zg_HadVHdecay','D_CP_HadVH' ,'D_int_HadVH','D_bkg_VHLep','ZZPt_VHLep'
        ]
submission.add_link("Webpage with all figures and tables", "https://cms-results.web.cern.ch/cms-results/public-results/publications/HIG-19-009/")
submission.add_link("arXiv", "http://arxiv.org/abs/arXiv:2104.12152")
submission.add_record_id(1860903, "inspire")
for l in range (0,29):
   table11a =makeHeshy(rootname[l],disname[l])
   submission.add_table(table11a)
table9a=makeTable("alldis_dbkgttH.root","009-a",r"$D_{bkg-}$","ttH")
table9b=makeTable("alldis_BDTGttH.root","009-b",r"$D_{0-}^{ttH}$","ttH")
table10a=makeTable("alldis_dbkgggH.root","010-a",r"$D_{bkg-}$","ggH")
table10b=makeTable("alldis_d_2j_qqggH.root","010-b",r"$D_{0-}^{ggH}$","ggH")
table10c=makeTable("alldis_d_2j_intggH.root","010-c",r"$D_{CP}^{ggH}$","ggH")
table14a=makegraph("fa3.txt","014-a",r"$f_{a3}^{ggH}$","ggH(4l)","","")
table14b=makelike("cgg_eft_cor_gamma_obs.root","014-b",r"$c_{gg}$",r"$\tilde{c}_{gg}$")
table15a=makegraph("scan_kappa.txt","015-a","fCP","ttH(gg+4l)","ttH(4l)","ttH(gg)")
table15b=makelike("kappa_eft_obs.root","015-b",r"$\kappa_t$",r"$\tilde{\kappa}_t$")
table16=makegraph("scan_kappa_cor.txt","016","fCP","ggH(4l)","ggH(4l)+ttH(4l)","ggH(4l)+ttH(gg+4l)")
table17a=makelike("cg_ct_eft_obs.root","017-a",r"$c_{gg}$",r"$\tilde{c}_{gg}$")
table17b=makelike("cg_ct_fix_eft_obs.root","017-b",r"$c_{gg}$",r"$\tilde{c}_{gg}$")
table17c=makelike("ka_kt_eft_obs.root","017-c",r"$\kappa_{t}$",r"$\tilde{\kappa}_{t}$")
table17d=makelike("ka_kt_fix_eft_obs.root","017-d",r"$\kappa_{t}$",r"$\tilde{\kappa}_{t}$")
table17e=makelike("ka_cg_eft_obs.root","017-e",r"$\kappa_{t}$",r"$c_{gg}$")
table17f=makelike("ka_cg_fix_eft_obs.root","017-f",r"$\kappa_{t}$",r"$c_{gg}$")

submission.add_table(table9a)
submission.add_table(table9b)
submission.add_table(table10a)
submission.add_table(table10b)
submission.add_table(table10c)
submission.add_table(table14b)
submission.add_table(table15b)
submission.add_table(table17a)
submission.add_table(table17b)
submission.add_table(table17c)
submission.add_table(table17d)
submission.add_table(table17e)
submission.add_table(table17f)

submission.add_table(table14a)
submission.add_table(table15a)
submission.add_table(table16)
submission.create_files("example_output")
'''

