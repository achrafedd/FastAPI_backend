from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    field_validator,
    model_validator,
)


class UserCreate(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=8)
    confirm_password: str = Field(..., min_length=8)
    user_name: str = Field(...)

    @field_validator('password', mode='before')
    @classmethod
    def password_validation(cls, password):
        special_char = '~`!@#$%^&*()_+{}[];:\'",<.>/\\|'
        if all([not c.isupper() for c in password]) or \
           all([not c.isdigit() for c in password]) or \
           all([not c in special_char for c in password]):
               raise ValueError("Password is invalid.")
        return password

    @model_validator(mode='after')
    def confirm_password_checker(self):
        if self.password != self.confirm_password:
            raise ValueError("Password is incorrect.")
        return self

if __name__ == '__main__':
    data = {
        'email':'hello@gmail.com',
        'password':'H3lL0Wrld@!',
        'confirm_password':'H3lL0Wrld@!',
        'user_name':'aeddiba'
        }
    result = UserCreate(**data)
    print(result)
