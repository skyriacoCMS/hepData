import ROOT 
import os 
import sys


nm = sys.argv[1]
minx = float(sys.argv[2])
maxx = float(sys.argv[3])
nmout = nm.replace("root","txt")

f = ROOT.TFile(nm)
c = f.Get("c1")
l  = list(c.GetListOfPrimitives())
fileout = open(nmout,"w")
#print l 
for i in l : 
    

    #print i 
    if i.InheritsFrom("TMultiGraph") or i.InheritsFrom("TGraph") : 
        print "this:",  i , i.GetName()
        gr = i.GetListOfGraphs()
        print gr
        lx = ""
        obs = ""
        exp = ""
        
        val0 = 0 
        val1 = 0
        for igr,gg in enumerate (gr): 
            if igr == 0 : 
                val0 = gg.Eval(0.05)
            if igr == 1 : 
                val1 = gg.Eval(0.05)
        
        iexp = 0         
        if val0 >  val1 :
            iexp = 1
        for igr,gg in enumerate (gr): 
            print gg.GetName()
            print nm
            step =(maxx - minx)/100
            for ik in range(0,101) :
                x = minx + step*ik
                
                if (igr == 0 ) : 
                    if lx ==  "" : 
                        lx = str(x)
                    else : 
                        lx = lx + " "+str(x)
                    
                if igr == iexp :                     
                    if exp == "": 
                        exp = str(gg.Eval(x))
                    else : 
                        exp = exp+" "+str(gg.Eval(x))
                else :         
                    if obs == "" : 
                        obs = str(gg.Eval(x))
                    else :     
                        obs = obs+" "+str(gg.Eval(x))    
                        
  
        lx = lx + "\n"
        obs = obs + "\n"
        exp = exp + "\n"
        fileout.write(lx)
        fileout.write(obs)
        fileout.write(exp)
        
    
