def estado_primal(s):
    cntR = 0
    cntH = 0
    cntS = 0
    r = {}

    for temp in s:
        if temp["sign"] == "==":
            cntR += 1
            r[f"R{cntR}"] = 1
            temp[f"R{cntR}"] = 1
        elif temp["sign"] == ">=":
            cntR += 1
            cntS += 1
            r[f"R{cntR}"] = 1
            temp[f"R{cntR}"] = 1
            temp[f"S{cntS}"] = -1
            temp["sign"] = "=="
        else:
            cntH += 1
            temp[f"H{cntH}"] = 1
            temp["sign"] = "=="
        for key in temp:
            if key == "value" or key == "sign":
                continue
            r[key] = 0
            if "R" in key:
                r[key] = 1
    r_sorted = dict(sorted(r.items(), key=lambda item: sort_key(item[0])))

    return s, r_sorted

def sort_key(k):
    if k.startswith("x"): return (0, k)
    if k.startswith("S"): return (1, k)
    if k.startswith("R"): return (2, k)
    if k.startswith("H"): return (3, k)
    if k == "tipe": return (-1, "")
    return (4, k)