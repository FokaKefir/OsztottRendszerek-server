import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1 import FieldFilter

# load credentials for firebase
cred = credentials.Certificate('forms_key.json')
firebase_admin.initialize_app(cred)

# firestore db
db = firestore.client()

# referencies
users_ref = db.collection('users')
submits_ref = db.collection('submits')
forms_ref = db.collection('forms')


# register user then return user_id
def register_user(user: dict) -> str:
    # set default role to user
    if 'role' not in user.keys():
        user['role'] = 'user'

    # add user to users collection
    _, new_user_ref = users_ref.add(user)

    # return new user's uid
    return new_user_ref.id
    
# create a new submission then return its id
def create_submission(form_id: str, user_id: str, options: list) -> str:
    # create document dictionary
    submit = {
        'user_id': user_id,
        'form_id': form_id,
        'options': options
    }

    # add submit to the collection
    _, new_submit_ref = submits_ref.add(submit)

    # return new submit's uid
    return new_submit_ref.id

# create a new form then return 
def create_form(form: dict) -> str:
    # set default active value for the form
    if 'active' not in form.keys():
        form['active'] = True

    # add form to the forms collection
    _, new_form_ref = forms_ref.add(form)

    # return new form's uid
    return new_form_ref.id

# change the status of the form by it's id
def change_form_status(form_id: str, status: bool) -> None:
    # get form reference by form_id
    form_ref = forms_ref.document(form_id)

    # update document
    form_ref.update({'active': status})
    return


# get form data by it's id
def get_form(form_id: str) -> dict:
    # get form reference by form_id
    form_ref = forms_ref.document(form_id)

    # get form data
    form_data = form_ref.get().to_dict()
    return form_data

# get options and their count for a form
def get_form_submissions(form_id: str) -> dict:
    # get all submits of the form
    submit_filter = FieldFilter('form_id','==',form_id)
    submits = submits_ref.where(filter=submit_filter).stream()

    option_values={}
    # count each option
    for submit in submits:
        for option in submit.to_dict()['options']:
            if option in option_values:
                option_values[option] += 1
            else:
                option_values[option] = 1
    
    return option_values

#check if the form is completed by the user
def check_form_completed(form_id: str, user_id: str) -> bool:
    # get all submits of the form
    form_filter = FieldFilter('form_id','==',form_id)
    user_filter = FieldFilter('user_id','==',user_id)
    submits = submits_ref.where(filter=form_filter).where(filter=user_filter).stream()  

    # check if user already submitted the form
    if len(list(submits)) > 0:
        return True
   
    return False

# login user then return user_id
def login_user(email: str, password: str) -> str:
    # get all users
    users = users_ref.stream()

    # check if user exists
    for user in users:
        user_data = user.to_dict()
        if user_data['email'] == email and user_data['password'] == password:
            return user.id

    return None
