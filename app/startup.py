from fastapi import FastAPI  # , Request
from fastapi.middleware.cors import CORSMiddleware

from app.api.assignment.router import router as assignment_router
from app.api.authentication.router import router as auth_router
from app.api.authorization.middleware import AuthorizationMiddleware
from app.api.authorization.router import router as authorization_router
from app.api.role.router import router as role_router
from app.api.transaction.router import router as transaction_router
from app.api.user.router import router as user_router

app = FastAPI()


# ----------------------------------
#  APP CORSMiddleware
# ----------------------------------
origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


# ----------------------------------
#  APP MIDDLEWARES
# ----------------------------------
app.add_middleware(AuthorizationMiddleware)

# ----------------------------------
#   APP ROUTERS
# ----------------------------------
app.include_router(user_router, prefix='/users', tags=['Users'])
app.include_router(auth_router, prefix='/auth', tags=['Auth'])
app.include_router(transaction_router, prefix='/transaction', tags=['Transactions'])
app.include_router(role_router, prefix='/role', tags=['Roles'])
app.include_router(assignment_router, prefix='/assignment', tags=['Assignments'])
app.include_router(
    authorization_router, prefix='/authorization', tags=['Authorizations']
)
# ----------------------------------


@app.get('/')
def read_root():
    return {'message': 'Wellcome to API!'}
