import datetime as dt
from json import JSONEncoder
import logging
import uvicorn
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
import json

from database import engine, Session, Base, City, User, Picnic, PicnicRegistration
from external_requests import CheckCityExisting, GetWeatherRequest
from models import RegisterUserRequest, UserModel, ItemPicnic, ItemRegistration, ItemCity


logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
logger = logging.getLogger('logger_root')  # pylint: disable=invalid-name


tags_metadata = [
    {
        "name": "picnic-add",
        "description": "picnic-add",
    },
    {
        "name": "all-picnics",
        "description": "all-picnics",
    },
    {
        "name": "picnic-register",
        "description": "picnic-register",
    },
]

app = FastAPI(openapi_tags=tags_metadata)

@app.post('/create-city/', summary='Create City', description='Создание города по его названию')
def create_city(item: ItemCity):
    """
        Создание города по его названию
    """
    if item.city is None:
        raise HTTPException(status_code=400, detail='Параметр city должен быть указан')
    check = CheckCityExisting()
    if not check.check_existing(item.city):
        raise HTTPException(status_code=400, detail='Параметр city должен быть существующим городом')

    city_object = Session().query(City).filter(City.name == item.city.capitalize()).first()
    if city_object is None:
        city_object = City(name=item.city.capitalize())
        s = Session()
        s.add(city_object)
        s.commit()
    logger.info(
        f'Город {item.city.capitalize()} создан!'
    )

    return JSONResponse(
        status_code=201,
        content={"message": "Город создан!",
                 "id": city_object.id,
                 "name": city_object.name,
                 "weather": city_object.weather,
                 }
        )


@app.get('/get-cities/', summary='Get Cities', description='Получение списка городов')
def cities_list(q: str = Query(description="Название города", default=None)):
    """
    Получение списка городов с необязательным параметром поиска q
    """
    if q:
        try:
            city_object = Session().query(City).filter(City.name == q).first()
            result = {'id': city_object.id, 'name': city_object.name, 'weather': city_object.weather}
            logger.info(
                f'Город {city_object.name} найден!'
            )
            return JSONResponse(
                status_code=200,
                content=result
            )
        except Exception:
            logger.info(
                f'Город {city_object.name} не найден!!'
            )
            return JSONResponse("Такой город не найден!", status_code=400)

    cities = Session().query(City).all()
    results = [{'id': city.id, 'name': city.name, 'weather': city.weather} for city in cities]
    logger.info(
        f'Список городов: {results}!'
    )

    return JSONResponse(
        status_code=200,
        content=results
    )


@app.get('/users-list/', summary='Get Users', description='Получение списка пользователей')
def users_list(minimum: int = Query(description="Минимальный возрост", default=None),
               maximum: int = Query(description="Максимальный возрост", default=None)):
    """
    Получение списка пользователей с необязательными параметроми фильтрации minimum, maximum
    """

    users = Session().query(User)
    if minimum is not None and maximum is None:
        users = users.filter(User.age >= minimum)
    elif maximum is not None and minimum is None:
        users = users.filter(User.age <= maximum)
    elif minimum is not None and maximum is not None:
        users = users.filter(User.age >= minimum, User.age <= maximum)
    else:
        users = users.all()

    results = [{
        'id': user.id,
        'name': user.name,
        'surname': user.surname,
        'age': user.age,
    } for user in users]
    logger.info(
        f'Список пользователей: {results}!'
    )

    return JSONResponse(
        status_code=200,
        content=results
    )

@app.post('/register-user/', summary='CreateUser', response_model=UserModel)
def register_user(user: RegisterUserRequest):
    """
    Регистрация пользователя
    """
    user_object = User(**user.dict())
    s = Session()
    s.add(user_object)
    s.commit()
    logger.info(
        f'Пользователей: {UserModel.from_orm(user_object)} добавлен!'
    )
    result = {'name': user_object.name, 'surname': user_object.surname, 'age': user_object.age}

    return JSONResponse(
        status_code=201,
        content=result
    )


@app.get('/all-picnics/', summary='All Picnics', tags=['all-picnics'])
def all_picnics(datetime: dt.datetime = Query(default=None, description='Время пикника (по умолчанию не задано)'),
                past: bool = Query(default=True, description='Включая уже прошедшие пикники')):
    """
    Получение списка всех пикников
    """
    picnics = Session().query(Picnic)
    if datetime is not None:
        picnics = picnics.filter(Picnic.time == datetime)
    if not past:
        picnics = picnics.filter(Picnic.time >= dt.datetime.now())

    return [{
        'id': pic.id,
        'city': pic.city.name,
        # 'city': Session().query(City).filter(City.id == pic.city_id).first().name,
        'time': pic.time,
        'users': [
            {
                'id': pr.user.id,
                'name': pr.user.name,
                'surname': pr.user.surname,
                'age': pr.user.age,
            }
            for pr in Session().query(PicnicRegistration).filter(PicnicRegistration.picnic_id == pic.id)],
    } for pic in picnics]


@app.post('/picnic-add/', summary='Picnic Add', tags=['picnic-add'])
def picnic_add(item: ItemPicnic):
    """
        Добавление нового объекта пикник в БД
    """
    city_object = Session().query(City).filter(City.id == item.city_id).first()
    if city_object is None:
        raise HTTPException(status_code=400, detail="Такого города нет в базе данных!")

    p = Picnic(**item.dict())
    s = Session()
    city_name = Session().query(City).filter(City.id == p.city_id).first().name
    s.add(p)
    s.commit()

    result = {'id': p.id, 'city': city_name, 'time': json.dumps(p.time, default=str)}
    logger.info(
        f'Объект пикник {result} добавлен!'
    )

    return JSONResponse(
        status_code=201,
        content=result
    )


@app.post('/picnic-register/', summary='Picnic Registration', tags=['picnic-register'])
def register_to_picnic(item: ItemRegistration):
    """
    Регистрация пользователя на пикник
    """
    user_object = Session().query(User).filter(User.id == item.user_id).first()
    if user_object is None:
        raise HTTPException(status_code=400, detail="Такого пользователя нет в базе данных!")

    picnic_object = Session().query(Picnic).filter(Picnic.id == item.picnic_id).first()
    if picnic_object is None:
        raise HTTPException(status_code=400, detail="Такого объекта пикник нет в базе данных!")

    reg = PicnicRegistration(**item.dict())
    s = Session()
    user_name = Session().query(User).filter(User.id == reg.user_id).first().name
    s.add(reg)
    s.commit()

    result = {'id': reg.id, 'user_name': user_name, 'picnic_id': reg.picnic_id}
    logger.info(
        f'Пользователь {user_name} зарегистрирован на пикник ID {reg.picnic_id}!'
    )
    return JSONResponse(
        status_code=201,
        content=result
    )

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)