/*
-------------GRAPHING-------------

PnL vs Time (Date, X amount of labels), Linegraph


Cumsum vs Time
Signals vs Time, Linegraph
Histogram of daily % returns
Time vs SD (if we have time), optional
 */



/*let x = [];
let y = [];

for (let i = 0; i < 100; i++) {
    x.push(i);
    y.push(i * i);
}*/

am4core.useTheme(am4themes_animated);
am4core.useTheme(am4themes_customTheme);
// am4core.useTheme(am4themes_kelly);


// line chart
function sigmaGraph() {
    /*let lineChart = am4core.create('lineChart', am4charts.XYChart);
    lineChart.data = [];
    for (let i = 0; i < dataframe['Date'].length; i++) {
        lineChart.data.push({'Date': new Date(dataframe['Date'][i]), 'PnL': dataframe['PnL'][i]});
    }
    let horizontalAxis1 = lineChart.xAxes.push(new am4charts.DateAxes());
    let verticalAxis1 = lineChart.yAxes.push(new am4charts.ValueAxis());

    horizontalAxis1.title.text = 'Date';
    verticalAxis1.title.text = 'PnL';

    let series1 = lineChart.series.push(new am4charts.LineSeries());
    series1.name = 'PnL vs Time';
    series1.strokeWidth = 3;
    series1.dataFields.dateX = 'Date';
    series1.dataFields.valueY = 'PnL';

    lineChart.legend = new am4charts.Legend();
    lineChart.cursor = new am4charts.XYCursor();
    lineChart.scrollbarY = new am4core.Scrollbar();
    lineChart.scrollbarX = new am4core.Scrollbar();*/

    let pnlTime = am4core.create('pnlTime', am4charts.XYChart);
    pnlTime.data = [];
    for (let i = 0; i < Object.keys(dataframe['Date']).length; i++) {
        pnlTime.data.push({'x': new Date(dataframe['Date'][i]), 'y': dataframe['PnL'][i]});// lineChart.data.push({'x': i, 'y': i*i});
        // console.log(lineChart.data[i]);
    }
    let horizontalAxis1 = pnlTime.xAxes.push(new am4charts.DateAxis());
    let verticalAxis1 = pnlTime.yAxes.push(new am4charts.ValueAxis());

    horizontalAxis1.title.text = 'X';
    verticalAxis1.title.text = 'Y';

    let series1 = pnlTime.series.push(new am4charts.LineSeries());
    series1.name = 'PnL vs Time';
    series1.strokeWidth = 3;
    series1.dataFields.dateX = 'x';
    series1.dataFields.valueY = 'y';

    pnlTime.legend = new am4charts.Legend();
    pnlTime.cursor = new am4charts.XYCursor();
    pnlTime.scrollbarY = new am4core.Scrollbar();
    pnlTime.scrollbarX = new am4core.Scrollbar();





    let cumSumTime = am4core.create('cumSumTime', am4charts.XYChart);
    cumSumTime.data = [];
    for (let i = 0; i < Object.keys(dataframe['Date']).length; i++) {
        cumSumTime.data.push({'x': new Date(dataframe['Date'][i]), 'y': dataframe['cum_sum'][i]});// lineChart.data.push({'x': i, 'y': i*i});
        // console.log(lineChart.data[i]);
    }
    let horizontalAxis2 = cumSumTime.xAxes.push(new am4charts.DateAxis());
    let verticalAxis2 = cumSumTime.yAxes.push(new am4charts.ValueAxis());

    horizontalAxis2.title.text = 'Date';
    verticalAxis2.title.text = 'Cumulative Profit and Loss';

    let series2 = cumSumTime.series.push(new am4charts.LineSeries());
    series2.name = 'Cumulative Profit and Loss vs Time';
    series2.strokeWidth = 3;
    series2.dataFields.dateX = 'x';
    series2.dataFields.valueY = 'y';

    cumSumTime.legend = new am4charts.Legend();
    cumSumTime.cursor = new am4charts.XYCursor();
    cumSumTime.scrollbarY = new am4core.Scrollbar();
    cumSumTime.scrollbarX = new am4core.Scrollbar();



    let signalTime = am4core.create('signalTime', am4charts.XYChart);
    signalTime.data = [];
    for (let i = 0; i < Object.keys(dataframe['Date']).length; i++) {
        signalTime.data.push({'x': new Date(dataframe['Date'][i]), 'y': dataframe['Signal'][i]});// lineChart.data.push({'x': i, 'y': i*i});
        // console.log(lineChart.data[i]);
    }
    let horizontalAxis3 = signalTime.xAxes.push(new am4charts.DateAxis());
    let verticalAxis3 = signalTime.yAxes.push(new am4charts.ValueAxis());

    horizontalAxis3.title.text = 'Date';
    verticalAxis3.title.text = 'Signals';

    let series3 = signalTime.series.push(new am4charts.LineSeries());
    series3.name = 'Signals vs Time';
    series3.strokeWidth = 3;
    series3.dataFields.dateX = 'x';
    series3.dataFields.valueY = 'y';

    signalTime.legend = new am4charts.Legend();
    signalTime.cursor = new am4charts.XYCursor();
    signalTime.scrollbarY = new am4core.Scrollbar();
    signalTime.scrollbarX = new am4core.Scrollbar();


    console.log('Done');
}

