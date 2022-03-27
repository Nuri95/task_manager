from task_manager.sql_app.database import engine
from task_manager.sql_app.tables import Base

Base.metadata.create_all(engine)