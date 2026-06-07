"""Operator jonli yordam — chatlar, xabarlar, javob berish (Faza 3)."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_session
from core.models import Message, OperatorChat, User

from backend.app.deps import current_admin

router = APIRouter(prefix="/api/operator", tags=["operator"])


class ChatOut(BaseModel):
    id: int
    user_id: int
    status: str
    name: str | None = None
    username: str | None = None
    last_message: str | None = None


class MessageOut(BaseModel):
    id: int
    sender: str
    text: str


class ReplyIn(BaseModel):
    text: str


@router.get("/chats", response_model=list[ChatOut], dependencies=[Depends(current_admin)])
async def list_chats(status: str = "open", db: AsyncSession = Depends(get_session)):
    chats = list(await db.scalars(
        select(OperatorChat).where(OperatorChat.status == status).order_by(desc(OperatorChat.id))
    ))
    out = []
    for c in chats:
        user = await db.scalar(select(User).where(User.telegram_id == c.user_id))
        last = await db.scalar(
            select(Message).where(Message.chat_id == c.id).order_by(desc(Message.id)).limit(1)
        )
        out.append(ChatOut(
            id=c.id, user_id=c.user_id, status=c.status,
            name=user.name if user else None,
            username=user.username if user else None,
            last_message=last.text if last else None,
        ))
    return out


@router.get("/chats/{chat_id}/messages", response_model=list[MessageOut],
            dependencies=[Depends(current_admin)])
async def chat_messages(chat_id: int, db: AsyncSession = Depends(get_session)):
    rows = list(await db.scalars(
        select(Message).where(Message.chat_id == chat_id).order_by(Message.id)
    ))
    return [MessageOut(id=m.id, sender=m.sender, text=m.text) for m in rows]


@router.post("/chats/{chat_id}/reply", dependencies=[Depends(current_admin)])
async def reply(chat_id: int, data: ReplyIn, request: Request,
                db: AsyncSession = Depends(get_session)):
    chat = await db.get(OperatorChat, chat_id)
    if not chat:
        raise HTTPException(404, "Chat topilmadi")
    bot = getattr(request.app.state, "bot", None)
    if bot is None:
        raise HTTPException(503, "Bot ishlamayapti")
    db.add(Message(chat_id=chat_id, sender="operator", text=data.text))
    await db.commit()
    try:
        await bot.send_message(
            chat.user_id, f"👨‍💼 <b>Operator:</b>\n{data.text}"
        )
    except Exception as e:  # noqa: BLE001
        raise HTTPException(502, f"Foydalanuvchiga yuborib bo'lmadi: {e}")
    return {"ok": True}


@router.post("/chats/{chat_id}/close", dependencies=[Depends(current_admin)])
async def close_chat(chat_id: int, request: Request, db: AsyncSession = Depends(get_session)):
    chat = await db.get(OperatorChat, chat_id)
    if not chat:
        raise HTTPException(404, "Chat topilmadi")
    chat.status = "closed"
    await db.commit()
    bot = getattr(request.app.state, "bot", None)
    if bot is not None:
        try:
            await bot.send_message(chat.user_id, "✅ Operator suhbati yakunlandi. Rahmat!")
        except Exception:  # noqa: BLE001
            pass
    return {"ok": True}
