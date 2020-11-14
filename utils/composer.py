import csv
import random


def build_table(table_id, treatment):
    
    path = 'data/parts_' + str(table_id) + '.csv'
    decision_table = ''
    capacity = 0


    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        line_count = 0

        decision_table += '<table id="decision_table" border="0">'

        decision_table += '<tr>'
        decision_table += '<th style="width:110px"><b><a id="sort_id" href="#">Item<span id="arrow_part"></span></a></b> <br>ID</th>'
        decision_table += '<th style="width:110px"><b><a id="sort_w" href="#">Weight<span id="arrow_weight"></span></a></b><br>[lb]</th>'
        decision_table += '<th style="width:140px"><b><a id="sort_p" href="#">Value<span id="arrow_prob"></span></a></b><br>[pt]</th>'
        decision_table += '<th style="width:130px"><b><a id="sort_r" href="#">Ratio<span id="arrow_ratio"></span></a></b><br>[pt/lb]</th>'
        if treatment != 'no_sol':
            decision_table += '<th style="width:200px; vertical-align:top"><b>Recommendation</b><br></th>' #We do not set a recommendation column for treatment 'no_sol'
        decision_table += '<th style="width:220px; vertical-align:top"><b>Your Selection</b><br></th>'
        decision_table += '</tr>'

        decision_table += '<td style="border-top:1px solid black;" colspan="6"></td>'

        for row in csv_reader:
            if line_count == 0:
                # We take only the capacity from line 1
                capacity = float(f'{row[7]}')
                line_count += 1
            else:
                decision_table += '<tr>'
                decision_table += '<td>' + (f'{row[0]}') + '</td>' #Part ID
                decision_table += '<td>' + (f'{row[1]}') + '</td>' #Weight
                decision_table += '<td>' + (f'{row[2]}') + '</td>' #Value
                #decision_table += '<td>' + str(round(float(f'{row[3]}'),2)) + '</td>' #Ratio
                decision_table += '<td>' + (f'{row[3]}') + '</td>' #Ratio
                #Recommendation is only given in treatments 'opt_sol' and 'heur_sol'
                if treatment == 'opt_sol':
                    rec = ''
                    if int((f'{row[4]}')) == 1:
                        rec = 'checked=true'
                    decision_table += '<td><input type="checkbox" class="o_sol" id="o_part_' + (f'{row[0]}') + '" name="o_part_' + (f'{row[0]}') + '" value="o_part_' + (f'{row[0]}') + '" ' + rec + ' disabled="true"></td>'
                elif treatment == 'heur_sol':
                    rec = ''
                    if int((f'{row[5]}')) == 1:
                        rec = 'checked=true'
                    decision_table += '<td><input type="checkbox" class="h_sol" id="h_part_' + (f'{row[0]}') + '" name="h_part_' + (f'{row[0]}') + '" value="h_part_' + (f'{row[0]}') + '" ' + rec + ' disabled="true"></td>'
                decision_table += '<td><input type="checkbox" class="gurke" id="part_' + (f'{row[0]}') + '" name="part_' + (f'{row[0]}') + '" value="part_' + (f'{row[0]}') + '"></td>'
                line_count += 1

        decision_table += '<tr>'
        decision_table += '<td style="border-top:1px solid black;" colspan="6"></td>'

        #Total Weight
        decision_table += '<tr><td></td><td></td><td></td><td></td>'
        if treatment != 'no_sol':
            decision_table += '<td></td>'
        decision_table += '<td style="vertical-align:top"><b>Total Weight: <span id="total_weight">0</span>lb</b></td>'

        #Total Value
        decision_table += '<tr><td></td><td></td><td></td><td></td>'
        if treatment != 'no_sol':
            decision_table += '<td></td>'
        decision_table += '<td style="vertical-align:top"><b>Total Value: <span id="total_value">0</span>pt</b></td>'

        decision_table += '</table>'
    
    return decision_table, int(capacity)

