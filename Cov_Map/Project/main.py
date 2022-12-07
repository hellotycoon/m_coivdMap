from flask import Flask
from flask import render_template
app = Flask(__name__)
import utils
from flask import jsonify
from jieba.analyse import extract_tags


@app.route('/')
def cov_index_page():  # put application's code here
    return render_template("index.html")

@app.route('/time')
def get_time():
    return utils.get_time()

@app.route("/cov_trend_cq")
def get_cov_trend_cq_data():
    data = utils.get_cov_trend_cq_data()
    date = []
    confirmedIncr = []
    currentConfirmedIncr = []
    suspectedIncr = []
    curedIncr = []
    deadIncr = []
    i = len(data) - 1
    while(i >= 0):
        date.append(str(data[i][0]))
        confirmedIncr.append(data[i][1])
        currentConfirmedIncr.append(data[i][2])
        suspectedIncr.append(data[i][3]) 
        curedIncr.append(data[i][4])
        deadIncr.append(data[i][5])
        i -= 1
    return jsonify({"date":date,"confirmedIncr":confirmedIncr,"currentConfirmedIncr":currentConfirmedIncr,"suspectedIncr":suspectedIncr,"curedIncr":curedIncr,'deadIncr':deadIncr})

@app.route("/cov_trend")
def get_cov_trend_data():
    data = utils.get_cov_trend_data()
    date = []
    confirmedCount = []
    currentConfirmedCount = []
    suspectedCount = []
    curedCount = []
    deadCount = []
    for oneday in data:
        date.append(str(oneday[1])[4:])
        confirmedCount.append(oneday[0][0][0])
        currentConfirmedCount.append(oneday[0][0][1])
        suspectedCount.append(oneday[0][0][2])
        curedCount.append(oneday[0][0][3])
        deadCount.append(oneday[0][0][4])
    return jsonify({"date":date,"confirmedCount":confirmedCount,"currentConfirmedCount":currentConfirmedCount,"suspectedCount":suspectedCount,"curedCount":curedCount,"deadCount":deadCount})

@app.route("/total_data_of_china")
def get_total_data_of_china():
    data = utils.get_total_data_of_china()
    return jsonify({"currentConfirmedCount":int(data[0]),"suspectedCount":int(data[1]),"curedCount":int(data[2]),"deadCount":int(data[3])})

@app.route("/china_map")
def get_china_map_data():
    res = []
    for tup in utils.get_china_map_data(): #数据库查询结果为元组类型,数据为字符串类型
        res.append({'name':tup[0],'value':int(tup[1])})
    return jsonify({"data":res}) #组装成json格式{"data":res}
@app.route("/cov_top10")
def get_top10_data():
    data = utils.get_top10_data()
    province = []
    currentConfirmedCount = []
    for pvc,count in data:
        province.append(pvc)
        currentConfirmedCount.append(int(count))
    return jsonify({"city":province,'currentConfirmedCount':currentConfirmedCount})

@app.route("/wordcloud")
def get_wordcloud_data():
    data = utils.get_wordcloud_data()
    d = []
    for hotsearch in data:
        keywords = extract_tags(hotsearch[1])
        for keyword in keywords:
            if not keyword.isdigit():
                flag = False
                for char in keyword:
                    if char.isdigit():
                        flag = True
                        break
                if(flag):
                    continue
                d.append({"name":keyword,"value":int(hotsearch[0])})
    return jsonify({"kws":d})

@app.route("/covIncr_cq")
def get_covIncr_cq_data():
    data = utils.get_covIncr_cq_data()
    localIncr = []
    asymptomaticIncr = []
    dangerArea = []
    areaName = []
    for area in data:
        areaName.append(area[0])
        asymptomaticIncr.append(area[2])
        localIncr.append(area[1])
        dangerArea.append(area[3])
    return jsonify({'areaName':areaName,'localIncr':localIncr,'asymptomaticIncr':asymptomaticIncr,'dangerArea':dangerArea})

@app.route("/cov_msg")
def get_cov_msg_data():
    data = utils.get_cov_msg_data()
    return jsonify({'msg1':data[0],'msg2':data[1],'msg3':data[2],'msg4':data[3],'msg5':data[4]})

if __name__ == '__main__':
    app.run(host="0.0.0.0") #默认5000端口,在云服务器上要打开对应端口
