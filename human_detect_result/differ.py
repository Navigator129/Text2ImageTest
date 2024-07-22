import pandas as pd

def parse_decision(decision):
    if decision == 'T':
        return True
    else:
        return False

def get_decision(decision1, decision2):
    decision1 = parse_decision(decision1)
    decision2 = parse_decision(decision2)
    if decision1 and decision2:
        return True
    else:
        return False

def process():
    df = pd.read_excel('./human_detect_result/output.xlsx')
    decision_result = []

    for row in df.iterrows():
        results = row[1]
        result1 = get_decision(results[2], results[3])
        result2 = get_decision(results[4], results[5])
        result3 = get_decision(results[6], results[7])
        result4 = get_decision(results[8], results[9])


        if result1 and result2 and result3 and result4:
            decision_result.append(True)
        else:
            decision_result.append(False)

    df['Decision'] = decision_result
    df.to_excel('./human_detect_result/final_output.xlsx', index=False)

