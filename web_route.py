from app import *
import json
import hashlib
import datetime
import dip_excel
import os
basedir = os.path.abspath(os.path.dirname(__file__))
@app.route('/admin/')
def admin_index():
    return render_template('admin/charts.html')

@app.route('/admin/manage/')
def admin_manage():
    all_diplomas = Diploma.query.filter().all()
    diploma_list = [i.get_values() for i in all_diplomas]
    return render_template('admin/tables.html',diploma=diploma_list)

@app.route('/admin/add/diploma',methods=['GET','POST'])
def admin_add_diploma():
    if request.method=='GET':
        diploma = {
            "id": '',
            "project_name": '',
            "compete_name": '',
            "diploma_time": '',
            "level": '',
            "rank": '',
            "time": ''
        }
        return render_template('admin/add_diploma.html',diploma=diploma,today=datetime.date.today())
    else:
        project_name = request.form.get('project_name')
        level = request.form.get('level')
        rank = request.form.get('rank')
        compete_name = request.form.get('compete_name')
        compete_member = request.form.get('compete_member')
        techer_name = request.form.get('compete_teacher')
        project_time = request.form.get('project_time')
        project_content = request.form.get('project_content')
        project_image = request.files.get('project_image')
        if project_image:
            image_save_path = url_for('static',filename='images/project_images/')+str(hashlib.md5(str(str(time.time())+str(project_name)).encode('utf-8')).hexdigest())+'.jpg'
        else:
            image_save_path = ''
        re_data = {
            "status":400,
            "content":""
        }
        if compete_name=="":
            re_data['content']="未填写比赛名称"
            return json.dumps(re_data)

        if compete_member=="":
            re_data['content']="未填写比赛人员"
            return json.dumps(re_data)

        if level==None:
            re_data['content'] = "未选择比赛的级别"
            return json.dumps(re_data)

        if rank==None:
            re_data['content'] = "未选择比赛的等次"
            return json.dumps(re_data)

        member_name_list = compete_member.split(";")
        teacher_name_list = techer_name.split(";")
        if member_name_list==[]:
            re_data['content'] = "请按（A;B;C）的填写方式填写参赛人员"
            return json.dumps(re_data)


        if project_time=="":
            re_data['content']="未填写比赛时间"
            return json.dumps(re_data)
        if project_image:
            project_image.save(basedir+image_save_path)
        dip_id = Diploma(project_name=project_name,project_content=project_content,compete_name=compete_name,diploma_time=project_time,level=level,rank=rank,image_path=image_save_path).add().id
        for m in member_name_list:
            Member(diploma_id=dip_id,member_name=m).add()
        for t in teacher_name_list:
            Teacher(diploma_id=dip_id,teacher_name=t).add()
        re_data['status']=200
        re_data['content']='OK'
        return json.dumps(re_data)

@app.route('/admin/edit/diploma/<id>',methods=['GET','POST'])
def admin_edit_diploma(id):
    if request.method=='GET':
        diploma = Diploma.query.filter(Diploma.id==id).first().get_values()
        return render_template('admin/add_diploma.html',diploma=diploma)
    else:
        diploma = Diploma.query.filter(Diploma.id==id).first()
        if diploma:
            project_name = request.form.get('project_name')
            level = request.form.get('level')
            rank = request.form.get('rank')
            compete_name = request.form.get('compete_name')
            compete_member = request.form.get('compete_member')
            techer_name = request.form.get('compete_teacher')
            project_time = request.form.get('project_time')
            project_content = request.form.get('project_content')
            project_image = request.files.get('project_image')
            if project_image:
                image_save_path = url_for('static', filename='images/project_images/') + str(hashlib.md5(str(str(time.time()) + str(project_name)).encode('utf-8')).hexdigest()) + '.jpg'
            else:
                image_save_path = ''
            re_data = {
                "status": 400,
                "content": ""
            }
            if compete_name == "":
                re_data['content'] = "未填写比赛名称"
                return json.dumps(re_data)

            if compete_member == "":
                re_data['content'] = "未填写比赛人员"
                return json.dumps(re_data)

            if level == None:
                re_data['content'] = "未选择比赛的级别"
                return json.dumps(re_data)

            if rank == None:
                re_data['content'] = "未选择比赛的等次"
                return json.dumps(re_data)

            member_name_list = compete_member.split(";")
            teacher_name_list = techer_name.split(";")
            if member_name_list == []:
                re_data['content'] = "请按（A;B;C）的填写方式填写参赛人员"
                return json.dumps(re_data)

            if project_time == "":
                re_data['content'] = "未填写比赛时间"
                return json.dumps(re_data)

            diploma.project_name = project_name
            diploma.project_content = project_content
            if project_image:
                project_image.save(basedir + image_save_path)
                diploma.image_path = image_save_path
            diploma.rank=rank
            diploma.time=time.time()
            diploma.diploma_time=project_time
            diploma.compete_name=compete_name
            for m in diploma.members:
                m.delete()
            for t in diploma.teachers:
                t.delete()
            for m in member_name_list:
                Member(diploma_id=diploma.id, member_name=m).add()
            for t in teacher_name_list:
                Teacher(diploma_id=diploma.id,teacher_name=t).add()
            re_data['status'] = 200
            re_data['content'] = 'OK'
            db.session.commit()
            return json.dumps(re_data)
        else:
            return json.dumps({'status':'400','content':"奖状不存在"})


