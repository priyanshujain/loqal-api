# ROADMAP

- Implement Idempotency key feature in all API calls (Ref: dwolla)
- Add logging 




- Password validation using django password validators
- Email verification mandatory on Merchant APIs and consumer payment APIs
- Verify EIN using python-stdnum




## Medium term

- Add fields for KYC related data both on models and serializers (ex. EIN number, SSN number)
- Add phone number country to all places where we are asking for phone number from user


## Long terms

### Validators

- add ISO4217 validator
- Do not allow some special characters like `/` in loqal ID, only allow `@`, `#`, `.` etc.