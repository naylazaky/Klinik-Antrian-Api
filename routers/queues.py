from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.queue import Queue
from models.user import User
from schemas.queue import QueueCreate, QueueUpdate, QueueOut
from auth.dependencies import get_current_user

router = APIRouter(prefix="/queues", tags=["Antrian Klinik"])

@router.post("/", response_model=QueueOut, status_code=status.HTTP_201_CREATED)
def take_queue(queue_data: QueueCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Ambil nomor antrian baru - butuh login"""
    last = db.query(Queue).order_by(Queue.queue_number.desc()).first()
    next_number = (last.queue_number + 1) if last else 1

    new_queue = Queue(
        queue_number=next_number,
        status="waiting",
        complaint=queue_data.complaint,
        user_id=current_user.id
    )
    db.add(new_queue)
    db.commit()
    db.refresh(new_queue)
    return new_queue

@router.get("/", response_model=list[QueueOut])
def get_all_queues(db: Session = Depends(get_db)):
    """Lihat semua antrian - public"""
    return db.query(Queue).order_by(Queue.queue_number).all()

@router.get("/waiting", response_model=list[QueueOut])
def get_waiting_queues(db: Session = Depends(get_db)):
    """Lihar antrisn yang masih menunggu - public"""
    return db.query(Queue).filter(Queue.status == "waiting").order_by(Queue.queue_number).all()

@router.get("/{queue_id}", response_model=QueueOut)
def get_queue_by_id(queue_id: int, db: Session = Depends(get_db)):
    """Lihat detail antrian by ID - public"""
    queue = db.query(Queue).filter(Queue.id == queue_id).first()
    if not queue:
        raise HTTPException(status_code=404, detail="Antrian tidak ditemukan")
    return queue

@router.put("/{queue_id}/status", response_model=QueueOut)
def update_status(queue_id: int, data: QueueUpdate, db:Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Update status antrian - butuh login"""
    valid = ["waiting", "processing", "done"]
    if data.status not in valid:
        raise HTTPException(status_code=422, detail=f"Status harus salah satu dari {valid}")
    
    queue = db.query(Queue).filter(Queue.id == queue_id).first()
    if not queue:
        raise HTTPException(status_code=404, detail="Antrian tidak ditemukan")
    
    queue.status = data.status
    db.commit()
    db.refresh(queue)
    return queue

@router.delete("/{queue_id}", status_code=status.HTTP_200_OK)
def delete_queue(queue_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Hapus antrian - butuh login"""
    queue = db.query(Queue).filter(Queue.id == queue_id). first()
    if not queue:
        raise HTTPException(status_code=404, detail="Antrian tidak ditemukan")
    db.delete(queue)
    db.commit()
    return {"message": f"Antrian nomor {queue.queue_number} berhasil dihapus"}