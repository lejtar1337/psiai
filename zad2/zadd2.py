import json

def load_knowledge_base(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return json.load(file)

def ask_questions(questions):
    user_answers = {}
    for q_id, q_data in questions.items():
        print(f"\n[{q_id}] {q_data['text']}")
        options = q_data['answers']
        
        for i, option in enumerate(options, 1):
            print(f"  {i}. {option}")
            
        while True:
            choice = input("Wybierz numer lub wpisz odpowiedź: ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(options):
                user_answers[q_id] = options[int(choice) - 1]
                break
            elif choice in options:
                user_answers[q_id] = choice
                break
            else:
                print("Nieprawidłowy wybór. Spróbuj ponownie.")
                
    return user_answers

def evaluate_rules(rules, user_answers):
    matched_rules = []
    for rule in rules:
        conditions = rule['if']
        if all(user_answers.get(q_id) == expected_ans for q_id, expected_ans in conditions.items()):
            matched_rules.append(rule['then'])
    return matched_rules

def main():
    filepath = 'zad.json'
    
    try:
        kb = load_knowledge_base(filepath)
    except FileNotFoundError:
        print(f"Błąd: Nie znaleziono pliku '{filepath}'. Zapisz w nim wcześniej wygenerowany model.")
        return
    except json.JSONDecodeError:
        print(f"Błąd: Plik '{filepath}' ma nieprawidłowy format JSON.")
        return

    user_answers = ask_questions(kb.get('questions', {}))
    matched_results = evaluate_rules(kb.get('rules', []), user_answers)

    print("\n--- WYNIKI DIAGNOZY ---")
    if matched_results:
        for i, result in enumerate(matched_results, 1):
            print(f"\n dopasowanie #{i}:")
            print(f"  Diagnoza: {result.get('diagnosis')}")
            print(f"  Zalecenie: {result.get('action')}")
    else:
        print("Brak pasujących reguł dla podanych odpowiedzi.")

if __name__ == '__main__':
    main()