"""Application startup and configuration."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.assignment.router import router as assignment_router
from app.api.authentication.router import router as auth_router
from app.api.authorization.middleware import AuthorizationMiddleware
from app.api.authorization.router import router as authorization_router
from app.api.role.router import router as role_router
from app.api.text_processing.router import router as text_processing_router
from app.api.transaction.router import router as transaction_router
from app.api.user.router import router as user_router

app = FastAPI(
    title='FastAPI Starter faster than ever',
    description='FastAPI Starter',
    version='0.1.0',
    openapi_url='/api/v1/openapi.json',
    docs_url='/api/v1/docs',
    redoc_url='/api/v1/redoc',
    openapi_tags=[
        {
            'name': 'Users',
            'description': 'Operations with users',
        },
        {
            'name': 'Auth',
            'description': 'Operations with authentication',
        },
        {
            'name': 'Transactions',
            'description': 'Operations with transactions',
        },
        {
            'name': 'Roles',
            'description': 'Operations with roles',
        },
        {
            'name': 'Assignments',
            'description': 'Operations with assignments',
        },
        {
            'name': 'Authorizations',
            'description': 'Operations with authorizations',
        },
        {
            'name': 'Data Processing',
            'description': 'Operations with data processing using AI',
        },
    ],
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
#  APP MIDDLEWARES
# ----------------------------------
app.add_middleware(AuthorizationMiddleware)

# ----------------------------------
#   APP ROUTERS
# ----------------------------------
app.include_router(user_router, prefix='/users', tags=['Users'])
app.include_router(auth_router, prefix='/auth', tags=['Auth'])
app.include_router(
    transaction_router, prefix='/transaction', tags=['Transactions']
)
app.include_router(role_router, prefix='/role', tags=['Roles'])
app.include_router(
    assignment_router, prefix='/assignment', tags=['Assignments']
)
app.include_router(
    authorization_router, prefix='/authorization', tags=['Authorizations']
)
app.include_router(
    text_processing_router, prefix='/text-processing', tags=['Text Processing']
)
# ----------------------------------


@app.get('/')
def read_root():
    """Root endpoint to verify that the API is running."""
    return {'message': 'Welcome to API!'}
