def bechdel_scorer(entry):
    score = 0
    binary, clean_test, test = entry

    # Check the binary result
    if binary == 'FAIL':
        score -= 1
    elif binary == 'PASS':
        score += 1

    # Check the clean_test and test results
    if 'ok' in clean_test and 'disagree' not in clean_test:
        score += 0.5
    elif 'ok' in test and 'disagree' not in test:

        score += 0.5
    elif 'ok' in clean_test and 'disagree' in clean_test:
        score += 0.25
    elif 'ok' in test and 'disagree' in test:
        score += 0.25

    # Check for any 'disagree' without 'ok'
    if 'disagree' in clean_test and 'ok' not in clean_test:
        score += 0.25
    if 'disagree' in test and 'ok' not in test:
        score += 0.25

    # Normalize the score to be within -1 to 1
    score = max(min(score, 1), -1)

    return score