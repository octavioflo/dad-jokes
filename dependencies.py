from database.database import SessionLocal

def get_db():
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()


# origins = [
#     "http://localhost",
#     "http://localhost:8080",
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