def build_feedback_table(table_id, treatment, decision_str, part_drawn):
    path = 'data/parts_' + str(table_id) + '.csv'
    print(decision_str)
    decision = decision_str.split(",")
    print(decision)
    feedback_table = ''
    capacity = 0
    current_part = 1

    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        line_count = 0

        feedback_table += '<table id="decision_table" border="0">'

        feedback_table += '<tr>'
        feedback_table += '<th style="width:110px"><b>Item<span id="arrow_part"></span></b> <br>ID</th>'
        feedback_table += '<th style="width:110px"><b>Weight<span id="arrow_weight"></span></b><br>[lb]</th>'
        feedback_table += '<th style="width:140px"><b>Value<span id="arrow_prob"></span></b><br>[USD]</th>'
        feedback_table += '<th style="width:130px"><b>Ratio<span id="arrow_ratio"></span></b><br>[USD/lb]</th>'
        if treatment != 'no_sol':
            feedback_table += '<th style="width:200px; vertical-align:top"><b>Recommendation</b><br></th>' #We do not set a recommendation column for treatment 'no_sol'
        feedback_table += '<th style="width:200px; vertical-align:top"><b>Your Selection</b><br></th>'
        feedback_table += '</tr>'

        feedback_table += '<td style="border-top:1px solid black;" colspan="6"></td>'

        for row in csv_reader:
            if line_count == 0:
                # We take only the capacity from line 1
                capacity = float(f'{row[7]}')
                line_count += 1
            else:
                bold_start = ''
                bold_end = ''
                if current_part == part_drawn:
                    feedback_table += '<tr style="background-color:#C7C7C7">'
                    bold_start = '<b>'
                    bold_end = '</b>'
                else:
                    feedback_table += '<tr>'
                feedback_table += '<td>' + bold_start + (f'{row[0]}') + bold_end + '</td>' #Item ID
                feedback_table += '<td>' + bold_start + (f'{row[1]}') + bold_end + '</td>' #Weight
                feedback_table += '<td>' + bold_start + (f'{row[2]}') + bold_end + '</td>' #Value
                feedback_table += '<td>' + bold_start + (f'{row[3]}') + bold_end + '</td>' #Ratio

                #Recommendation is only given in treatments 'opt_sol' and 'heur_sol'
                if treatment == 'opt_sol':
                    rec = ''
                    if int((f'{row[4]}')) == 1:
                        rec = 'checked=true'
                    feedback_table += '<td>' + bold_start + '<input type="checkbox" class="o_sol" id="o_part_' + (f'{row[0]}') + '" name="o_part_' + (f'{row[0]}') + '" value="o_part_' + (f'{row[0]}') + '" ' + rec + ' disabled="true">' + bold_end + '</td>'
                elif treatment == 'heur_sol':
                    rec = ''
                    if int((f'{row[5]}')) == 1:
                        rec = 'checked=true'
                    feedback_table += '<td>' + bold_start + '<input type="checkbox" class="h_sol" id="h_part_' + (f'{row[0]}') + '" name="h_part_' + (f'{row[0]}') + '" value="h_part_' + (f'{row[0]}') + '" ' + rec + ' disabled="true">' + bold_end + '</td>'
                #Own Selection from previous round
                dec = ''
                #print('Decision for part ' + str(current_part) + ' is ' + str(decision[current_part-1]))
                if decision[current_part-1] == 'true':
                    dec = 'checked = true'             
                feedback_table += '<td>' + bold_start + '<input type="checkbox" class="gurke" id="part_' + (f'{row[0]}') + '" name="part_' + (f'{row[0]}') + '" value="part_' + (f'{row[0]}') + '" ' + dec + ' disabled="true">' + bold_end + '</td>'
                line_count += 1
                current_part += 1

        feedback_table += '<tr>'
        feedback_table += '<td style="border-top:1px solid black;" colspan="6"></td>'
        feedback_table += '<tr><td style="vertical-align:top"><b>Total Weight:</b></td><td><b><p id="total_weight">0</p></b></td>'

        feedback_table += '</table>'
    
    return feedback_table, capacity

def partDrawnWasSelected(decision_str, part_drawn):
    decision = decision_str.split(",")
    if decision[part_drawn-1] == 'true':
        return True
    else:
        return False

def getTextFeedbackPage(decision, part_drawn):
    text_begin = ('According to the probabilities shown <b>part ' + str(part_drawn) + ' was drawn</b>.'
        '<br>')
    if partDrawnWasSelected(decision, part_drawn):
        text_begin += 'Well done! You <b>had the required part ' + str(part_drawn) + ' in your vehicle</b>. You reveive <b>1 ECU</b> for this round.'
    else:
        text_begin += 'You <b>did not select the required part</b> into your vehice. You do not receive a payment for this round.'
    
    return text_begin

