from flask import Flask, render_template, request,jsonify,url_for
from wtforms import Form,validators,SubmitField,DateTimeField
import json
from datetime import datetime
import time

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
   
class getForm(Form):
    start_time=DateTimeField('start time *',validators=[validators.DataRequired()],format="%Y-%m-%dT%H:%M:%SZ")
    end_time=DateTimeField('end time *',validators=[validators.DataRequired()],format="%Y-%m-%dT%H:%M:%SZ")
    submit = SubmitField('Submit')
class getForm1(Form):
    start_time=DateTimeField('start time *',validators=[validators.DataRequired()],format="%Y-%m-%dT%H:%M:%SZ")
    end_time=DateTimeField('end time *',validators=[validators.DataRequired()],format="%Y-%m-%dT%H:%M:%SZ")
    submit = SubmitField('Submit')
class getForm2(Form):
    start_time=DateTimeField('start time *',validators=[validators.DataRequired()],format="%Y-%m-%dT%H:%M:%SZ")
    end_time=DateTimeField('end time *',validators=[validators.DataRequired()],format="%Y-%m-%dT%H:%M:%SZ")
    submit = SubmitField('Submit')
@app.route('/')
def home():
    return render_template("main.html")
@app.route('/question1' , methods=["GET", "POST"])
def result():
    if request.method == "GET":
        form = getForm()
        return render_template("index.html",form=form)
    elif request.method == "POST":
        data=dict(request.form)
        stime = datetime.strptime(data["start_time"][0], '%Y-%m-%dT%H:%M:%SZ')
        etime = datetime.strptime(data["end_time"][0], '%Y-%m-%dT%H:%M:%SZ')
        shifts = { 
            'shiftA': {'production_A_count': 0,'production_B_count': 0},
            'shiftB': {'production_A_count': 0,'production_B_count': 0},
            'shiftC': {'production_A_count': 0,'production_B_count': 0}
        }
        with open('./shared/sample_json_1.json') as f:
            j=json.load(f)
            for d in j:
                time = datetime.strptime(d["time"], '%Y-%m-%d %H:%M:%S')
                if time>=stime and time<=etime:
                    if time.time()>=(datetime.strptime('06:00:00', '%H:%M:%S')).time() and time.time()<=(datetime.strptime('14:00:00', '%H:%M:%S')).time():
                        if(d["production_A"]):
                            shifts['shiftA']['production_A_count']+=1
                        if(d["production_B"]):
                            shifts['shiftA']['production_B_count']+=1   
                    if time.time()>=(datetime.strptime('14:00:00', '%H:%M:%S')).time() and time.time()<=(datetime.strptime('20:00:00', '%H:%M:%S')).time():
                        if(d["production_A"]):
                            shifts['shiftB']['production_A_count']+=1
                        if(d["production_B"]):
                            shifts['shiftB']['production_B_count']+=1
                    if time.time()>=(datetime.strptime('20:00:00', '%H:%M:%S')).time() or time.time()<=(datetime.strptime('06:00:00', '%H:%M:%S')).time():
                        if(d["production_A"]):
                            shifts['shiftC']['production_A_count']+=1
                        if(d["production_B"]):
                            shifts['shiftC']['production_B_count']+=1
        return jsonify(shifts)
@app.route('/question2' , methods=["GET", "POST"])
def result1():
    if request.method == "GET":
        form = getForm1()
        return render_template("index1.html",form=form)
    elif request.method == "POST":
        data=dict(request.form)
        stime = datetime.strptime(data["start_time"][0], '%Y-%m-%dT%H:%M:%SZ')
        etime = datetime.strptime(data["end_time"][0], '%Y-%m-%dT%H:%M:%SZ')
        alltime ={
            'runtime' : 0,
	        'downtime': 0,
        }
        result ={
            'runtime' : '0h:00m:00s',
            'downtime': '0h:00m:00s',
            'utilisation': 00.00
        }
        with open('./shared/sample_json_2.json') as f:
            j=json.load(f)
            for d in j:
                tme = datetime.strptime(d["time"], '%Y-%m-%d %H:%M:%S')
                if tme>=stime and tme<=etime:
                    if d["runtime"]>1021:
                        alltime['runtime']+=1021
                        alltime['downtime']+=d["runtime"]-1021
                    else :
                        alltime['runtime']+=d["runtime"]
        result['utilisation']+=(alltime['runtime']/(alltime['runtime']+alltime['downtime']))*100
        result['utilisation']=round(result['utilisation'],2)
        result['runtime']=time.strftime("%Hh:%Mm:%Ss", time.gmtime(alltime['runtime']))
        result['downtime']=time.strftime("%Hh:%Mm:%Ss", time.gmtime(alltime['downtime']))
        return jsonify(result)
@app.route('/question3' , methods=["GET", "POST"])
def result2():
    if request.method == "GET":
        form = getForm2()
        return render_template("index2.html",form=form)
    elif request.method == "POST":
        data=dict(request.form)
        stime = datetime.strptime(data["start_time"][0], '%Y-%m-%dT%H:%M:%SZ')
        etime = datetime.strptime(data["end_time"][0], '%Y-%m-%dT%H:%M:%SZ')
        sums={}
        with open('./shared/sample_json_3.json') as f:
            j=json.load(f)
            for d in j:
                time = datetime.strptime(d["time"], '%Y-%m-%d %H:%M:%S')
                if time>=stime and time<=etime:
                    aid=d["id"][4:]
                    aid=int(aid)
                    if sums.get(aid) == None:
                        if  d["state"]==False:
                            sums.update({
                                aid:{
                                'belt1' : d["belt1"],
                                'belt2' : 0,
                                }
                            })
                        else :
                            sums.update({
                                aid:{
                                'belt1' : 0,
                                'belt2' : d["belt2"],
                                }
                            })
                    else :
                        if d["state"]==False:
                            sums[aid]['belt1']+=d["belt1"]
                        else:
                            sums[aid]['belt2']+=d["belt2"]
        ans=[]
        k=sorted(sums.keys())
        for i in k:
            ans.append({'id':i,'avg_belt1':sums[i]['belt1'],'avg_belt2':sums[i]['belt2']})
        return jsonify(ans)
if __name__ == '__main__':
    app.run()
                