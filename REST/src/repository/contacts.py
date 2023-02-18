from datetime import datetime
from typing import List
from sqlalchemy import or_, and_
from sqlalchemy.orm import Session
from src.database.models import Contact, User
from src.schemas import ContactModel, ContactUpdate, ContactStatusUpdate


async def get_contacts(skip: int, limit: int, user: User, db: Session) -> List[Contact]:
    return db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()


async def get_contact(first_name: str, last_name: str, email: str, user: User, db: Session) -> List[Contact]:
    return db.query(Contact).filter(and_(or_(Contact.first_name == first_name,
     Contact.last_name == last_name, Contact.email == email), Contact.user_id == user.id)).all()


async def get_contact_by_birthday(user: User, db: Session) -> List[Contact]:
    now = datetime.now().date()
    year_now = now.year
    query_list = []
    result = db.query(Contact).all()
    for res in result:
        if res.user_id == user.id:
            b_list = res.birthday.split("-")
            if 0 <= (datetime(year_now, int(b_list[1]), int(b_list[2])).date()-now).days <= 7:
                query_list.append(res)
    return query_list


async def create_contact(body: ContactModel, user: User, db: Session) -> Contact:
    contact = Contact(first_name=body.first_name, last_name=body.last_name,
     email=body.email, phone=body.phone, birthday=body.birthday, user_id=user.id)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def remove_contact(contact_id: int, user: User, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id, Contact.user_id == user.id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact

async def update_contact(contact_id: int, body: ContactUpdate, user: User, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id, Contact.user_id == user.id).first()
    if contact:
        contact.first_name=body.first_name,
        contact.last_name=body.last_name,
        contact.email=body.email,
        contact.phone=body.phone, 
        contact.birthday=body.birthday
        contact.done=body.done
        db.commit()
    return contact


async def update_status_contact(contact_id: int, body: ContactStatusUpdate, user: User, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id, Contact.user_id == user.id).first()
    if contact:
        contact.done = body.done
        db.commit()
    return contact
