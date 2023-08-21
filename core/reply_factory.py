
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        # Placeholder logic for storing the answer in the session
        if "answers" not in session or session["answers"] != {}:
            session["answers"] = {}  # Initialize an empty dictionary for answers
        
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]
    print(current_question_id)
    next_question, nextoptions, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
        bot_responses.append('Options:-' +str(nextoptions))
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    '''
    Validates and stores the answer for the current question to django session.
    '''
    if current_question_id is None:
        return True, ""

    # Placeholder logic for answer validation
    if not answer:
        return False, "Answer cannot be empty."

    # Placeholder logic for storing the answer in the session
    if "answers" not in session:
        session["answers"] = {}  # Initialize an empty dictionary for answers

    session["answers"][current_question_id-1] = answer  # Store the answer in the session
    
    return True, ""  # Return success status and an empty error message



def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''
    if not current_question_id:
        current_question_id = 0
    
    if current_question_id > len(PYTHON_QUESTION_LIST) - 1:
        return None,None, None
    nextquestion = PYTHON_QUESTION_LIST[current_question_id]['question_text']
    nextoptions = PYTHON_QUESTION_LIST[current_question_id]['options']
    nextquestion_id = current_question_id +1
    
    return nextquestion,nextoptions,nextquestion_id



def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''
    score = 0
    for i in range(len(PYTHON_QUESTION_LIST)):
        print(PYTHON_QUESTION_LIST[i]['answer'],session["answers"][i])
        if(PYTHON_QUESTION_LIST[i]['answer'] == session["answers"][i]):
            score+=1

    return 'Your score is '+str(score)+' out of '+str(len(PYTHON_QUESTION_LIST))
