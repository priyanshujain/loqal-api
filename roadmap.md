# ROADMAP

- Implement Idempotency key feature in all API calls (Ref: dwolla)
- Add logging 




- Password validation using django password validators
- Email verification mandatory on Merchant APIs and consumer payment APIs
- Verify EIN using python-stdnum




## Medium term

- Add fields for KYC related data both on models and serializers (ex. EIN number, SSN number)
- Add phone number country to all places where we are asking for phone number from user
- Handle all the DB errors not just by catching exception but by resloving it to an error
- https://github.com/jazzband/django-defender

## Long terms

### Validators

- add ISO4217 validator
- Do not allow some special characters like `/` in loqal ID, only allow `@`, `#`, `.` etc.

### DB

- Make editable false on foreign keys