from fastapi import FastAPI  # , Request
from fastapi.middleware.cors import CORSMiddleware

from app.api.assignment.router import router as assignment_router
from app.api.authentication.router import router as auth_router
from app.api.authorization.middleware import AuthorizationMiddleware
from app.api.authorization.router import router as authorization_router
from app.api.role.router import router as role_router
from app.api.transaction.router import router as transaction_router
from app.api.user.router import router as user_router

app = FastAPI(
    title='CEUA - API',
    description='Applicação backend para o sistema da CEUA - UFPE',
    summary='Aplicação desenvolvida para a CEUA - UFPE',
    version='0.0.1',
    terms_of_service='https://www.ufpe.br/ceua',
    contact={
        'name': 'STILabs - STI/UFPE',
        'url': 'http://www.ufpe.br/sti',
        'email': 'stilabs.sti@ufpe.br',
    },
    license_info={
        'name': 'Apache 2.0',
        'url': 'https://www.apache.org/licenses/LICENSE-2.0.html',
    },
)


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
#  LOGGING MIDDLEWARE FOR DEBUGGING
# ----------------------------------

# FIXME: ainda é necessario corrigir pois quando ele esta descomentado ele trava o app
# @app.middleware("http")
# async def log_requests(request: Request, call_next):
#     print(f"Incoming request: {request.method} {request.url}")
#     print(f"Headers: {request.headers}")
#     print(f"Body: {await request.body()}")
#     response = await call_next(request)
#     return response

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
    return {'message': 'Wellcome to FairPlay API!'}
