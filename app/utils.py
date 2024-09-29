from passlib.context import CryptContext
pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


def hash(password:str): # to hash the given password and store in the the database
   return pwd_context.hash(password)

def verify_password(plain_password, hashed_password): # to verify the password in the database to verify the login
   return pwd_context.verify(plain_password, hashed_password)


def convert_time_to_seconds(time_str):
   units = {"day": 86400, "hour": 3600, "days": 86400, "hours": 3600}
   value,unit = time_str.split()
   return f"r{int(value) * units[unit]}"