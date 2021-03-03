# ROADMAP


## Short term

- Add a new field in account for all verified/ account ready to use
- Replace all uid or u_id type reponse keys
- Email verification mandatory on Merchant APIs and consumer payment APIs
- Add conditions for disabled merchant/ user
- Build feature for disabling a user account on admin
- Show request ID on 500 error
- Add twilio sms error conditions


## Medium term

- Add fields for KYC related data both on models and serializers (ex. EIN number, SSN number)
- Add phone number country to all places where we are asking for phone number from user
- Handle all the DB errors not just by catching exception but by resloving it to an error
- https://github.com/jazzband/django-defender
- Add error logging 
- Error formatting 
```
str     message:            A developer-friendly error message. Not
                            safe for programmatic use.
str     type:               A broad categorization of the error,
                            corresponding to the error class.
str     code:               An error code for programmatic use.
str     display_message:    A user-friendly error message. Not safe
                            for programmatic use. May be None.
list    causes:             A list of reasons explaining why the
                            error happened.
```
- Add IP address logging (Ref. Sentry)
- Move tip amount to order

## Long terms

- Implement Idempotency key feature in all API calls (Ref: dwolla)
- Encrypt user session key in sessions table
- Check file upload hash for onboarding docs (https://stackoverflow.com/questions/22058048/hashing-a-file-in-python)
- 

### Validators

- add ISO4217 validator
- Do not allow some special characters like `/` in loqal ID, only allow `@`, `#`, `.` etc.

### DB

- Make editable false on foreign keys


### Django settings
CSRF_TRUSTED_ORIGINS
