Функционал:
- Список организаций по зданию
- Список организаций по виду деятельности 
- Поиск организаций по названию
- Организации в прямоугольнике и радиусе
- CRUD создания сущностей
- Списки зданий
- Статический API ключ (Header: X-API-Key)

Быстрый старт (Docker):
1. cp .env.example .env (при необходимости изменить API_KEY/DATABASE_URL)
2. docker compose up --build
3. Документация Swagger: http://localhost:8000/docs (или /redoc)
4. Примеры запросов:
   - GET /api/v1/organizations?activity_id=1
   - GET /api/v1/organizations?building_id=1
   - GET /api/v1/organizations?name=Рога
   - GET /api/v1/organizations/geo/rectangle?lat1=...&lon1=...&lat2=...&lon2=...
   - GET /api/v1/organizations/geo/radius?lat=...&lon=...&radius_m=2000

Локальная разработка:
- poetry install
- Настройте .env (DATABASE_URL)
- alembic upgrade head
- uvicorn app.main:app --reload
