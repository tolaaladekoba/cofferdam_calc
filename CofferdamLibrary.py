"""
Project: CofferdamCalc
File: CofferdamLibraray.py
Authors: Rylan Weldon
Date Last Modified: 4/27/2026

Changes made: Added abilitiy to calculate earth pressure automatically and checks for cases 1-6

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

def calculate_earth_pressures(phi, gamma):
    if phi is None or gamma is None or gamma == 0:
        return 0, 0
        
    phi_rad = math.radians(phi)
    
    ka = (math.tan(math.radians(45) - (phi_rad / 2)))**2
    kp = (math.tan(math.radians(45) + (phi_rad / 2)))**2
    
    pa_calc = gamma * ka
    pp_calc = gamma * kp
    
    return pa_calc, pp_calc
def case1(S, L, PA=None, PP=None, PHI=None, GAMMA=None):
    # case1: Determine if we need to calculate pressures from soil properties
    if (not PA or PA == 0) and PHI is not None:
        PA, PP = calculate_earth_pressures(PHI, GAMMA)
    Z = S + (PA * L)
    X = Z / (PP - PA)
    P1 = S * L
    P2 = (PA * L**2) / 2
    P3 = Z * X / 2

    PT = P1 + P2 + P3
    Y = math.sqrt((2 * PT) / (PP - PA))
    P4 = ((PP - PA) * Y**2) / 2
    M = (
        P1 * (X + Y + L / 2)
        + P2 * (X + Y + L / 3)
        + P3 * (Y + 2 * X / 3)
        - P4 * Y / 3
    )
    SP = L+X+Y

    return {
        "Z": Z,
        "X": X,
        "P1": P1,
        "P2": P2,
        "P3": P3,
        "PT": PT,
        "Y": Y,
        "P4": P4,
        "M": M,
        "SP": SP,
    }


def case2(S, L, PA=None, PP=None, D=None, PHI=None, GAMMA=None):
    if (not PA or PA == 0) and PHI is not None:
        PA, PP = calculate_earth_pressures(PHI, GAMMA)
    # Case 2: determines wall moment and top waler loading after excavation
    Z = S + (PA * D)
    X = Z / (PP - PA)
    P1 = S * D
    P2 = (PA * D**2) / 2
    P3 = Z * X / 2

    W = ((P1 * (X + D / 2)) + (P2 * (X + D / 3)) + (P3 * (2 * X / 3))) / (X + D - L)
    R = P1 + P2 + P3 - W
    PR = R / X
    PT = P1 + P2 + P3
    Y = math.sqrt((2 * PT) / (PP - PA))
    WH = W + (0.005 * W)
    WL = W - (0.005 * W)

    yVals = []
    mVals = []
    step = 0.0208

    if L < D:
        currY = L
        while currY <= D:
            W1 = (S * currY) + (PA * currY**2 / 2)

            if WH >= W1 >= WL:
                yVals.append(currY)
                M = (W * (currY - L)) - ((S * currY**2) / 2) - ((PA * currY**3) / 6)
                mVals.append(M)

            currY += step
    else:
        print("For input values there are no points of zero shear")

    return {
        "Z": Z,
        "X": X,
        "P1": P1,
        "P2": P2,
        "P3": P3,
        "PT": PT,
        "Y": Y,
        "W": W,
        "R": R,
        "PR": PR,
        "WH": WH,
        "WL": WL,
        "Moments": mVals,
        "YValues": yVals,
    }
def case3(S, L, PA=None, PP=None, D=None, DW=None, PHI=None, GAMMA=None):
        if (not PA or PA == 0) and PHI is not None:
            PA, PP = calculate_earth_pressures(PHI, GAMMA)
        F = D-DW
        
        PPadj = PP+60 
        
        PW = 60
        Z = S+(PA*F)+((PA-PW)*DW)
        P0 = (PA * F**2) / 2
        
        X = Z/(PP-PA)
        
        P1 = S*D
        P2 = ((PA-PW)/2)*DW**2
        P3 = Z*X/2
        P5 = PA*F*DW
    
        W = ((P0*(X+DW+F/3))+(P1*(X+D/2))+(P2*(X+DW/3))+(P3*2/3)+(P5*(X+DW/2)))/(X+D-L)
        R = P0 + P1 + P2 + P3 + P5 - W
        PR = R/X
        PT = P1+P2+P3
        #might have to revise, unsure if have to define in loop
        WH = W + (0.005 * W)
        WL = W - (0.005 * W)
        
        Ycalculated = 0
        if (PP - PA) > 0 and PT > 0:
            Ycalculated = math.sqrt((2 * PT) / (PP - PA))
        
        yVals = []
        mVals = []
        counter = 0
        step = 0.0208
    
        if L < D:
            currY = L
            while currY <= D:
                W1 = (S * currY) + P0 + (PA * F * (currY - F)) + (((PA - PW) / 2) * (currY - F)**2)
                
                if min(WH, WL) <= W1 <= max(WH, WL):
                    counter += 1
                    yVals.append(currY)
                    M = (W * (currY - L)) - ((S * currY**2) / 2) - (P0 * (currY - (2 * F / 3))) - ((PA * F * (currY - F)**2) / 2) - (((PA - PW) / 2) * (currY - F)**3 / 3)
                    mVals.append(M)
                currY += step
                
            if counter == 0:
                print("For input values there are no points of zero shear")
                
                if Ycalculated > 0:
                    finalW1 = (S * Ycalculated) + P0 + (PA * F * (Ycalculated - F)) + (((PA - PW) / 2) * (Ycalculated - F)**2)
                    Matycalc = (W * (Ycalculated - L)) - ((S * Ycalculated**2) / 2) - (P0 * (Ycalculated - (2 * F / 3))) - ((PA * F * (Ycalculated - F)**2) / 2) - (((PA - PW) / 2) * (Ycalculated- F)**3 / 3)
                    mVals = [Matycalc] 
                else:
                    Matd = (W*(D-L))-((S*D**2)/2)-(P0*(D-(2*F/3)))-((PA*F*(D-F)**2)/2)-(((PA-PW)/2)*(D-F)**3/3)
                    mVals = [Matd]
    
        return {
            "F": F,
            "PP": PPadj, 
            "PW": PW, 
            "Z": Z, 
            "P0": P0, 
            "X": X,
            "P1": P1, 
            "P2": P2, 
            "P3": P3, 
            "P5": P5,
            "W": W, 
            "R": R, 
            "PR": PR,
            "PT": PT, 
            "Moments": mVals, 
            "YValues": yVals
        }
def case4(S, L, PA=None, PP=None, D=None, DW=None, L1=0, L2=0, L3=0, L4=0, L5=0, L6=0, PHI=None, GAMMA=None):
    if (not PA or PA == 0) and PHI is not None:
        PA, PP = calculate_earth_pressures(PHI, GAMMA)
    # Case 4: determines wall moments and waler loadings for two or more walers

    X = (S + (PA * D)) / (PP - PA)
    SL1 = S + (PA * L)
    SL2 = SL1 + (PA * L1)
    SR = S + (PA * D)

    W1 = (S * L) + (((PA * L) * L) / 2) + ((SL1 * L1) / 2) + (((PA * (L1**2)) / 2) / 3)
    ML1 = (((S + (PA * L)) * (L1**2)) / 8) + (0.1283 * ((PA * L1) / 2) * (L1**2))

    SL3 = SL2 + (PA * L2)
    W2 = ((SL1 * L1) / 2) + ((((PA * (L1**2)) / 2) * 2) / 3) + ((SL2 * L2) / 2) + (((PA * (L2**2)) / 2) / 3)
    ML2 = ((SL2 * (L2**2)) / 8) + (0.1283 * ((PA * L2) / 2) * (L2**2))

    SL4 = SL3 + (PA * L3)
    W3 = ((SL2 * L2) / 2) + ((((PA * (L2**2)) / 2) * 2) / 3) + ((SL3 * L3) / 2) + (((PA * (L3**2)) / 2) / 3)
    ML3 = ((SL3 * (L3**2)) / 8) + (0.1283 * ((PA * L3) / 2) * (L3**2))

    SL5 = SL4 + (PA * L4)
    W4 = ((SL3 * L3) / 2) + ((((PA * (L3**2)) / 2) * 2) / 3) + ((SL4 * L4) / 2) + (((PA * (L4**2)) / 2) / 3)
    ML4 = ((SL4 * (L4**2)) / 8) + (0.1283 * ((PA * L4) / 2) * (L4**2))

    SL6 = SL5 + (PA * L5)
    W5 = ((SL4 * L4) / 2) + ((((PA * (L4**2)) / 2) * 2) / 3) + ((SL5 * L5) / 2) + (((PA * (L5**2)) / 2) / 3)
    ML5 = ((SL5 * (L5**2)) / 8) + (0.1283 * ((PA * L5) / 2) * (L5**2))

    WR = (
        ((SL6 * L6) * ((L6 / 2) + X))
        + (((PA * (L6**2)) / 2) * ((L6 / 3) + X))
        + (((SR * X) / 2) * ((2 / 3) * X))
    ) / (X + L6)

    W6 = ((SL5 * L5) / 2) + ((((PA * (L5**2)) / 2) * 2) / 3) + WR
    ML6 = (1 / 12) * (S + (PA * D)) * ((L6 + X) ** 2)

    TP = (
        (S * D)
        + ((PA * (D**2)) / 2)
        + ((SR * X) / 2)
        - W1
        - W2
        - W3
        - W4
        - W5
        - W6
    ) / X

    WT = W1 + W2 + W3 + W4 + W5 + W6

    return {
        "X": X,
        "SL1": SL1,
        "SL2": SL2,
        "SL3": SL3,
        "SL4": SL4,
        "SL5": SL5,
        "SL6": SL6,
        "SR": SR,
        "W1": W1,
        "W2": W2,
        "W3": W3,
        "W4": W4,
        "W5": W5,
        "W6": W6,
        "WR": WR,
        "WT": WT,
        "ML1": ML1,
        "ML2": ML2,
        "ML3": ML3,
        "ML4": ML4,
        "ML5": ML5,
        "ML6": ML6,
        "TP": TP,
    }
def case5(S, PA=None, PP=None, D=None, PHI=None, GAMMA=None):
    if (not PA or PA == 0) and PHI is not None:
        PA, PP = calculate_earth_pressures(PHI, GAMMA)
    T = S+(PA*D)
    M = T/(PP-PA)
    
    P1 = S * D
    P2 = (PA * D**2) / 2
    P3 = (T * M) / 2
    L = P1 + P2 + P3
    H = (P1*(M+D/2)+P2*(M+D/3)+P3*(2/3*M))/L
    
    #from the excel sheet, only thing found in code
    XH =2000
    XL =-2000
    bestXfound = D
    minXa = float('inf')
    
    X = D
    while X <= 2.5 * D:
        Xa =(X**4)-((8*L*(X**2))/(PP-PA))-((12*L*H*X)/(PP-PA))-(4*(L/(PP-PA))**2)
        #added to not print out every single xa
        if abs(Xa) < minXa:
            minXa = abs(Xa)
            bestXfound = X
        X +=0.04
        
    X = bestXfound
    ML = D + M + X
    Z = (X/2)-(L/((PP-PA)*X))
    Y = math.sqrt(L/((PP-PA)/2))
    
    P4 =((PP-PA)/2)*(Y**2)
    MS =(L*(Y+H))-(P4*(Y/3))
    
    VA =L
    VC =((PP-PA)/2) * (((X**2)-Z)/((2*X)-Z))
    
    return {
        "T": T,
        "M": M,
        "P1": P1,
        "P2": P2,
        "P3": P3,
        "L": L,
        "H": H,
        "X": X,
        "ML": ML,
        "Z": Z,
        "Y": Y,
        "P4": P4,
        "MS": MS,
        "VA": VA,
        "VC": VC
    }

def case6(S, PA=None, PP=None, D=None, DW=None, PHI=None, GAMMA=None):
    if (not PA or PA == 0) and PHI is not None:
        PA, PP = calculate_earth_pressures(PHI, GAMMA)
    # Case 6: determines moment and minimum length of sheetpile for a cantilevered bulkhead

    XH = 2000
    XL = -2000

    if D == 0:
        raise ValueError("For D = 0 there are no results")

    PW = 60
    PP_total = PP + PW
    F = D - DW
    P0 = (PA * (F**2)) / 2
    T = S + (PA * F) + ((PA - PW) * DW)
    M = T / (PP_total - PA)
    P1 = S * D
    P2 = ((PA - PW) / 2) * (DW**2)
    P3 = (T * M) / 2
    P5 = PA * F * DW
    L = P0 + P1 + P2 + P3 + P5

    H = (
        (P0 * (M + DW + (F / 3)))
        + (P1 * (M + (D / 2)))
        + (P2 * (M + (DW / 3)))
        + (P3 * ((2 / 3) * M))
        + (P5 * (M + (DW / 2)))
    ) / L

    D1 = 2.5 * D

    return {
        "XH": XH,
        "XL": XL,
        "PW": PW,
        "PP_total": PP_total,
        "F": F,
        "P0": P0,
        "T": T,
        "M": M,
        "P1": P1,
        "P2": P2,
        "P3": P3,
        "P5": P5,
        "L": L,
        "H": H,
        "D1": D1,
    }


if __name__ == "__main__":
    # Case 1 test
    s, l, pa, pp = 300, 60, 75, 280
    results = case1(s, l, pa, pp)
    print("Case 1:")
    print("Inputs: S: " + str(s) + " L: " + str(l) + " PA: " + str(pa) + " PP: " + str(pp))
    print(
        "Z: " + str(round(results["Z"], 2))
        + " X: " + str(round(results["X"], 2))
        + " P1: " + str(round(results["P1"], 2))
        + " P2: " + str(round(results["P2"], 2))
        + " P3: " + str(round(results["P3"], 2))
        + " PT: " + str(round(results["PT"], 2))
        + " Y: " + str(round(results["Y"], 2))
        + " P4: " + str(round(results["P4"], 2))
        + " M: " + str(round(results["M"], 2))
        + " SP: " + str(round(results["SP"], 2))
    )

    print()

    # Case 2 test
    s, l, pa, pp, dd = 8, 2, 1, 7, 9
    result2 = case2(s, l, pa, pp, dd)
    print("Case 2:")
    print("Inputs: S: " + str(s) + " L: " + str(l) + " PA: " + str(pa) + " PP: " + str(pp) + " D: " + str(dd))
    print(
        "Z: " + str(round(result2["Z"], 2))
        + " X: " + str(round(result2["X"], 2))
        + " P1: " + str(round(result2["P1"], 2))
        + " P2: " + str(round(result2["P2"], 2))
        + " P3: " + str(round(result2["P3"], 2))
        + " PT: " + str(round(result2["PT"], 2))
        + " Y: " + str(round(result2["Y"], 2))
        + " W: " + str(round(result2["W"], 2))
        + " Moments: " + str(result2["Moments"])
        + " Y_shear: " + str(result2["YValues"])
    )

    print()

    # Case 4 test
    s, l, pa, pp, d, dw, l1, l2, l3, l4, l5, l6 = 5, 2, 3, 4, 4, 2, 3, 4, 5, 6, 7, 8
    result4 = case4(s, l, pa, pp, d, dw, l1, l2, l3, l4, l5, l6)

    print("Case 4:")
    print(
        "Inputs: "
        + "S: " + str(s)
        + " L: " + str(l)
        + " PA: " + str(pa)
        + " PP: " + str(pp)
        + " D: " + str(d)
        + " DW: " + str(dw)
        + " L1: " + str(l1)
        + " L2: " + str(l2)
        + " L3: " + str(l3)
        + " L4: " + str(l4)
        + " L5: " + str(l5)
        + " L6: " + str(l6)
    )
    print(
        "X: " + str(round(result4["X"], 2))
        + " SL1: " + str(round(result4["SL1"], 2))
        + " SL2: " + str(round(result4["SL2"], 2))
        + " SL3: " + str(round(result4["SL3"], 2))
        + " SL4: " + str(round(result4["SL4"], 2))
        + " SL5: " + str(round(result4["SL5"], 2))
        + " SL6: " + str(round(result4["SL6"], 2))
        + " SR: " + str(round(result4["SR"], 2))
        + " W1: " + str(round(result4["W1"], 2))
        + " W2: " + str(round(result4["W2"], 2))
        + " W3: " + str(round(result4["W3"], 2))
        + " W4: " + str(round(result4["W4"], 2))
        + " W5: " + str(round(result4["W5"], 2))
        + " W6: " + str(round(result4["W6"], 2))
        + " WR: " + str(round(result4["WR"], 2))
        + " WT: " + str(round(result4["WT"], 2))
        + " ML1: " + str(round(result4["ML1"], 2))
        + " ML2: " + str(round(result4["ML2"], 2))
        + " ML3: " + str(round(result4["ML3"], 2))
        + " ML4: " + str(round(result4["ML4"], 2))
        + " ML5: " + str(round(result4["ML5"], 2))
        + " ML6: " + str(round(result4["ML6"], 2))
        + " TP: " + str(round(result4["TP"], 2))
    )

    print()

    # Case 6 test
    s, l, pa, pp, d, dw, l1, l2, l3, l4, l5, l6 = 5, 2, 3, 4, 4, 2, 3, 4, 5, 6, 7, 8
    result6 = case6(s, pa, pp, d, dw)

    print("Case 6:")
    print(
        "Inputs: "
        + "S: " + str(s)
        + " L: " + str(l)
        + " PA: " + str(pa)
        + " PP: " + str(pp)
        + " D: " + str(d)
        + " DW: " + str(dw)
        + " L1: " + str(l1)
        + " L2: " + str(l2)
        + " L3: " + str(l3)
        + " L4: " + str(l4)
        + " L5: " + str(l5)
        + " L6: " + str(l6)
    )
    print(
        "XH: " + str(round(result6["XH"], 2))
        + " XL: " + str(round(result6["XL"], 2))
        + " PW: " + str(round(result6["PW"], 2))
        + " PP_total: " + str(round(result6["PP_total"], 2))
        + " F: " + str(round(result6["F"], 2))
        + " P0: " + str(round(result6["P0"], 2))
        + " T: " + str(round(result6["T"], 2))
        + " M: " + str(round(result6["M"], 2))
        + " P1: " + str(round(result6["P1"], 2))
        + " P2: " + str(round(result6["P2"], 2))
        + " P3: " + str(round(result6["P3"], 2))
        + " P5: " + str(round(result6["P5"], 2))
        + " L: " + str(round(result6["L"], 2))
        + " H: " + str(round(result6["H"], 2))
        + " D1: " + str(round(result6["D1"], 2))
    )

def case7c1(R, W, E, S, H, FC, FY, rebarList):
    csDict = {6: 0.44, 7: 0.6, 8: 0.79, 9: 1, 10: 1.27, 11: 1.56, 14: 2.25, 18: 4}
    AS = 0
    for quant, barSize in rebarList:
        testArea = csDict.get(barSize, 0)
        AS = AS+quant*testArea
    P = W * R
    M = (P * E) / 12
    TA = 15 * AS
    IS = TA*((S/2)-3)**2
    IC = (H * S**3) / 12
    IT = IS + IC
    
    WM = (FC * IT) / (48 * (R**3))
    PM = (FC * IT) / (48 * (R**2))
    
    FA = (1000 * P) / (S * H)
    FB = (12000 * M * (S / 2)) / IT
    PG = AS / (S * H)
    FB_1 = 0.45 * FC
    FA_1 = 0.34 * (1 + ((PG * FY) / (0.85 * FC))) * FC
    CS = (FA / FA_1) + (FB / FB_1)
    EC = (((0.67 * PG * FY) / (0.85 * FC)) + 0.17) * (S - 3)
    return {
        #scaled by 1000 to convert to ft-lb
        "M": M * 1000,
        "P": P,
        "AS": AS,
        "TA": TA,
        "IS": IS,
        "IC": IC,
        "IT": IT,
        "WM": WM,
        "PM": PM,
        "CS": CS,
        "EC": EC
    }

def case7c2(R, W, S, H, FC, FY, rebarList, E=3.0):
    csDict = {6: 0.44, 7: 0.6, 8: 0.79, 9: 1, 10: 1.27, 11: 1.56, 14: 2.25, 18: 4}
    AS = 0
    for quant, barSize in rebarList:
        testArea = csDict.get(barSize, 0)
        AS = AS+quant*testArea

    P = W*R
    #rise is radius
    T = R  
    M = 0.068 * W * (T**2)
    TA = 15 * AS
    IS = TA * ((S / 2) - 3)**2
    IC = (H * S**3) / 12
    IT = IS + IC
    
    WM = (FC * IT) / (48 * (R**3))
    
    FA = (1000 * P) / (S * H)
    FB = (12000 * M * (S / 2)) / IT
    PG = AS / (S * H)
    FB_1 = 0.45 * FC
    FA_1 = 0.34 * (1 + ((PG * FY) / (0.85 * FC))) * FC
    CS = (FA / FA_1) + (FB / FB_1)
    EC = (((0.67 * PG * FY) / (0.85 * FC)) + 0.17) * (S - 3)
    
    return {
        #scaled by 1000 to convert to ft-lb
        "M": M * 1000,
        "P": P,
        "AS": AS,
        "TA": TA,
        "IS": IS,
        "IC": IC,
        "IT": IT,
        "WM": WM,
        "CS": CS,
        "EC": EC
    }

def case7c3(R, W, T, C, S, H, FC, FY, rebarList, E=3.0):
    csDict = {6: 0.44, 7: 0.6, 8: 0.79, 9: 1, 10: 1.27, 11: 1.56, 14: 2.25, 18: 4.00}
    AS = 0
    for quant, barSize in rebarList:
        testArea = csDict.get(barSize, 0)
        AS = AS+quant*testArea
    
    P = W*R
    M = 0.068*W*(T**2)
    TA = 15 * AS
    IS = TA * ((S / 2) - 3)**2
    IC = (H * S**3) / 12
    IT = IS + IC
    
    try:
        AG = (C / 2) / math.sqrt((R**2) - (C / 2)**2)
        AD = math.degrees(math.atan(AG))#this is for pis estimate
    except Error:
        AD = 90
        
    WM = ((FC*IT)/(144*(R**3)))*(((180**2)/(AD**2))-1)
    
    FA = (1000*P)/(S*H)
    FB = (12000 * M * (S / 2)) / IT
    PG = AS / (S * H)
    FB_1 = 0.45 * FC
    FA_1 = 0.34 * (1 + ((PG * FY) / (0.85 * FC))) * FC
    CS = (FA / FA_1) + (FB / FB_1)
    EC = (((0.67 * PG * FY) / (0.85 * FC)) + 0.17) * (S - 3)
    
    return {
        #scaled by 1000 to convert to ft-lb
        "M": M*1000,
        "P": P,
        "AS": AS,
        "TA": TA,
        "IS": IS,
        "IC": IC,
        "IT": IT,
        "AD": AD,
        "WM": WM,
        "CS": CS,
        "EC": EC
    }
