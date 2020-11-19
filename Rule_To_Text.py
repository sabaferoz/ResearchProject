from SPARQLWrapper import SPARQLWrapper, JSON

rule = "relative(v0,object)∧spouse(v0,subject)->relative(subject,object)"

#below function splits an atom into subject, predicate and object
def splitAtom(atom):
    predicate = atom.split('(')[0]
    subject = atom.split('(')[1].split(',')[0]
    object  = atom.split('(')[1].split(',')[1][0:-1]
    return predicate,subject,object

#converts the given atom into text
def atomToText(atom):
    splittedAtom = splitAtom(atom)
    predicate = splittedAtom[0]
    subject = splittedAtom[1]
    object = splittedAtom[2]
    text= subject + "'s " + predicate + " is " +  object;
    print(text);
    return text;

def splitPositiveRule(rule):
    splitText = rule.split('->')
    result= splitText[1]
    conditions = splitText[0]
    conditions = conditions.split('∧')
    return conditions,result

def positiveRuleToText(rule):
    print("rule: " + rule)
    text = "If"
    splittedRule = splitPositiveRule(rule)
    conditions = splittedRule[0]
    result = splittedRule[1]
    for condition in conditions:     
        if (text== 'If'):
            text =text + " " + atomToText(condition)
        else:
            text =text + " and "  + atomToText(condition)
    text = text + " then " + atomToText(result)
    print ("text: " + text)
    return text
        

def executeSparQl(rule):
    query="PREFIX dbo: <http://dbpedia.org/ontology/> SELECT * WHERE { "    
    splittedRule = splitPositiveRule(rule)
    conditions = splittedRule[0]
    result = splittedRule[1]
    entities = []
    for condition in conditions:
            splittedAtom = splitAtom(condition)
            predicate = splittedAtom[0]
            subject = splittedAtom[1]
            object = splittedAtom[2]
            if subject not in entities:
                entities.append(subject)
            if object not in entities:
                entities.append(object)
            query = query + "?" + subject +  " dbo:" + predicate +  " ?" + object + ". "
    splittedAtom = splitAtom(result)
    predicate = splittedAtom[0]
    subject = splittedAtom[1]
    object = splittedAtom[2]
    if subject not in entities:
        entities.append(subject)
    if object not in entities:
        entities.append(object)
    query = query + "?" + subject +  " dbo:" + predicate +  " ?" + object + ". }"
    text = positiveRuleToText(rule)
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    print (entities)
    for result in results["results"]["bindings"]:
        new_text=text
        for entity in entities:
            print("entity" + entity)
            new_text = new_text.replace(entity,result[entity]["value"].split('/')[-1])
        print(new_text)
        

    print('---------------------------')
    
executeSparQl(rule)

