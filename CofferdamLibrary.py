"""
Project: CofferdamCalc
File: CofferdamLibraray.py
Authors: Rylan Weldon
Date Last Modified: 3/22/2026



Description:

This portion of the program is created to provide access to the needed algorithms for each Cofferdam
Calculation case. The first two cases have been made, both providing intermediate and final values as the output. 
There is also test cases to ensure both functions worked properly. The arithmetic and nomenclature for the variables for
both functions was taken directly from the excel sheet with the calculations. 

To Run:
On a computer with Python installed, ensure that you have the current file installed with the .py file extension
and double click to run with Python. The output from the test cases will be displayed.

Author: Rylan Weldon
"""
import math

def case1(S, L, PA, PP):
    #Case 1: determines cantilever moment when cofferdam is excavated to install top waler
    #Z, X, p1/p2/p3 calculations
    Z = S + (PA * L)
    X = Z / (PP - PA)
    P1 = S * L
    P2 = (PA * L**2) / 2
    P3 = Z * X / 2
    
    #Pt, Y, p4, m, Sp calculation
    PT = P1 + P2 + P3
    Y = math.sqrt((2 * PT) / (PP - PA))
    P4 = ((PP - PA) * Y**2) / 2
    M = P1*(X + Y + L/2) + P2*(X + Y + L/3) + P3*(Y + 2*X/3) - P4*Y/3
    SP = L + X + Y
    
    return {"Z": Z, "X": X, "P1": P1, "P2": P2, "P3": P3, "PT": PT, "Y": Y, "P4": P4, "M": M, "SP": SP}

def case2(S, L, PA, PP, D):
    #Case 2: This program determines wall moment and top water loading after excavation
    #z, x, p1, p2, p3 calculations
    Z = S + (PA * D)
    X = Z / (PP - PA)
    P1 = S * D
    P2 = (PA * D**2) / 2
    P3 = Z * X / 2
    
    #W, r, pr, pt, y, w1, wh, wl calculation
    W = ((P1 * (X + D/2)) + (P2 * (X + D/3)) + (P3 * (2 * X/3))) / (X + D - L)
    R = P1 + P2 + P3 - W
    PR = R / X
    PT = P1 + P2 + P3
    Y = math.sqrt((2 * PT) / (PP - PA))
    W1 = Y * 5
    WH = W + (0.005 * W)
    WL = W - (0.005 * W)
    yVals = []
    mVals = []
    count = 0
    step = 0.0208
    
    current = L
    if L < D:
        currY = L
        #for second subroutine (for y=l to d step 0.0208)
        while currY <= D:
            W1 = (S * currY) + (PA * currY**2 / 2)
            
            #for third subroutine: (if wh>=W1 and W1 >=wl)
            if WH >= W1 and W1 >= WL:
                count = count + 1;
                yVals.append(currY)
                M = (W * (currY - L)) - ((S * currY**2) / 2) - ((PA * currY**3) / 6)
                mVals.append(M)
            currY += step
        if count == 0:
            print("There are no points of zero shear")
    else: #for first subroutine (checking if L >= D)
        print("For input values there are no points of zero shear")
    return {
        "Z": Z, "X": X, "P1": P1, "P2": P2, "P3": P3, "PT": PT, 
        "Y": Y, "W": W, "Moments": mVals, "YValues": yVals
    }

#Case1:
s, l, pa, pp = 300, 60, 75, 280
results = case1(s, l, pa, pp)
print("Case 1:")
print("Inputs: S: "+str(s)+ " L: " +str(l)+ " PA: " +str(pa)+ " PP: "+str(pp));
print("Case one calculations:")
print("Z: " + str(round(results["Z"], 2)) + 
          " X: " + str(round(results["X"], 2)) + 
          " P1: " + str(round(results["P1"], 2)) + 
          " P2: " + str(round(results["P2"], 2)) + 
          " P3: " + str(round(results["P3"], 2)) + " PT: " + str(round(results["PT"], 2)) + 
          " Y: " + str(round(results["Y"], 2)) + 
          " P4: " + str(round(results["P4"], 2))+
          " M: " + str(round(results["M"], 2))+
          " SP: " +str(round(results["SP"], 2)))
#Case2 :
print("\n")
s, l, pa, pp, dd = 8, 2, 1, 7, 9
result2 = case2(s, l, pa, pp, dd)

print("Case 2:")
print("Inputs: s: "+str(s)+ " L: " +str(l)+ " PA: " +str(pa)+ " PP: "+str(pp)+ " DD: "+str(dd));print("Case two calculations:")
print("Z: " + str(round(result2["Z"], 2)) + 
      " X: " + str(round(result2["X"], 2)) + 
      " P1: " + str(round(result2["P1"], 2)) + 
      " P2: " + str(round(result2["P2"], 2)) + 
      " P3: " + str(round(result2["P3"], 2)) + 
      " PT: " + str(round(result2["PT"], 2)) + 
      " Y: " + str(round(result2["Y"], 2)) + 
      " W: " + str(round(result2["W"], 2)) + 
      " M: " + str(result2["Moments"]) + 
      " Y_shear: " + str(result2["YValues"]))
testing = input("");
