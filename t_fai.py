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
        obs_float = ""
        exp_float = ""
        obs_fix = ""
        exp_fix = ""
        

        #Logic to identify which graph of expfix/float and which obsfix/float 
        vals = []     
        for igr,gg in enumerate (gr): 
            
            line = []
            line.append(gg.Eval(0))
            line.append(gg.Eval(0.5))
            vals.append(line)

        
        iexp_float = -1 
        iexp_fix   = -1
        iobs_float = -1
        iobs_fix   = -1
        print (vals)
        print (vals[0][0])
        for i in range(0,4) : 
            if vals[i][0] < 0.0000000000001 : 
               if(iexp_float == -1 ) : 
                   iexp_float = i 
               else: 
                   iexp_fix = i
            else : 
                 if(iobs_float == -1) : 
                     iobs_float = i 
                 else : 
                     iobs_fix = i 
        if vals[iexp_float][1] > vals[iexp_fix][1] : 
            temp = iexp_float 
            iexp_float = iexp_fix 
            iexp_fix = temp
        if vals[iobs_float][1] > vals[iobs_fix][1] : 
            temp = iobs_float 
            iobs_float = iobs_fix 
            iobs_fix = temp
            
        if "fa2" in nm: 
            iobs_float = 3
            iobs_fix = 1
            iexp_float = 2 
            iexp_fix = 0
            
        print (iobs_fix, iexp_fix,iobs_float, iexp_float)        
        for igr,gg in enumerate (gr): 
            print gg.GetName()
            print nm
            step =(maxx - minx)/1000
            for ik in range(0,1001) :
                x = minx + step*ik
                graphval = gg.Eval(x)
                if (igr == 0 ) : 
                    if lx ==  "" : 
                        lx = str(x)
                    else : 
                        lx = lx + " "+str(x)
                    
                if igr == iexp_float :                     
                    if exp_float == "": 
                        exp_float = str(graphval)
                    else : 
                        exp_float = exp_float+" "+str(graphval)
                if igr == iexp_fix :                     
                    if exp_fix == "": 
                        exp_fix = str(graphval)
                    else : 
                        exp_fix = exp_fix+" "+str(graphval)
                if igr == iobs_fix :         
                    if obs_fix == "" : 
                        obs_fix = str(graphval)
                    else :     
                        obs_fix = obs_fix+" "+str(graphval)    
                if igr == iobs_float :         
                    if obs_float == "" : 
                        obs_float = str(graphval)
                    else :     
                        obs_float = obs_float+" "+str(graphval)    
                        
  
        lx = lx + "\n"
        obs_fix = obs_fix + "\n"
        exp_fix = exp_fix + "\n"
        obs_float = obs_float + "\n"
        exp_float = exp_float + "\n"
        fileout.write(lx)
        fileout.write(obs_fix)
        fileout.write(exp_fix)
        fileout.write(obs_float)
        fileout.write(exp_float)
        
    
