from exts import db
from sqlalchemy import or_
import os
import time

class Base_Model():
    def add(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self



class Diploma(db.Model,Base_Model):
    __tablename__ = 'dip_diploma'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    project_name = db.Column(db.VARCHAR(255))
    project_content = db.Column(db.Text)
    compete_name = db.Column(db.VARCHAR(255),nullable=True)
    diploma_time = db.Column(db.Date,nullable=True)
    level = db.Column(db.VARCHAR(20),nullable=True)
    rank = db.Column(db.VARCHAR(20),nullable=True)
    image_path = db.Column(db.VARCHAR(100))
    time = db.Column(db.Integer,default=time.time())
    def get_values(self):
        data = {
            "id":self.id,
            "project_name":self.project_name,
            "compete_name":self.compete_name,
            "diploma_time":self.diploma_time,
            "level":self.level,
            "rank":self.rank,
            "content":self.project_content,
            "image_path":self.image_path,
            "time":self.time,
            "members":[m.member_name for m in self.members],
            "teachers":[t.teacher_name for t in self.teachers]
        }
        return data
    def delete(self):
        for m in self.members:
            db.session.delete(m)
        for t in self.teachers:
            db.session.delete(t)
        db.session.delete(self)
        db.session.commit()
        return self

    def add_members(self,members_list):
        for m in members_list:
            Member(diploma_id=self.id,member_name=m).add()

    def add_teachers(self,teachers_list):
        for t in teachers_list:
            Teacher(diploma_id=self.id,teacher_name=t).add()

class Member(db.Model,Base_Model):
    __tablename__ = 'dip_member'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    diploma_id = db.Column(db.Integer,db.ForeignKey('dip_diploma.id',ondelete='cascade'))
    member_name = db.Column(db.VARCHAR(20),nullable=True)
    time = db.Column(db.Integer,default=time.time())
    diploma = db.relationship('Diploma',backref = 'members')

class Teacher(db.Model,Base_Model):
    __tablename__ = 'dip_teacher'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    diploma_id = db.Column(db.Integer, db.ForeignKey('dip_diploma.id', ondelete='cascade'))
    teacher_name = db.Column(db.VARCHAR(20), nullable=True)
    time = db.Column(db.Integer, default=time.time())
    diploma = db.relationship('Diploma', backref='teachers')
