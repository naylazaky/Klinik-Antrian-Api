from fastapi import FastAPI
from database import engine, Base
from routers import users, queues

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistem Manajemen Antrian Klinik",
    description="""
    API untuk mengelola antrian pasien di klinik.
    - Pasien bisa daftar, login, dan ambil nomor antrian.
    - Status antrian: waiting → processing → done
    - Endpoint publik: lihat semua antrian, dan status
    - Endpoint terproteksi: ambil antrian, update status, hapus
    """,
    version="1.0.0"
)

app.include_router(users.router)
app.include_router(queues.router)

@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Selamat datang di API Sistem Antrian Klinik",
        "dokumentasi": "Buka /docs untuk Swagger UI"
    }