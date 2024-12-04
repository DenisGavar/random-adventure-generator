from app.common.db import db

class UserTask(db.Model):
    __tablename__ = "user_tasks"
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="assigned")
    completed_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    user = db.relationship("User", backref="user_tasks", cascade="all, delete", passive_deletes=True)
    task = db.relationship("Task", backref="user_tasks", cascade="all, delete", passive_deletes=True)