// grouped bar plot

/*let barChart = am4core.create('barChart', am4charts.XYChart);
barChart.data = [];
for (let i = 0; i < x.length; i++) {
    barChart.data.push({'x': x[i], 'y': y[i], 'z': i * 30});
}
let horizontalAxis2 = barChart.xAxes.push(new am4charts.CategoryAxis());
let verticalAxis2 = barChart.yAxes.push(new am4charts.ValueAxis());

horizontalAxis2.dataFields.category = 'x';
horizontalAxis2.title.text = 'Independent Variable'
horizontalAxis2.renderer.minGridDistance = 40;
verticalAxis2.title.text = 'Dependent Variable';

let series2 = barChart.series.push(new am4charts.ColumnSeries());
series2.dataFields.valueY = 'y';
series2.dataFields.categoryX = 'x';
series2.name = 'X vs Y';
// series2.columns.template.fill = am4core.color('#104547')
series2.tooltipText = '{name}: [bold]{valueY}[/]'

let series3 = barChart.series.push(new am4charts.ColumnSeries());
series3.dataFields.valueY = 'z';
series3.dataFields.categoryX = 'x';
series3.name = 'X vs Z';
// series3.columns.template.fill = am4core.color('#603010');
// series3.tooltipText = '{name}: [bold]{valueY}[/]';
barChart.responsive.enabled = true;
barChart.legend = new am4charts.Legend();
barChart.cursor = new am4charts.XYCursor();
barChart.scrollbarY = new am4core.Scrollbar();
barChart.scrollbarX = new am4core.Scrollbar();


/*let scrollbarX = new am4charts.XYChartScrollbar();
scrollbarX.series.push(series);
chart.scrollbarX = scrollbarX;*/


/*series.columns.template.tooltipText = 'Series: {name}\nX: {valueX}\nY: {valueY}';
series.columns.template.fill = am4core.color('#104547')
series.dataFields.valueY = 'y';
series.dataFields.valueX = 'x';*/


function am4themes_customTheme(target) {
    if (target instanceof am4core.InterfaceColorSet) {
        /*target.setFor("primaryButton", am4core.color("#353A41"));
        target.setFor("primaryButtonHover", am4core.color("#353A41").lighten(-0.2));
        target.setFor("primaryButtonDown", am4core.color("#353A41").lighten(-0.2));
        target.setFor("primaryButtonActive", am4core.color("#353A41").lighten(-0.2));
        target.setFor("primaryButtonText", am4core.color("#FFFFFF"));
        target.setFor("primaryButtonStroke", am4core.color("#353A41"));*/
        target.setFor("secondaryButton", am4core.color("#353A41"));
        target.setFor("secondaryButtonHover", am4core.color("#353A41").lighten(-0.2));
        target.setFor("secondaryButtonDown", am4core.color("#353A41").lighten(-0.2));
        target.setFor("secondaryButtonActive", am4core.color("#353A41").lighten(-0.2));
        target.setFor("secondaryButtonText", am4core.color("#FFFFFF"));
        target.setFor("secondaryButtonStroke", am4core.color("#353A41"));
        target.setFor("text", am4core.color('#FFFFFF'));
        target.setFor('grid', am4core.color('#FFFFFF'));
    } else if (target instanceof am4core.ColorSet) {
        target.list = [
            am4core.color('#D438D4'),
            am4core.color('#8B50F5')
        ];
    }
}

function extract(data) {
    return data;
}