@app.route('/admin/delete/diploma_list/',methods=['POST'])
def admin_delete_diploma_list():
    select_id = request.values.getlist('select')
    for id in select_id:
        Diploma.query.filter(Diploma.id==id).first().delete()
    return redirect(url_for('admin_manage'))

@app.route('/admin/delete/diploma/<id>',methods=['POST'])
def admin_delete_diploma(id):
    Diploma.query.filter(Diploma.id==id).first().delete()
    return redirect(url_for('admin_manage'))
#
@app.route('/admin/add/excel',methods=['POST'])
def admin_add_excel():
    excel_file = request.files.get('excel')
    if excel_file:
        file_path = basedir+'/file/'+str(time.time())+'.xlsx'
        excel_file.save(file_path)
        try:
            dip_excel.ReadDiploma(file_path).read()
        except Exception:
            pass
        os.remove(file_path)

    return redirect(url_for('admin_manage'))

#
#
# #########################前台###########################
#
#
@app.route('/')
def index():
    def count_number(level='',rank=''):
        level_tuple=None
        if level != '':
            if level == '校级':
                level_tuple=(or_(Diploma.level=='校级',Diploma.level=='院级'))
            else:
                level_tuple=(Diploma.level==level)
        if rank!='':
            if rank=='一等奖':
                rank_tuple = (or_(Diploma.rank=='特等奖',Diploma.rank=='一等奖'))
            elif rank=='三等奖':
                rank_tuple = (or_(Diploma.rank=='三等奖',Diploma.rank=='优秀奖'))
            else:
                rank_tuple = (Diploma.rank==rank)
                level_tuple += rank_tuple
        result = db.session.query(func.count(Diploma.id)).filter(level_tuple).first()[0]
        return result
    data={
        "total":count_number(),
        "nation":{
            'total':count_number('国家级'),
            'one':count_number('国家级','一等奖'),
            'two':count_number('国家级','二等奖'),
            'three':count_number('国家级','三等奖'),
        },
        "province":{
            'total':count_number('省级'),
            'one':count_number('省级','一等奖'),
            'two':count_number('省级','二等奖'),
            'three':count_number('省级','三等奖'),
        },
        "school":{
            'total':count_number('校级'),
            'one':count_number('校级','一等奖'),
            'two':count_number('校级','二等奖'),
            'three':count_number('校级','三等奖'),
        },
    }
    nation = Diploma.query.filter(Diploma.level=='国家级',Diploma.rank=='一等奖').all()
    nation = [m.get_values() for m in nation]
    nation += [m.get_values() for m in Diploma.query.filter(Diploma.level=='国家级',Diploma.rank=='二等奖').all()]
    nation += [m.get_values() for m in Diploma.query.filter(Diploma.level=='国家级',Diploma.rank=='三等奖').all()]
    return render_template('html/index.html',stat=data,nation=nation)

@app.route('/list/<id>')
def list(id):
    diploma = Diploma.query.filter().all()
    diploma_list = [di.get_values() for di in diploma]
    return render_template('html/list.html',diploma=diploma_list)

@app.route('/article/<id>')
def article(id):
    diploma = Diploma.query.filter(Diploma.id==id).first()
    if diploma:
        infor  = diploma.get_values()
        print(infor)
        return render_template('html/list-detail.html',diploma = infor)
    else:
        return redirect(url_for('list'))
#
#
#


