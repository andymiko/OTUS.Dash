import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import select, func, and_, or_
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, class_mapper
from typing import Optional

# === Подключение к БД ===
DATABASE_URL = f"sqlite+aiosqlite:///{os.path.join(os.getcwd(), 'dashdb.db')}"
engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


# === Базовая модель ===
class Base(DeclarativeBase):
    def to_dict(self) -> dict:
        """Универсальный метод для конвертации объекта SQLAlchemy в словарь"""
        # Получаем маппер для текущей модели
        columns = class_mapper(self.__class__).columns
        # Возвращаем словарь всех колонок и их значений
        return {column.key: getattr(self, column.key) for column in columns}

    def __repr__(self):
        """Читабельный вывод объекта"""
        attrs = ', '.join(f"{key}={value}" for key, value in self.to_dict().items())
        return f"<{self.__class__.__name__}({attrs})>"


# === Модель данных ===
class Data(Base):
    __tablename__ = "data"

    ordernumber: Mapped[str] = mapped_column(primary_key=True)
    orderdate: Mapped[Optional[str]]
    channel: Mapped[Optional[str]]
    order_quantity: Mapped[Optional[float]]
    unit_price: Mapped[Optional[float]]
    line_total: Mapped[Optional[float]]
    unit_cost: Mapped[Optional[float]]
    product_name: Mapped[Optional[str]]
    product_sales: Mapped[Optional[float]]
    district: Mapped[Optional[str]]
    subdistrict: Mapped[Optional[str]]
    total_unit_cost: Mapped[Optional[float]]
    district_sales: Mapped[Optional[float]]
    subdistrict_sales: Mapped[Optional[float]]
    schoolcustomer: Mapped[Optional[str]]
    centroid_lat: Mapped[Optional[str]]
    centroid_long: Mapped[Optional[str]]
    rentabel: Mapped[Optional[float]]
    category: Mapped[Optional[str]]
    warehouse_name: Mapped[Optional[str]]


# === Класс для работы с БД ===
class Database:
    def __init__(self):
        self.async_session_maker = async_session_maker

    async def create_tables(self):
        """Создает таблицы, если их нет"""
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def get_data_for_filters(self, type: str, param: str, **kwargs):
        """Получает уникальные значения для фильтрации"""
        async with self.async_session_maker() as session:
            stmt = select(getattr(Data, param)).distinct()

            for key, value in kwargs.items():
                stmt = stmt.where(getattr(Data, key) == value)

            result = await session.execute(stmt)
            data = [row[0] for row in result.all()]

            if type == 'option':
                return [{'value': col, 'label': col} for col in data]
            elif type == 'list':
                return data
            elif type == 'minmax':
                return min(data), max(data) if data else (None, None)
            else:
                raise ValueError('Некорректный тип')


    async def get_data(self, orderdate_range=None, rentabel_range=None, channel=None, **kwargs):
        """Получает данные по фильтрам, включая диапазоны и множественные значения"""
        async with self.async_session_maker() as session:
            stmt = select(Data)

            # Фильтр по точным совпадениям
            for key, value in kwargs.items():
                if isinstance(value, list):  # Если передан список значений, используем IN
                    stmt = stmt.where(getattr(Data, key).in_(value))
                else:
                    stmt = stmt.where(getattr(Data, key) == value)

            # Фильтр по дате
            if orderdate_range:
                stmt = stmt.where(and_(Data.orderdate >= orderdate_range[0], Data.orderdate <= orderdate_range[1]))

            # Фильтр по рентабельности
            if rentabel_range:
                stmt = stmt.where(and_(Data.rentabel >= rentabel_range[0], Data.rentabel <= rentabel_range[1]))

            # Фильтр по нескольким каналам продаж
            if channel:
                if isinstance(channel, list):
                    stmt = stmt.where(Data.channel.in_(channel))
                else:
                    stmt = stmt.where(Data.channel == channel)

            result = await session.execute(stmt)
            return result.scalars().all()
