from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from users.router import router as users_router
from authentication.router import router as authentication_router
from roles.router import router as roles_router
from boards.router import router as boards_router

from utils.config import VERSION

app = FastAPI(
    title='Chess Backend',
    description='Some interesting functionality',
    version=VERSION
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        '*'
    ],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


@app.get(f'/', tags=['Setup'])
async def get_root_handler():
    return {
        'data': 'Chess Backend',
        'detail': f'Visit /docs or /redoc for the full documentation.'
    }


@app.get('/readyz', tags=['Setup'])
async def get_readyz_handler():
    return {
        'data': 'Ready',
        'detail': 'Backend is ready.'
    }


@app.get('/healthz', tags=['Setup'])
async def get_healthz_handler():
    return {
        'data': 'Health',
        'detail': 'Backend is healthy.'
    }


@app.get('/api/v1/version', tags=['Setup'])
async def get_version_handler():
    return {
        'data': VERSION,
        'detail': 'Version was selected.'
    }


app.include_router(users_router, prefix='/api/v1')
app.include_router(authentication_router, prefix='/api/v1')
app.include_router(roles_router, prefix='/api/v1')
app.include_router(boards_router, prefix='/api/v1')
