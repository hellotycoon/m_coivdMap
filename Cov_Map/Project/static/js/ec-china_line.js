var chartDom = document.getElementById('multi-line-china');
var ecMulti_line = echarts.init(chartDom);
var ecMulti_line_option;

ecMulti_line_option = {
  title: {
    //text: 'Stacked Line'
  },
  tooltip: {
    trigger: 'axis'
  },
  legend: {
    data: ['累计确诊', '现存确诊', '累计疑似', '累计治愈', '累计死亡'],
  },
  grid: {
    left: '5%',
    right: '7%',
    bottom: '2%',
    containLabel: true
  },
  toolbox: {
    feature: {
      saveAsImage: {}
    }
  },
  xAxis: {
    type: 'category',
    boundaryGap: false,
    data: [],
    fontSize: 3
  },
  yAxis: {
    type: 'value'
  },
  series: [
    {
      name: '累计确诊',
      type: 'line',
      stack: 'Total',
      data: []
    },
    {
      name: '现存确诊',
      type: 'line',
      stack: 'Total',
      data: []
    },
    {
      name: '累计疑似',
      type: 'line',
      stack: 'Total',
      data: []
    },
    {
      name: '累计治愈',
      type: 'line',
      stack: 'Total',
      data: []
    },
    {
      name: '累计死亡',
      type: 'line',
      stack: 'Total',
      data: []
    }
  ]
};

ecMulti_line_option && ecMulti_line.setOption(ecMulti_line_option);

var chartDom2 = document.getElementById('multi-line-cq');
var ecMulti_line_cq = echarts.init(chartDom2);
var ecMulti_line_cq_option;

ecMulti_line_cq_option = {
  title: {
    //text: 'Stacked Line'
  },
  tooltip: {
    trigger: 'axis'
  },
  legend: {
    data: ['累计确诊新增', '现存确诊新增', '累计疑似新增', '累计治愈新增', '累计死亡新增'],
  },
  grid: {
    left: '5%',
    right: '7%',
    bottom: '2%',
    containLabel: true
  },
  toolbox: {
    feature: {
      saveAsImage: {}
    }
  },
  xAxis: {
    type: 'category',
    boundaryGap: false,
    data: [],
    fontSize: 3
  },
  yAxis: {
    type: 'value'
  },
  series: [
    {
      name: '累计确诊新增',
      type: 'line',
      stack: 'Total',
      data: []
    },
    {
      name: '现存确诊新增',
      type: 'line',
      stack: 'Total',
      data: []
    },
    {
      name: '累计疑似新增',
      type: 'line',
      stack: 'Total',
      data: []
    },
    {
      name: '累计治愈新增',
      type: 'line',
      stack: 'Total',
      data: []
    },
    {
      name: '累计死亡新增',
      type: 'line',
      stack: 'Total',
      data: []
    }
  ]
};


ecMulti_line_cq_option && ecMulti_line_cq.setOption(ecMulti_line_cq_option);
