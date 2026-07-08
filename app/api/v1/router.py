from fastapi import APIRouter

from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.problems import router as problems_router
from app.api.v1.endpoints.submissions import router as submissions_router
from app.api.v1.endpoints.test_cases import router as test_cases_router
from app.api.v1.endpoints.users import router as users_router

router = APIRouter()

router.include_router(health_router)
router.include_router(users_router)
router.include_router(auth_router)
router.include_router(problems_router)
router.include_router(submissions_router)
router.include_router(test_cases_router)