def getTextTreatmentPage(treatment):
    title = ''
    text_begin = ''
    table_explanation = ('The table contains the following information'
        '<br>'
        '<br>'
        '<ul>'
        '<li><b>Weight:</b> The weight of the item that will count towards the backpack\'s capacity.</li>'
        '<br>'
        '<li><b>Value:</b> The value assigned to the item.</li>'
        '<br>'
        '<li><b>Ratio:</b> The ratio between the value and the weight.</li>')

    if treatment == 'no_sol':
        title = 'Example'
        text_begin = ('In each round, you will see a table with the items you can make your selection from.'
            '<br>'
            '<br>'
            'Here is an example table. Note that, there is no limit for the capacity of your backpack in this example. In the following three rounds, though, your backpack will have a fixed capacity.'
            '<br>'
            '<br>'
        'You can order the item table by <i>Item ID, Weight, Value</i> or <i>Ratio</i> by clicking on the table headings.')

    elif treatment == 'opt_sol':
        title = 'Decision Support'
        text_begin = ('An algorithm has solved the problem. It selects items such that – given the backpack\'s capacity – the total value of the items in the backpack is maximized. The recommendation of the algorithm is shown in the item table.'
            '<br>'
            '<br>'
            'A table for an example set of items looks like this:')
        table_explanation += ('<br>'
            '<b><li>Recommendation: </b> The algorithm would make this selection.</li>')

    elif treatment == 'heur_sol':
        title = 'Decision Support'
        text_begin = ('An algorithm has solved the problem. It selects items such that – given the backpack\'s capacity – the total value of the items in the backpack is high. The recommendation of the algorithm is shown in the item table.'
            '<br>'
            '<br>'
            'A table for an example set of items looks like this:')
        table_explanation += ('<br>'
            '<b><li>Recommendation: </b> The algorithm would make this selection.</li>')

    else:
        title = '!Undefined Treatment Title!'
        text_begin = '!Undefined Treatment!'

    table_explanation += ('<br>'
        '<li><b>Your Selection: </b> You can make your selection by clicking the respective checkboxes.</li>'
            '<br>'
        '<li><b>Your Payoff: </b> Your payoff in this game will be the total value of all the items you place into your backpack under the capacity limit. </li>'
        '</ul>'
        )

    return title, text_begin, table_explanation

def getRandomPart(table_id):
    
    path = 'data/parts_' + str(table_id) + '.csv'
    prob_smaller_than_current_part = 0
    part_probabilities = []

    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                # We do not need the capacity
                line_count += 1
            else:
                prob_smaller_than_current_part += float(f'{row[2]}')
                part_probabilities.append(prob_smaller_than_current_part)
                line_count += 1
    
    #DEVELOPMENT
    print('Probabilities: ' + str(part_probabilities))

    random_nr = random.uniform(0, 1)
    part_id = 0

    #DEVELOPMENT
    print('Random Numbers: ' + str(random_nr))

    for part_probability in part_probabilities:
        part_id = part_id+1
        if random_nr <= part_probability:
            break

    print('Part ID: ' + str(part_id))
    
    return part_id

def buildResultTable(rounds, weight, value):

    result_table = '<table id="decision_table" border="0">'

    result_table += '<tr>'
    result_table += '<th style="width:110px"><b>Round</b> <br>ID</th>'
    result_table += '<th style="width:110px"><b>Total Weight</b><br>[lb]</th>'
    result_table += '<th style="width:140px"><b>Total Value</b><br>[pt]</th>'
    result_table += '<tr>'

    result_table += '<td style="border-top:1px solid black;" colspan="6"></td>'

    sumvalue = 0

    for r in range(1,rounds+1):
        result_table += '<tr>'
        result_table += '<td>' + str(r) + '</td>'
        result_table += '<td>' + str(weight[r-1]) + '</td>'
        result_table += '<td>' + str(value[r-1]) + '</td>'
        result_table += '</tr>'

        sumvalue = sumvalue+value[r-1]

    sumvalue_cent = int(sumvalue)
    sumvalue_dollar = sumvalue_cent/100

    result_table += '<tr>'
    result_table += '<td style="border-top:1px solid black;" colspan="6"></td>'
    result_table += '<tr><td></td><td style="vertical-align:top"><b>Total Value:</b></td><td><b>' + str(sumvalue) + 'pt</b></td>'

    result_table += '</table>'

    return sumvalue_cent, sumvalue_dollar, result_table
    
def buildLikertScale(questions):

    # table = '<style> td, th {text-align: center;}</style>'

    table = '<table id="likert_table" border="0">'

    width = 107

    table += '<tr>'
    table += '<th style="width:200px"><b>Question</b></th>'
    table += '<th style="width:' + str(width) + 'px; text-align: center">Strongly disagree</th>'
    table += '<th style="width:' + str(width) + 'px; text-align: center">Disagree</th>'
    #table += '<th style="width:' + str(width) + 'px; text-align: center">Somewhat disagree</th>'
    table += '<th style="width:' + str(width) + 'px; text-align: center">Neither agree nor disagree</th>'
    #table += '<th style="width:' + str(width) + 'px; text-align: center">Somewhat agree</th>'
    table += '<th style="width:' + str(width) + 'px; text-align: center">Agree</th>'
    table += '<th style="width:' + str(width) + 'px; text-align: center">Strongly agree</th>'
    table += '</tr>'

    table += '<td style="border-top:1px solid black;" colspan="8"></td>'

    question_counter = 0
    likert_scale_number = 5

    for q in questions:
        question_counter += 1
        table += '<tr style="height:90px">'
        table += '<td>' + str(q) + '</td>'
       
        for l in range(1,likert_scale_number+1):
             table += '<td style="text-align: center"><input type="radio" class="answer" name="q_' + str(question_counter) + '" value="' + str(l) + '"></td>'
        
        table += '</tr>'

    table += '</table>'

    return question_counter, table    
